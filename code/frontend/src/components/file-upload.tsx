"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, X } from "lucide-react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface FileWithPreview extends File {
  preview: string;
}

export default function FileUpload() {
  const [files, setFiles] = useState<FileWithPreview[]>([]);

  const [pdfAsBlob, setPdfAsBlob] = useState<Blob[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(
      acceptedFiles.map((file) =>
        Object.assign(file, {
          preview: URL.createObjectURL(file),
        })
      )
    );
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
  });

  const removeFile = (file: FileWithPreview) => {
    const newFiles = [...files];
    newFiles.splice(newFiles.indexOf(file), 1);
    setFiles(newFiles);
  };

  const uploadFiles = async () => {
    if (files.length === 0) return;

    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("pdfs[]", file);
      });

      const response = await fetch("http://127.0.0.1:8080/pdfpseudo/entities", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erreur lors de l'envoi des fichiers");
      }

      const data = await response.json();

      for (const key in data) {
        setPdfAsBlob([...pdfAsBlob, data[key].pdfAsBlob]);
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi des fichiers:", error);
    }
  };

  const thumbs = files.map((file) => (
    <Card key={file.name} className="relative inline-block m-2 ">
      <CardContent className="p-2">
        <embed
          src={file.preview}
          type="application/pdf"
          className="w-full h-full"
        />
        <button
          onClick={() => removeFile(file)}
          className="absolute top-0 right-0 bg-red-500 text-white rounded-full p-1"
          aria-label={`Supprimer ${file.name}`}
        >
          <X size={16} />
        </button>
      </CardContent>
    </Card>
  ));

  return (
    <section className="container mx-auto p-4">
      <h1 className="text-2xl font-bold pb-4">Télécharger vos PDF</h1>
      <div
        {...getRootProps()}
        className={`p-10 border-2 border-dashed rounded-lg text-center cursor-pointer ${
          isDragActive ? "border-primary" : "border-gray-300"
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto text-gray-400" size={48} />
        {isDragActive ? (
          <p>Déposez les fichiers PDF ici ...</p>
        ) : (
          <p>
            Glissez et déposez des fichiers PDF ici, ou cliquez pour
            sélectionner des fichiers
          </p>
        )}
      </div>
      <aside className="mt-4">
        <h4 className="text-lg font-semibold mb-2">
          {files.length > 0 ? "Fichiers PDF sélectionnés : " : ""}
        </h4>
        {thumbs}
      </aside>
      {pdfAsBlob.length > 0 && (
        <div>
          <h4 className="text-lg font-semibold mb-2">Fichiers PDF générés :</h4>
          {pdfAsBlob.map((pdf, index) => (
            <Card key={index} className="relative inline-block m-2">
              <CardContent className="p-2">
                <embed
                  src={URL.createObjectURL(pdf)}
                  type="application/pdf"
                  className="w-full h-full"
                />
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <Button
          className="mt-4"
          onClick={() => {
            uploadFiles();
          }}
        >
          Envoyer les fichiers
        </Button>
      )}
    </section>
  );
}
