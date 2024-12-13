"use client";

import { Button } from "@/components/ui/button";
import { Upload } from "lucide-react";
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
      const allData = []
      for (const key in data) {
        allData.push(data[key].pdfAsBlob );

      }
      setPdfAsBlob(allData)
    } catch (error) {
      console.error("Erreur lors de l'envoi des fichiers:", error);
    }
  };

  const thumbs = files.map((file) => (
    <div key={file.name} className="w-full h-[40rem] flex flex-col pb-4">
      <embed
        src={file.preview}
        type="application/pdf"
        className="w-full h-full"
      />

      {/* <Button
        className="bg-red-500 hover:bg-red-600 absolute"
        onClick={() => removeFile(file)}
      >
        <Trash className="w-4 h-4" />
      </Button> */}
    </div>
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
      {files.length > 0 && (
        <Button
          className="m-4 ml-0 w-56 h-14"
          onClick={() => {
            uploadFiles();
          }}
        >
          <p className="text-lg">Envoyer les fichiers</p>
        </Button>
      )}

      <section className="grid grid-cols-2 gap-4 pb-10">
        <div className="">
          <h1 className="text-2xl font-bold pb-4">Fichiers sélectionnés :</h1>
          {thumbs}
        </div>

        <div className="">
          <h1 className="text-2xl font-bold pb-4">
            {pdfAsBlob.length > 0 ? "Fichiers traités :" : ""}
          </h1>
          {pdfAsBlob.length > 0 && (
            <div className="flex flex-col">
              {pdfAsBlob.map((pdf, index) => (
                <div key={index} className="w-full h-[40rem] pb-4">
                  <embed
                    src={`data:application/pdf;base64,${pdf}`}
                    type="application/pdf"
                    className="w-full h-full"
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </section>
  );
}
