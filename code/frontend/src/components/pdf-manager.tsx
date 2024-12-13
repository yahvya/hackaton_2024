"use client";

import { ChangeLog } from "@/components/change-log";
import { FileList } from "@/components/file-list";
import { PDFViewer } from "@/components/pdf-viewer";
import { useEffect, useState } from "react";

interface PDFFile {
  id: string | number;
  name?: string;
  status?: "done" | "not_done";
  url?: string;
  changes?: string[];
  entitiesConfig?: {
    content_entities?: {
      end: number;
      score: number;
    };
    metadata_entities?: {
      Title?: string;
      Author?: string;
      CreationDate?: string;
      ModificationDate?: string;
      Producer?: string;
      Creator?: string;
      [key: string]: string | undefined;
    };
  };
  rebuildPdfAsBlob?: string;
  anonymousPdfAsBlob?: string;
}

// On déplace les données exemple en dehors du composant
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
  const [files, setFiles] = useState<PDFFile[]>(sampleFiles);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPDFs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/pdfpseudo/reload", {
          method: "POST",
        });
        if (!response.ok) {
          throw new Error("Erreur lors de la récupération des PDFs");
        }
        const data = await response.json();
        setFiles(data);
      } catch (error) {
        console.error("Erreur:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPDFs();
  }, []); // Le tableau vide signifie que l'effet ne s'exécute qu'une fois au montage

  return (
    <div className="flex h-full max-h-screen bg-background p-6 gap-6">
      <div className="w-1/3 bg-card rounded-lg shadow-lg">
        <FileList
          files={files} // On utilise maintenant les fichiers de l'état
          onFileSelect={setSelectedFile}
          selectedFileId={selectedFile?.id}
        />
      </div>
      <div className="w-2/3 flex flex-col gap-6">
        <div className="h-2/3 bg-card rounded-lg shadow-lg p-4">
          {selectedFile ? (
            <PDFViewer url={selectedFile.anonymousPdfAsBlob} />
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
