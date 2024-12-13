interface PDFViewerProps {
  url: string;
}

export function PDFViewer({ url }: PDFViewerProps) {
  const pdfUrl = `data:application/pdf;base64,${url}`;
  return (
    <div className="w-full h-full bg-white rounded-lg overflow-hidden">
      <embed
        src={pdfUrl}
        type="application/pdf"
        className="w-full h-full"
        style={{ minHeight: "500px" }}
      />
    </div>
  );
}
