interface PDFViewerProps {
  url: string
}

export function PDFViewer({ url }: PDFViewerProps) {
  return (
    <div className="w-full h-full bg-white rounded-lg overflow-hidden">
      <embed
        src={url}
        type="application/pdf"
        className="w-full h-full"
        style={{ minHeight: '500px' }}
      />
    </div>
  )
}

