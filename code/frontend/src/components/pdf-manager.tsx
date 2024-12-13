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

export default function PDFManager() {
  const [selectedFile, setSelectedFile] = useState<PDFFile | null>(null);
  const [files, setFiles] = useState<PDFFile[]>([]);
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

  useEffect(() => {
    if (selectedFile) {
      // Trouve le fichier correspondant dans la nouvelle liste
      const updatedFile = files.find((file) => file.id === selectedFile.id);
      if (updatedFile) {
        setSelectedFile(updatedFile);
      }
    }
  }, [files]);

  const handleClickUpdateState = async () => {
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
    }
  };

  return (
    <div className="flex h-full max-h-screen bg-background p-6 gap-6">
      <div className="w-1/3 bg-card rounded-lg shadow-lg">
        <FileList
          files={files}
          onFileSelect={setSelectedFile}
          selectedFileId={selectedFile?.id}
          onUpdateState={handleClickUpdateState}
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
          <ChangeLog file={setFiles} />
        </div>
      </div>
    </div>
  );
}
