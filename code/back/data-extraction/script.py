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

# Classe TransformerRecognizer pour utiliser un modèle NER Transformer
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

# Configuration du pipeline NER et Presidio
mapping_labels = {"PER": "PERSON", "LOC": "LOCATION", "ORG": "ORGANIZATION", "MISC": "MISC"}
transformers_recognizer = TransformerRecognizer("Jean-Baptiste/camembert-ner", mapping_labels)

configuration = {"nlp_engine_name": "spacy", "models": [{"lang_code": "fr", "model_name": "fr_core_news_lg"}]}
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["fr"])
analyzer.registry.add_recognizer(transformers_recognizer)

anonymizer = AnonymizerEngine()

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Fonction pour anonymiser le texte
def anonymize_text(text):
    analyzer_results = analyzer.analyze(text=text, entities=None, language="fr")
    anonymized_result = anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
    return anonymized_result.text, anonymized_result.items

# Fonction pour colorer le texte anonymisé
def colorize_text(original_text, entities):
    colored_text = original_text
    for entity in sorted(entities, key=lambda x: x.start, reverse=True):
        replacement = f"\033[93m{colored_text[entity.start:entity.end]}\033[0m"
        colored_text = colored_text[:entity.start] + replacement + colored_text[entity.end:]
    return colored_text


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

text = extract_text_from_pdf(sys.argv[1])
anonymized_text, entities = anonymize_text(text)
colorized_text = colorize_text(anonymized_text, entities)
save_to_pdf(colorized_text, sys.argv[2])

words = [{"word": text[entity.start:entity.end],"start": entity.start,"end": entity.end} for entity in entities]

print(json.dumps(words))