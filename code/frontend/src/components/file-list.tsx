"use client";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ArrowUpDown } from "lucide-react";
import { useState } from "react";
import type { PDFFile } from "../types/file";

interface FileListProps {
  files: PDFFile[];
  onFileSelect: (file: PDFFile) => void;
  selectedFileId?: string;
}

export function FileList({
  files,
  onFileSelect,
  selectedFileId,
}: FileListProps) {
  const [fileList,setFileFist] = useState(files)
  const [sortByStatus, setSortByStatus] = useState(false);

  const sortedFiles = [...files].sort((a, b) => {
    // if (sortByStatus) {
    //   return a.status.localeCompare(b.status);
    // }
    // return a.name.localeCompare(b.name);
  });

  const handleClickUpdateState = async (id, status) => {
    const form = new FormData();

    form.append("id", id);
    const response = await fetch("http://127.0.0.1:8080/pdfpseudo/status", {
      method: "POST",
      body: form,
    });

    const updatedFileList = [...fileList];

    // Modifiez l'élément avec le bon id dans la copie
    for (let index in updatedFileList) {
      if (updatedFileList[index].id === id) {
        updatedFileList[index].status = !updatedFileList[index].status;
        break;
      }
    }

    // Mettez à jour l'état avec la nouvelle liste
    setFileFist(updatedFileList);
  };

  return (
    <div className="flex flex-col h-full">
        <h1>Liste des PDFS</h1>
      <ScrollArea className="flex-1">
        <div className="space-y-1 p-2">
          {files.map((file) => (
            <div
              key={file.id}
              onClick={() => onFileSelect(file)}
              className={`w-full flex items-center justify-between p-2 text-sm rounded-lg hover:bg-accent ${
                selectedFileId === file.id ? "bg-accent" : ""
              }`}
            >
              <span className="truncate">{`Fichier ${file.id}`}</span>
              <span
                className={`px-2 py-1 rounded-full text-xs ${
                  file.status === "done"
                    ? "bg-green-100 text-green-700"
                    : "bg-yellow-100 text-yellow-700"
                }`}
              >
                {`${file.status ? "Traité" : "En cours"}`}
              </span>
              <button
                onClick={() => handleClickUpdateState(file.id, !file.status)}
              >
                Traité
              </button>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
