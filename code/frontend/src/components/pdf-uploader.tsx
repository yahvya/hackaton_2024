'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { uploadPDF } from './actions'

export default function PDFUploader() {
  const [originalPDF, setOriginalPDF] = useState<string | null>(null)
  const [processedPDF, setProcessedPDF] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setIsLoading(true)
      const reader = new FileReader()
      reader.onload = async (e) => {
        const base64 = e.target?.result as string
        setOriginalPDF(base64)
        
        try {
          const response = await uploadPDF(base64.split(',')[1])
          setProcessedPDF(`data:application/pdf;base64,${response}`)
        } catch (error) {
          console.error('Error processing PDF:', error)
        } finally {
          setIsLoading(false)
        }
      }
      reader.readAsDataURL(file)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">PDF Uploader et Processeur</h1>
      <Card>
        <CardHeader>
          <CardTitle>Téléverser un PDF</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2">
            <Input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={isLoading}
            />
            <Button disabled={isLoading}>
              {isLoading ? 'Traitement...' : 'Téléverser'}
            </Button>
          </div>
        </CardContent>
      </Card>
      
      {originalPDF && (
        <PDFViewer title="PDF Original" pdfData={originalPDF} />
      )}
      
      {processedPDF && (
        <PDFViewer title="PDF Traité" pdfData={processedPDF} />
      )}
    </div>
  )
}

function PDFViewer({ title, pdfData }: { title: string, pdfData: string }) {
  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <embed
          src={pdfData}
          type="application/pdf"
          width="100%"
          height="600px"
        />
      </CardContent>
    </Card>
  )
}

