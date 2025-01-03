from dataclasses import dataclass
from typing import Dict, List

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from anonymisation.recognition.text.transform_recognizer import TransformRecognizer

@dataclass
class TextParseResult:
    """
        text parse result from entity data
    """

    type: str
    """
        entity type , replaced with the provided replacement
    """

    start: int
    """
        element start pos in input str
    """

    end: int
    """
        element end pos in input str
    """

    score: float
    """
        element possibility score
    """

    word: str
    """
        founded word
    """

class TextRecognizer:
    """
        application text recognizer
    """
    default_text_elements_mapping = {
        "PERSON": "person",
        "ORG": "organization",
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

    default_nlp_configuration: Dict[str,List[Dict[str,str]]] = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "fr",
                "model_name": "fr_core_news_lg"
            }
        ]
    }

    __analyzer: AnalyzerEngine
    """
        internal analyzer
    """

    __supported_language: str
    """
        internal supported language
    """

    __text_elements_mapping: Dict[str, str]
    """
        text elements mapping
    """

    def __init__(self,nlp_configuration: Dict[str,List[Dict[str,str]]] = None,text_elements_mapping: Dict[str,str] = None,ignore_labels: List[str] = None):
        """
        :param nlp_configuration: nlp configuration base on the default one format
        :param text_elements_mapping: text elements label mapping base on the default one format
        :param ignore_labels: labels to ignore
        :throws Exception: on error during init
        """

        # treating default arguments
        nlp_configuration = nlp_configuration or self.default_nlp_configuration
        self.__text_elements_mapping = text_elements_mapping or self.default_text_elements_mapping
        ignore_labels = ignore_labels or []

        # create and configure the analyzer
        self.__analyzer = AnalyzerEngine(
            nlp_engine= NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine(),
            supported_languages= [model_config["lang_code"] for model_config in nlp_configuration["models"]]
        )

        self.__supported_language = nlp_configuration["models"][0]["lang_code"]
        self.__analyzer.registry.add_recognizer(recognizer= TransformRecognizer(
            supported_entities_mapping= self.__text_elements_mapping,
            model_id= "Jean-Baptiste/camembert-ner",
            ignore_labels= ignore_labels,
            supported_language= self.__supported_language

        ))

    def analyze(self,text: str) -> List[TextParseResult]:
        """
        analyze the provided text
        :param text: input text
        :return: list of recognized entities as a list of TexTParseResult
        :throws Exception: on error during analysis
        """
        results = self.__analyzer.analyze(
            text= text,
            language= self.__supported_language,
            entities= list(self.__text_elements_mapping.keys()),
        )

        return [TextParseResult(
            type= self.__text_elements_mapping[result.entity_type],
            start= result.start,
            end= result.end,
            score= result.score,
            word= text[result.start:result.end]
        ) for result in results]

