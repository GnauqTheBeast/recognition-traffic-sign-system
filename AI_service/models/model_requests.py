from config.settings import ModelType
from .base_model import BaseModel

class ModelTypeRequest(BaseModel):
    model_type: ModelType 