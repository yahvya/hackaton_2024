import fitz
import sys
import json
import re
import rstr

# parse the pdf text and provide the first element list
def get_words_to_anonymize_map(text):
    analyzer = build_analyzer()
    analyzer_results = analyzer.analyze(text=text, entities=None, language="fr")
    allowed_types = ["PERSON","LOCATION","EMAIL_ADDRESS","CREDIT_CARD","CRYPTO","IBAN_CODE","PHONE_NUMBER","ORGANISATION","NUMBER","MISC","DATE_TIME","IP_ADDRESS","NRP","MEDICAL_LICENSE","URL"]
    filtered_list_by_score = list(filter(lambda result: result.score >= 0.3 and result.entity_type in allowed_types, analyzer_results))
    return [{"word": text[result.start:result.end],"start": result.start,"end":result.end,"type": result.entity_type,"score": result.score} for result in filtered_list_by_score]

# take an input string and regexify the string
def regexify_str(input_str):
    regex_str = ""

    regex_map = [
        "[\+]",
        "[\-]",
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
            if re.match(regex,char):
                regex_str = regex_str + regex
                break

    return regex_str

# generate a text from a model pattern
def generate_text_from_regex(regex):
    return rstr.xeger(regex)

# convert the pdf doc color to pdf
def convert_color_to_rgb(color_value):
    # Convert ARGB color value to RGB
    # color_value is an int in ARGB format (e.g., -13343324)
    alpha = (color_value >> 24) & 0xFF  # Get alpha component
    red = (color_value >> 16) & 0xFF    # Get red component
    green = (color_value >> 8) & 0xFF   # Get green component
    blue = color_value & 0xFF           # Get blue component

    # Convert to a range 0 to 1
    return (red / 255.0, green / 255.0, blue / 255.0)

# load the pdf doc
def load_pdf(file_path):
    doc = fitz.open(file_path)
    return doc

# extract text from the pdf
def extract_text_and_positions(doc):
    text_positions = {}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        text_positions[page_num] = [
            {"text": block[4], "bbox": block[:4]} for block in blocks
        ]
    
    return text_positions

# replace text in pdf
def replace_text_in_pdf(doc,words_map):
    new_doc = fitz.open()
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        
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
                    font_name = span["font"]
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

                    replace_text = original_text

                    for word_data in  words_map:
                        if re.match(f".*{re.escape(word_data['word'])}.*",replace_text):
                            replace_text = replace_text.replace(word_data["word"],word_data["modified_word"])

                    # Utiliser la couleur de fond extraite pour le rectangle
                    new_page.draw_rect(rect, color=background_color, fill=background_color)
                    
                    # Calculer le point d'insertion ajusté
                    # Ajout d'un décalage vertical basé sur la taille de la police
                    insertion_point = fitz.Point(
                        rect.tl.x,  # x reste identique
                        rect.tl.y + font_size * 0.85  # ajustement vertical
                    )
                    
                    new_page.insert_text(
                        insertion_point,
                        replace_text,
                        fontname="helv",
                        fontsize=font_size,
                        color=convert_color_to_rgb(color)
                    )
    return new_doc

def generate_text(words_map,file_path):
    pass

def extract_pdf_text(pdf_doc):
    doc_data = extract_text_and_positions(pdf_doc)
    pdf_content = ""

    for key in doc_data:
        for row_config in doc_data[key]:
            pdf_content = pdf_content + row_config["text"]

    return pdf_content

def build_words_map(pdf_text):
    words = get_words_to_anonymize_map(pdf_text)
    regexyfied_words = [
        {"word": word_data["word"], "modified_word": generate_text_from_regex(regexify_str(word_data["word"])),
         "start": word_data["start"], "end": word_data["end"],"type": word_data["type"]} for word_data in words]

    modified_text = pdf_text

    for word_data in regexyfied_words:
        modified_text = modified_text[:word_data["start"]] + word_data["word"] + modified_text[word_data["end"]:]

    return regexyfied_words

# anonymize pdf content
def anonymize_pdf(input_file_path,output_file_path):
    pdf_doc = load_pdf(input_file_path)
    pdf_text = extract_pdf_text(pdf_doc)
    words_map = build_words_map(pdf_text)

    # replace and save pdf
    new_pdf_doc = replace_text_in_pdf(pdf_doc,words_map)
    new_pdf_doc.save(output_file_path)

    # free ressource
    pdf_doc.close()
    new_pdf_doc.close()

    print(json.dumps(words_map))

anonymize_pdf(sys.argv[1],sys.argv[2])