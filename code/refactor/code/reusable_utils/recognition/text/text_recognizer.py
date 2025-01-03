from dataclasses import dataclass
from typing import Dict, List

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer import EntityRecognizer


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
        text recognizer
    """

    __analyzer: AnalyzerEngine
    """
        internal analyzer
    """

    __text_elements_mapping: Dict[str, str]
    """
        text elements mapping
    """

    __languages_code: List[str]
    """
        internal languages code extracted from models config
    """

    def __init__(self,recognizers: List[EntityRecognizer],nlp_configuration: Dict[str,List[Dict[str,str]]],text_elements_mapping: Dict[str,str]):
        """
        :param recognizers: list of entity recognizers
        :param nlp_configuration: nlp configuration base on the default one format
        :param text_elements_mapping: mapping of text elements
        :throws Exception: on error during init
        """

        # extract internal vars, unique or langs
        self.__text_elements_mapping = text_elements_mapping
        self.__languages_code = list(set([model_config["lang_code"] for model_config in nlp_configuration["models"]]))

        # create and configure the analyzer
        self.__analyzer = AnalyzerEngine(
            nlp_engine= NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine(),
            supported_languages= self.__languages_code
        )

        for recognizer in recognizers:
            self.__analyzer.registry.add_recognizer(recognizer= recognizer)

    def analyze(self,text: str) -> List[TextParseResult]:
        """
        analyze the provided text
        :param text: input text
        :return: list of recognized entities as a list of TexTParseResult
        :throws Exception: on error during analysis
        """
        results = []

        for lang_code in self.__languages_code :
            results.extend(self.__analyzer.analyze(
                text=text,
                language= lang_code,
                entities=list(self.__text_elements_mapping.keys()),
            ))

        return [TextParseResult(
            type= self.__text_elements_mapping[result.entity_type],
            start= result.start,
            end= result.end,
            score= result.score,
            word= text[result.start:result.end]
        ) for result in results]

