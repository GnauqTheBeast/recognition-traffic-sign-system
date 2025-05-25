from pydantic import BaseModel
from typing import Optional
from config.settings import ModelType
from .base_model import BaseResponseModel
from .bounding_box import BoundingBox

class DetectionResponse(BaseModel):
    bounding_box: BoundingBox
    model_used: ModelType
    sample_id: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_response()

    def validate_response(self):
        """Validate detection response"""
        if not isinstance(self.bounding_box, BoundingBox):
            raise ValueError("Invalid bounding box type")
        if not self.model_used:
            raise ValueError("Model type must be specified")

class DetectionResponse(BaseResponseModel):
    bounding_box: BoundingBox
    model_used: ModelType 