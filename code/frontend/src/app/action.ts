'use server'

export async function uploadPDF(pdfBase64: string): Promise<string> {
  // Ici, vous implémenteriez la logique pour traiter le PDF
  // Pour cet exemple, nous allons simplement retourner le même PDF
  // Dans un cas réel, vous enverriez le PDF à un service de traitement
  
  // Simulons un délai de traitement
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  return pdfBase64
}

