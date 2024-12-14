import os
from PyPDF2 import PdfReader
from PIL import Image
import io
import cv2
import numpy as np
from skimage import transform, img_as_ubyte
import json

# Charger le classifieur Haar Cascade pour la détection de visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Créer les dossiers de sortie

# Tableau associatif entre images originales et swirlées
associative_table = {}

def extract_and_detect_faces_from_pdf(pdf_path, output_folder):
    """
    Extrait les images d'un PDF, détecte les visages, les entoure de rectangles et sauvegarde les images modifiées.
    """
    # Lire le PDF
    reader = PdfReader(pdf_path)
    image_count = 0

    for page_num, page in enumerate(reader.pages):
        if hasattr(page, "images"):

            for img in page.images:
                # Extraire les données de l'image
                image_data = img.data

                # Créer une image PIL à partir des octets
                image = Image.open(io.BytesIO(image_data))

                # Convertir l'image PIL en format OpenCV
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # Convertir l'image en niveaux de gris pour la détection de visages
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

                # Détecter les visages
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )

                # Dessiner des rectangles autour des visages détectés
                for (x, y, w, h) in faces:
                    cv2.rectangle(img_cv, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Sauvegarder l'image modifiée
                output_path = os.path.join(output_folder, f"page_{page_num+1}_image_{image_count+1}_faces.png")
                cv2.imwrite(output_path, img_cv)

                image_count += 1

def apply_swirl_to_faces(image_path, output_folder, strength=15, radius=80):
    """
    Applique un effet swirl aux visages détectés et sauvegarde l'image modifiée.
    """
    # Charger l'image avec OpenCV
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Détecter les visages
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Appliquer l'effet swirl sur chaque visage détecté
    for (x, y, w, h) in faces:
        face_region = img_rgb[y:y+h, x:x+w]
        face_region_normalized = face_region / 255.0
        swirled_face = transform.swirl(face_region_normalized, strength=strength, radius=radius)
        swirled_face_uint8 = img_as_ubyte(swirled_face)
        img_rgb[y:y+h, x:x+w] = swirled_face_uint8

    # Sauvegarder l'image finale
    swirled_img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, swirled_img)

    return output_path

def process_pdf_and_apply_swirl(pdf_path,output_pdf_path):
    """
    Pipeline complet pour extraire les images, détecter les visages, entourer les visages et appliquer un swirl.
    """
    # Étape 1 : Extraction et détection des visages
    extracted_folder=os.path.dirname(output_pdf_path) + "/tmp"
    extract_and_detect_faces_from_pdf(pdf_path, extracted_folder)
    swirl_folder=os.path.dirname(output_pdf_path) + "/tmp"

    # Étape 2 : Appliquer l'effet swirl aux images extraites
    for image_file in os.listdir(extracted_folder):
        image_path = os.path.join(extracted_folder, image_file)
        swirled_image_path = apply_swirl_to_faces(image_path, swirl_folder)

        # Ajouter au tableau associatif
        associative_table[image_path] = swirled_image_path

    # Sauvegarder le tableau associatif dans un fichier JSON
    json_path = os.path.join(os.path.dirname(swirl_folder), "associative_table.json")
    with open(json_path, "w") as json_file:
        json.dump(associative_table, json_file, indent=4)

def convert_images_to_pdf(images_folder, output_pdf_path):
    """
    Convertit toutes les images d'un dossier en un fichier PDF.
    """
    image_files = [
        os.path.join(images_folder, file) for file in os.listdir(images_folder)
        if file.endswith(('.png', '.jpg', '.jpeg'))
    ]

    if not image_files:
        return

    # Charger les images et les convertir en mode RGB
    images = [Image.open(image_file).convert('RGB') for image_file in image_files]

    # Créer un fichier PDF à partir des images
    images[0].save(output_pdf_path, save_all=True, append_images=images[1:])