from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .bounding_box import BoundingBox
from .label import Label

class Sample(BaseModel):
    id: int
    image_path: str
    bounding_box: BoundingBox
    label: Optional[Label] = None
    confidence: Optional[float] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    is_validated: bool = False
    validated_by: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_sample()

    def validate_sample(self):
        """Validate sample data"""
        if self.id < 0:
            raise ValueError("Sample ID must be non-negative")
        if not self.image_path:
            raise ValueError("Image path cannot be empty")
        if self.confidence is not None and (self.confidence < 0 or self.confidence > 1):
            raise ValueError("Confidence must be between 0 and 1")
        
    def validate(self, validator: str):
        """Mark sample as validated"""
        self.is_validated = True
        self.validated_by = validator
        self.updated_at = datetime.now()

    def update_prediction(self, label: Label, confidence: float):
        """Update prediction for sample"""
        self.label = label
        self.confidence = confidence
        self.updated_at = datetime.now() 