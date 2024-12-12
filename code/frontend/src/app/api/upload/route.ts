import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const files = formData.getAll("files");

    // Ici, ajoutez votre logique pour traiter les fichiers
    // Par exemple, les sauvegarder dans un stockage cloud ou sur le serveur

    return NextResponse.json({
      success: true,
      message: "Fichiers reçus avec succès",
      filesCount: files.length,
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, message: "Erreur lors du traitement des fichiers" },
      { status: 500 }
    );
  }
}
