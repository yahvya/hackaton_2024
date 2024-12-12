import os

from PyPDF2 import PdfReader
from fpdf import FPDF
from transformers import pipeline
from presidio_analyzer import AnalyzerEngine, RecognizerResult, EntityRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
import sys
import json
from reportlab.pdfgen import canvas
import re
import rstr

class TransformerRecognizer(EntityRecognizer):
    def __init__(self, model_id, mapping_labels, aggregation_strategy="simple"):
        super().__init__(supported_entities=list(mapping_labels.values()), supported_language="fr")
        self.pipeline = pipeline(
            "token-classification",
            model=model_id,
            aggregation_strategy=aggregation_strategy,
            ignore_labels=["O"]
        )
        self.label2presidio = mapping_labels

    def analyze(self, text, entities=None, nlp_artifacts=None):
        results = []
        predictions = self.pipeline(text)
        for entity in predictions:
            if entity["entity_group"] in self.label2presidio:
                converted_entity = self.label2presidio[entity["entity_group"]]
                if entities is None or converted_entity in entities:
                    results.append(
                        RecognizerResult(
                            entity_type=converted_entity,
                            start=entity["start"],
                            end=entity["end"],
                            score=entity["score"]
                        )
                    )
        return results

def build_analyzer():
    mapping_labels = {"PERSON": "PERSON", "LOCATION": "LOCATION", "ORGANIZATION": "ORGANIZATION",
                      "EMAIL_ADDRESS": "EMAIL_ADDRESS", "PHONE_NUMBER": "PHONE_NUMBER","CREDIT_CARD": "CREDIT_CARD","CRYPTO": "CRYPTO","IBAN_CODE": "IBAN_CODE","IP_ADDRESS":"IP_ADDRESS"}
    transformers_recognizer = TransformerRecognizer("Jean-Baptiste/camembert-ner", mapping_labels)

    configuration = {"nlp_engine_name": "spacy", "models": [{"lang_code": "fr", "model_name": "fr_core_news_lg"}]}
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["fr"])
    analyzer.registry.add_recognizer(transformers_recognizer)

    return analyzer

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_words_to_anonymize_map(text):
    analyzer = build_analyzer()
    analyzer_results = analyzer.analyze(text=text, entities=None, language="fr")
    allowed_types = ["PERSON","LOCATION","EMAIL_ADDRESS","CREDIT_CARD","CRYPTO","IBAN_CODE","PHONE_NUMBER","ORGANISATION","NUMBER"]
    filtered_list_by_score = list(filter(lambda result: result.score >= 0.4 and result.entity_type in allowed_types, analyzer_results))
    return [{"word": text[result.start:result.end],"start": result.start,"end":result.end,"type": result.entity_type,"score": result.score} for result in filtered_list_by_score]

def save_to_pdf(text, output_path):
    c = canvas.Canvas(output_path)
    c.setFont("Helvetica", 12)
    width, height = 595.27, 841.89  # Taille A4 en points
    y = height - 40  # Position de départ en haut de la page

    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 15
        if y < 40:  # Ajoutez une nouvelle page si nécessaire
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 40

    c.save()

def regexify_str(input_str):
    regex_str = ""

    regex_map = [
        "[\n]",
        "[ ]",
        "[\r]",
        "[\t]",
        "[a-zA-Z]",
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

def generate_text_from_regex(regex):
    return rstr.xeger(regex)

# read pdf and get words data
pdf_text = extract_text_from_pdf(sys.argv[1])
words = get_words_to_anonymize_map(pdf_text)

# replace element in word data
regexyfied_words = [{"word": word_data["word"],"modified_word": generate_text_from_regex(regexify_str(word_data["word"])),"start": word_data["start"],"end": word_data["end"]} for word_data in words]

modified_text = pdf_text

for word_data in regexyfied_words:
    modified_text = modified_text[:word_data["start"]] + word_data["word"] + modified_text[word_data["end"]:]

save_to_pdf(modified_text, sys.argv[2])

print(json.dumps(regexyfied_words))