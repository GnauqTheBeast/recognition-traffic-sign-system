from pydantic import BaseModel
from typing import Optional
from config.settings import ModelType
from models.label import Label

class ClassificationResponse(BaseModel):
    label: Label
    confidence: float
    model_used: ModelType
    sample_id: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_response()

    def validate_response(self):
        """Validate classification response"""
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("Confidence must be between 0 and 1")
        if not self.label:
            raise ValueError("Label must be specified")
        if not self.model_used:
            raise ValueError("Model type must be specified")

    @classmethod
    def create_response(cls, label_id: int, label_name: str, confidence: float, 
                       model_used: ModelType, sample_id: Optional[int] = None):
        """Factory method to create response from individual fields"""
        label = Label(
            id=label_id,
            name=label_name
        )
        return cls(
            label=label,
            confidence=confidence,
            model_used=model_used,
            sample_id=sample_id
        ) 