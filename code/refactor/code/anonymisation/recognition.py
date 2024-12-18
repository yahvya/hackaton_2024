from typing_extensions import override

from presidio_analyzer import EntityRecognizer
from transformers import pipeline
from transformers.pipelines.base import Pipeline

class Recognition(EntityRecognizer):
    """
        application text recognition utility
    """

    pipeline: Pipeline
    """
        pipeline
    """
    def __init__(self,supported_entities: list[str],supported_language: str,model_id: str):
        """
        :param supported_entities: list of supported labels
        :param supported_language: supported language iso code (fr,en ...)
        :param model_id: model to use id
        """
        super().__init__(
            supported_entities= supported_entities,
            supported_language= supported_language
        )

        # initialize transformation pipeline
        self.pipeline = pipeline(
            task= "token-classification",
            model= model_id,
        )

    @override
    def analyze(self,to_analyze: str,entities=None, nlp_artifacts=None):
        results = []

        predictions = self.pipeline(to_analyze)

        print(predictions)