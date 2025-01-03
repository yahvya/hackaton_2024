import re
from typing import Dict, List

from spire.pdf import PdfDocument, Utilities_PdfImageInfo, PdfTextReplacer, PdfImageHelper
from reusable_utils.pdf_treatment.pdf_parser import PDFParser
from reusable_utils.recognition.text.text_recognizer import TextRecognizer, TextParseResult
from reusable_utils.recognition.text.transform_recognizer import TransformRecognizer


class Anonymiser:
    """
        app anonymiser
    """
    default_nlp_configuration: Dict[str, List[Dict[str, str]]] = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "fr",
                "model_name": "fr_core_news_lg"
            }
        ]
    }

    default_text_elements_mapping = {
        "PERSON": "person",
        "ORG": "organization",
        "ORGANIZATION": "organization",
        "LOCATION": "location",
        "CREDIT_CARD": "credit_card",
        "CRYPTO": "crypto",
        "DATE_TIME": "date_time",
        "EMAIL_ADDRESS": "email",
        "PHONE_NUMBER": "phone",
        "IBAN_CODE": "iban",
        "IP_ADDRESS": "ip",
        "NRP": "nationality",
        "MEDICAL_LICENSE": "medical_license",
        "URL": "url",
        "ID": "id",
        "IN_VOTER": "in_voter",
        "AGE": "age",
        "LOC": "location",
        "PER": "person",
        "EMAIL": "email",
        "DATE": "date"
    }
    """
        text elements label mapping
    """

    app_recognizers_utils = [
        TransformRecognizer(
            supported_entities_mapping=default_text_elements_mapping,
            model_id="Jean-Baptiste/camembert-ner",
            ignore_labels=["O", "MISC"],
            supported_language="fr"
        )
    ]
    """
        application recognizers list
    """

    text_recognizer = TextRecognizer(
        recognizers= app_recognizers_utils,
        nlp_configuration= default_nlp_configuration,
        text_elements_mapping= default_text_elements_mapping,
    )
    """
        text recognizer
    """

    @staticmethod
    def anonymise_pdf(pdf_file_path:str) -> PdfDocument:
        """
            anonymise pdf file from the given path
            :param pdf_file_path: pdf file path
            :return PdfDocument: the modified pdf document to close after
        """

        return PDFParser(pdf_file_path=pdf_file_path).parse_content(
            todo_during_parsing= Anonymiser.__to_do_during_parsing
        )

    @staticmethod
    def __to_do_during_parsing(page_text:str, page_images:List[Utilities_PdfImageInfo], page_text_replacer:PdfTextReplacer, page_image_helper:PdfImageHelper):
        """
            action to do on parsed block in the pdf
            :param page_text: page text content
            :param page_images: page images content
            :page_text_replacer: page text replacer util
            :page_image_helper: page image helper
        """

        # replace texts
        text_analyze_filtered_results = Anonymiser.filter_bad_detections(results= Anonymiser.text_recognizer.analyze(text= page_text))

        for result in text_analyze_filtered_results:
            print(result)
            page_text_replacer.ReplaceText(oldText= result.word,newText= "<remplacement>")

    @staticmethod
    def filter_bad_detections(results: List[TextParseResult]) -> List[TextParseResult]:
        """
        filter bad detections
        :param results: list of TextParseResult
        :return List[TextParseResult]
        """
        return results