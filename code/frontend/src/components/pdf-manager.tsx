"use client";

import { ChangeLog } from "@/components/change-log";
import { FileList } from "@/components/file-list";
import { PDFViewer } from "@/components/pdf-viewer";
import { useState } from "react";
interface PDFFile {
  id: string;
  name: string;
  status: "done" | "not_done";
  url: string;
  changes?: string[];
}

// Sample data - replace with your actual data source
const sampleFiles: PDFFile[] = [
  {
    id: "1",
    name: "document1.pdf",
    status: "done",
    url: "/document1.pdf",
    changes: ["Updated page 1", "Fixed formatting"],
  },
  {
    id: "2",
    name: "document2.pdf",
    status: "not_done",
    url: "/document2.pdf",
    changes: [],
  },
  // Add more sample files as needed
];

export default function PDFManager() {
  const [selectedFile, setSelectedFile] = useState<PDFFile | null>(null);

  return (
    <div className="flex h-full max-h-screen bg-background p-6 gap-6">
      <div className="w-1/3 bg-card rounded-lg shadow-lg">
        <FileList
          files={sampleFiles}
          onFileSelect={setSelectedFile}
          selectedFileId={selectedFile?.id}
        />
      </div>
      <div className="w-2/3 flex flex-col gap-6">
        <div className="h-2/3 bg-card rounded-lg shadow-lg p-4">
          {selectedFile ? (
            <PDFViewer url={selectedFile.url} />
          ) : (
            <div className="h-full flex items-center justify-center text-muted-foreground">
              Select a file to view
            </div>
          )}
        </div>
        <div className="h-1/3 bg-card rounded-lg shadow-lg">
          <ChangeLog file={selectedFile} />
        </div>
      </div>
    </div>
  );
}
