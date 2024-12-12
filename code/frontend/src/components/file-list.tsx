'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ArrowUpDown } from 'lucide-react'
import type { PDFFile } from '../types/file'

interface FileListProps {
  files: PDFFile[]
  onFileSelect: (file: PDFFile) => void
  selectedFileId?: string
}

export function FileList({ files, onFileSelect, selectedFileId }: FileListProps) {
  const [sortByStatus, setSortByStatus] = useState(false)

  const sortedFiles = [...files].sort((a, b) => {
    if (sortByStatus) {
      return a.status.localeCompare(b.status)
    }
    return a.name.localeCompare(b.name)
  })

  return (
    <div className="flex flex-col h-full">
      <Button
        variant="ghost"
        className="flex justify-between w-full p-4"
        onClick={() => setSortByStatus(!sortByStatus)}
      >
        <span>Sort by {sortByStatus ? 'Name' : 'Status'}</span>
        <ArrowUpDown className="h-4 w-4" />
      </Button>
      <ScrollArea className="flex-1">
        <div className="space-y-1 p-2">
          {sortedFiles.map((file) => (
            <button
              key={file.id}
              onClick={() => onFileSelect(file)}
              className={`w-full flex items-center justify-between p-2 text-sm rounded-lg hover:bg-accent ${
                selectedFileId === file.id ? 'bg-accent' : ''
              }`}
            >
              <span className="truncate">{file.name}</span>
              <span
                className={`px-2 py-1 rounded-full text-xs ${
                  file.status === 'done'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-yellow-100 text-yellow-700'
                }`}
              >
                {file.status}
              </span>
            </button>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}

