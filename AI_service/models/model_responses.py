from typing import List
from config.settings import ModelType
from pydantic import BaseModel

class ModelStatusResponse(BaseModel):
    available_models: List[str]
    current_model: ModelType
    cnn_loaded: bool
    yolo_loaded: bool

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_status()

    def validate_status(self):
        """Validate model status"""
        if not self.available_models:
            raise ValueError("Available models list cannot be empty")
        if not self.current_model:
            raise ValueError("Current model must be specified")

class ModelChangeResponse(BaseModel):
    status: str
    current_model: ModelType

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_change()

    def validate_change(self):
        """Validate model change response"""
        if not self.status:
            raise ValueError("Status cannot be empty")
        if not self.current_model:
            raise ValueError("Current model must be specified") 