from typing import Dict, List

from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from transformers import pipeline, Pipeline


class TransformRecognizer(EntityRecognizer):
    """
        transform recognizer
    """

    pipeline: Pipeline
    """
        pipeline
    """

    label2presidio: Dict[str, str]
    """
        from supported entities mapping
    """

    def __init__(self,supported_entities_mapping: Dict[str,str],model_id: str,ignore_labels:List[str] = None,supported_language= "fr",aggregation_strategy:str = "simple"):
        """
        :doc https://microsoft.github.io/presidio/supported_entities/
        :param supported_entities_mapping: supported entities mapping from doc
        :param model_id: model to use id
        :param ignore_labels: labels to ignore list
        :param supported_language: supported language
        :param aggregation_strategy: aggregation strategy
        :throws Exception: on error during init
        """

        # treating default arguments
        ignore_labels = ignore_labels or []

        super().__init__(
            supported_entities= list(supported_entities_mapping.keys()),
            supported_language= supported_language
        )

        # init pipeline and presidio convertion mapping
        self.pipeline = pipeline(
            task= "token-classification",
            model= model_id,
            aggregation_strategy= aggregation_strategy,
            ignore_labels= ignore_labels,
            use_fast=False
        )
        self.label2presidio = supported_entities_mapping


    def load(self) -> None:
        """
            abstract method implemented
        """
        pass

    def analyze(self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts) -> List[RecognizerResult]:
        results = []

        # detect and format predictions in results
        predicted_entities = self.pipeline(text)

        if len(predicted_entities) > 0:
            for e in predicted_entities:
                if e["entity_group"] not in self.label2presidio:
                    continue

                converted_entity = self.label2presidio[e["entity_group"]]

                if converted_entity in entities or entities is None:
                    results.append(
                        RecognizerResult(
                            entity_type=converted_entity,
                            start=e["start"],
                            end=e["end"],
                            score=e["score"]
                        )
                    )

        return results