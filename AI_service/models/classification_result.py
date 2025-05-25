from pydantic import BaseModel
from models.label import Label
from models.classification_response import ClassificationResponse

class ClassificationResult(BaseModel):
    label: Label
    confidence: float

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_result()

    def validate_result(self):
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("Confidence must be between 0 and 1")
        if not self.label:
            raise ValueError("Label must be specified")
    
    def to_response(self, model_used, sample_id=None) -> ClassificationResponse:
        return ClassificationResponse(
            label=self.label,
            confidence=self.confidence,
            model_used=model_used,
            sample_id=sample_id
        ) 