import re
from typing import Dict, List

from faker import Faker
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
    """
        replacement regex map
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

    __faker: Faker = Faker()
    """
        internal faker 
    """

    anonymise_with_semantic: bool
    """
        define if pdf should be anonymised by keeping semantic
    """

    def anonymise_pdf(self,pdf_file_path:str,anonymise_with_semantic: bool = True) -> PdfDocument:
        """
            anonymise pdf file from the given path
            :param pdf_file_path: pdf file path
            :param anonymise_with_semantic: whether to anonymise pdf with semantic
            :return PdfDocument: the modified pdf document to close after
        """

        self.anonymise_with_semantic = anonymise_with_semantic

        return PDFParser(pdf_file_path=pdf_file_path).parse_content(
            todo_during_parsing= self.__to_do_during_parsing
        )

    def __to_do_during_parsing(self,page_text:str, page_images:List[Utilities_PdfImageInfo], page_text_replacer:PdfTextReplacer, page_image_helper:PdfImageHelper):
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
            page_text_replacer.ReplaceText(oldText= result.word,newText= self.replace_text_element_with(result= result))

    def replace_text_element_with(self,result: TextParseResult) -> str:
        """
            replace text element with another string based on the defined anonymisation mode
            :param result: result from text_recognizer
            :return str: replaced text
        """
        return Anonymiser.regexify_str(input_str= result.word) if not self.anonymise_with_semantic else Anonymiser.fake_str_from_type(input_str= result.word,type_from_mapping_elements= result.type)

    @staticmethod
    def filter_bad_detections(results: List[TextParseResult]) -> List[TextParseResult]:
        """
        filter bad detections
        :param results: list of TextParseResult
        :return List[TextParseResult]
        """
        return results

    @staticmethod
    def regexify_str(input_str:str) -> str:
        """
            replace each character of the input str by an item with the same format based on a regex matching. the result will have the same format (same length ... as the input_str)
            :param input_str: input string
            :return str: replaced string
        """
        regex_str = ""

        for char in input_str:
            for regex in Anonymiser.regex_map:
                if re.match(regex, char):
                    regex_str = regex_str + regex
                    break

        return regex_str

    @staticmethod
    def fake_str_from_type(input_str:str,type_from_mapping_elements: str) -> str:
        """
            fake the input string with an element with the same semantic, the format (len ...) isn't guaranteed
            :param input_str: input string
            :param type_from_mapping_elements: element type from mapping elements, if the type don't match regexify will be used
            :return str: fake string
        """

        match_map = {
            "person": lambda : Anonymiser.__faker.full_name(),
            "organization": lambda : Anonymiser.__faker.company(),
            "id": lambda : Anonymiser.__faker.org_id(),
            "email": lambda : Anonymiser.__faker.email(),
            "url": lambda : Anonymiser.__faker.url(),
            "iban": lambda : Anonymiser.__faker.iban(),
            "location": lambda : Anonymiser.__faker.address(),
            "credit_card": lambda : Anonymiser.__faker.credit_card_number(),
            "crypto": lambda : Anonymiser.__faker.cryptocurrency_name(),
            "date_time": lambda : Anonymiser.__faker.date_time().strftime("%d/%m/%Y"),
            "phone": lambda : Anonymiser.__faker.phone_number(),
            "ip": lambda : Anonymiser.__faker.ipv4(),
            "nationality": lambda : Anonymiser.__faker.nationality(),
            "medical_license": lambda : Anonymiser.__faker.license_plate(),
            "in_voter": lambda : "in voter",
            "age": lambda : Anonymiser.__faker.birth_number(),
            "date": lambda : Anonymiser.__faker.date()
        }

        return match_map[type_from_mapping_elements]() if type_from_mapping_elements in match_map else Anonymiser.regexify_str(input_str= input_str)