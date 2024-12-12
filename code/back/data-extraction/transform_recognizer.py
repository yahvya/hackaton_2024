from transformers import pipeline
from presidio_analyzer import AnalyzerEngine, RecognizerResult, EntityRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider

# transform recognizer
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

    @staticmethod
    def build_analyser():
        mapping_labels = {"PERSON": "PERSON", "LOCATION": "LOCATION", "ORGANIZATION": "ORGANIZATION",
                          "EMAIL_ADDRESS": "EMAIL_ADDRESS", "PHONE_NUMBER": "PHONE_NUMBER",
                          "CREDIT_CARD": "CREDIT_CARD", "CRYPTO": "CRYPTO", "IBAN_CODE": "IBAN_CODE",
                          "IP_ADDRESS": "IP_ADDRESS"}
        transformers_recognizer = TransformerRecognizer("Jean-Baptiste/camembert-ner", mapping_labels)

        configuration = {"nlp_engine_name": "spacy", "models": [{"lang_code": "fr", "model_name": "fr_core_news_lg"}]}
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["fr"])
        analyzer.registry.add_recognizer(transformers_recognizer)

        return analyzer