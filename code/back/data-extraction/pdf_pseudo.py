import fitz
import re

import pikepdf
import rstr
import faker
from PyPDF2 import PdfReader


# pdf pseudo manager
class PdfPseudo:
    def __init__(self,input_file_path,analyser):
        self.input_file_path = input_file_path
        self.analyzer = analyser
        self.doc = None
        self.fake = faker.Faker()
        self.anonymized_items = []
        self.new_metadata = {}

    # regexify a file
    def regexify_str(self,input_str):
        regex_str = ""

        regex_map = [
            "[\+]",
            "-",
            "[\/]",
            "[\(]",
            "[\)]",
            "[\n]",
            "[ ]",
            "[\r]",
            "[\t]",
            "[A-Z]",
            "[a-z]",
            "[0-9]",
            "[@]",
            "[.]",
            "[ÉÈÀÙÂÊÎÔÛÄËÏÖÜÇéèàùâêîôûäëïöüç]",
            "."
        ]

        for char in input_str:
            for regex in regex_map:
                if re.match(regex, char):
                    regex_str = regex_str + regex
                    break

        return regex_str

    # generate a phonenumber with the same format
    def generate_phone_number_with_format(self,base_phone_number):
        digits_only = re.sub(r'\D', '', base_phone_number)
        format_pattern = re.sub(r'\d', 'X', base_phone_number)

        generated_phone = self.fake.phone_number()

        generated_digits = re.sub(r'\D', '', generated_phone)

        if len(generated_digits) < len(digits_only):
            generated_digits = generated_digits.ljust(len(digits_only), '0')
        elif len(generated_digits) > len(digits_only):
            generated_digits = generated_digits[:len(digits_only)]
        phone_number_with_format = ""
        digit_index = 0

        for char in format_pattern:
            if char == 'X':  # Si c'est une place pour un chiffre
                phone_number_with_format += generated_digits[digit_index]
                digit_index += 1
            else:  # Garder les caractères non numériques (tirets, espaces, etc.)
                phone_number_with_format += char

        return phone_number_with_format

    # anonymise internal
    def anonymise_internal(self,text):
        words_map = self.get_words_to_anonymize_map(text=text)
        special_chars_regex = "[ÉÈÀÙÂÊÎÔÛÄËÏÖÜÇéèàùâêîôûäëïöüç]"

        for word_data in words_map:
            if word_data["score"] < 0.4:
                continue

            if word_data["type"] == "PERSON":
                base_len = len(word_data["word"])
                name = self.fake.name()[:base_len]

                # vérifier les accents
                for index in range(base_len):
                    char = word_data["word"][index]
                    if re.match(special_chars_regex, char):
                        name = name[:index] + rstr.xeger(special_chars_regex) + name[index:]

                word_data["modified"] = name
            elif word_data["type"] == "DATE_TIME":
                word_data["modified"] = self.fake.date()
            elif word_data["type"] == "EMAIL_ADDRESS":
                word_data["modified"] = self.fake.email()
                base_len = len(word_data["word"])
                while len(word_data["modified"]) > base_len:
                    word_data["modified"] = self.fake.email()
            elif word_data["type"] == "PHONE_NUMBER":
                word_data["modified"] = self.generate_phone_number_with_format(word_data["word"])
            else:
                word_data["modified"] = rstr.xeger(self.regexify_str(input_str=word_data["word"]))

            self.anonymized_items.append(word_data)

            text = text[:word_data["start"]] + word_data["modified"] + text[word_data["end"]:]
        return text

    # process the anonymise process
    def anonymise(self,output_file_path):
        self.new_metadata = {}

        reader = PdfReader(self.input_file_path)
        pdf_metadatas = reader.metadata

        if "/ecv-data" in pdf_metadatas:
            del pdf_metadatas["/ecv-data"]

        for metadata_key in pdf_metadatas:
            self.anonymized_items = []
            self.new_metadata[metadata_key] = {
                "modified": self.anonymise_internal(text=str(pdf_metadatas[metadata_key])),
                "entities": self.anonymized_items
            }

        with pikepdf.open(self.input_file_path) as pdf:
            pdf.metadata = self.new_metadata

            # Save the modified PDF
            pdf.save(output_file_path)

        self.anonymized_items = []
        self.parse_pdf(to_do_for_line= self.anonymise_internal)
        pdf_content_items = self.anonymized_items

        return {
            "content_entities": pdf_content_items,
            "metadata_entities": self.new_metadata
        }

    # process the reconstruct
    def reconstruct(self,entities_map):
        pass

    # provided base map of words to anonymise
    def get_words_to_anonymize_map(self,text):
        analyzer_results = self.analyzer.analyze(text=text, entities=None, language="fr")
        allowed_types = ["PERSON","DATE_TIME","EMAIL_ADDRESS", "LOCATION" , "CREDIT_CARD", "CRYPTO", "IBAN_CODE", "PHONE_NUMBER","ORGANISATION", "NUMBER", "MISC", "IP_ADDRESS", "NRP", "MEDICAL_LICENSE", "URL"]
        filtered_list_by_score = list(
            filter(lambda result: result.score >= 0.3 and result.entity_type in allowed_types, analyzer_results))
        return [{"word": text[result.start:result.end], "start": result.start, "end": result.end,
                 "type": result.entity_type, "score": result.score} for result in filtered_list_by_score]

    # convert pdf color to rgb
    def convert_color_to_rgb(self,color_value):
        # Convert ARGB color value to RGB
        # color_value is an int in ARGB format (e.g., -13343324)
        alpha = (color_value >> 24) & 0xFF  # Get alpha component
        red = (color_value >> 16) & 0xFF  # Get red component
        green = (color_value >> 8) & 0xFF  # Get green component
        blue = color_value & 0xFF  # Get blue component

        # Convert to a range 0 to 1
        return (red / 255.0, green / 255.0, blue / 255.0)

    # parse the pdf
    def parse_pdf(self,to_do_for_line):
        doc = fitz.open(self.input_file_path)
        self.doc = fitz.open()

        for page_num in range(len(doc)):
            page = doc[page_num]
            new_page = self.doc.new_page(width=page.rect.width, height=page.rect.height)

            # Copier le contenu original
            new_page.show_pdf_page(new_page.rect, doc, page_num)

            dict_blocks = page.get_text("dict")
            blocks = dict_blocks["blocks"]

            for block in blocks:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line["spans"]:
                        rect = fitz.Rect(span["bbox"])
                        font_size = span["size"]
                        color = span["color"]
                        original_text = span["text"]

                        # Extraire la couleur de fond
                        background_color = None
                        try:
                            # Obtenir le pixmap de la zone
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)
                            # Prendre la couleur du premier pixel (supposé être la couleur de fond)
                            background_color = pix.pixel(0, 0)
                            # Convertir en RGB normalisé (0-1)
                            background_color = (
                                background_color[0] / 255.0,
                                background_color[1] / 255.0,
                                background_color[2] / 255.0
                            )
                        except:
                            # En cas d'erreur, utiliser le blanc comme couleur par défaut
                            background_color = (1, 1, 1)

                        # Utiliser la couleur de fond extraite pour le rectangle
                        # new_page.draw_rect(rect, color=background_color, fill=background_color)

                        # Calculer le point d'insertion ajusté
                        # Ajout d'un décalage vertical basé sur la taille de la police
                        #insertion_point = fitz.Point(
                            #rect.tl.x,  # x reste identique
                            #rect.tl.y + font_size * 0.85  # ajustement vertical
                        #)

                        #new_page.insert_text(
                            #insertion_point,
                            #replace_text,
                            #fontname="helv",
                            #fontsize=font_size,
                            #color=self.convert_color_to_rgb(color_value=color)
                        #)
                        redact_annot = new_page.add_redact_annot(
                            rect,
                            text=to_do_for_line(original_text),
                            fontname="helv",  # Utilisation de la police helvetica
                            fontsize=font_size,  # Taille de police d'origine
                            text_color= self.convert_color_to_rgb(color),  # Couleur du texte d'origine
                            fill=background_color  # Couleur de fond détectée
                        )
            new_page.apply_redactions()
        return self.doc

    # save the current doc in file
    def save_result_in(self,output_file_path):
        self.doc.save(output_file_path)

    # free class resources
    def free_resources(self,output_file_path):
        self.doc.close()
