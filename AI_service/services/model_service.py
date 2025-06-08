# services/model_service.py

from config.settings import ModelType
from .context import TrafficSignModelContext
from .cnn_strategy import CNNStrategy
from .yolo_strategy import YOLOStrategy
from models import BoundingBox, ClassificationResult
from ultralytics import YOLO
from pathlib import Path
import numpy as np

class ModelService:
    _instance = None
    _current_model_type = ModelType.YOLO
    _strategies = {
        ModelType.YOLO: None,
        ModelType.CNN: None
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._strategies[ModelType.YOLO]:
            self._initialize_strategies()
        self.yolo_model = None

    def _initialize_strategies(self):
        """Initialize strategy instances"""
        self._strategies[ModelType.YOLO] = YOLOStrategy()
        self._strategies[ModelType.CNN] = CNNStrategy()

    @property
    def current_model_type(self):
        """Get current model type"""
        return self._current_model_type

    @current_model_type.setter
    def current_model_type(self, model_type: ModelType):
        """Set current model type"""
        if model_type not in ModelType:
            raise ValueError(f"Unsupported model type: {model_type}")
        self._current_model_type = model_type

    def get_model_status(self):
        """Get status of all models"""
        return {
            "available_models": [model.value for model in ModelType],
            "current_model": self._current_model_type.value,
            "cnn_loaded": self._strategies[ModelType.CNN] is not None,
            "yolo_loaded": self._strategies[ModelType.YOLO] is not None
        }

    def get_strategy(self, model_type: ModelType):
        """Get strategy instance for specified model type"""
        if model_type not in self._strategies:
            raise ValueError(f"Unsupported model type: {model_type}")
        return self._strategies[model_type]

    def detect_traffic_sign(self, image, model_type: ModelType = None):
        """Detect traffic sign using specified model type"""
        if model_type is None:
            model_type = self._current_model_type
        
        strategy = self.get_strategy(model_type)
        context = TrafficSignModelContext(strategy)
        return context.detect_sign(image)

    def classify_traffic_sign(self, image, model_type: ModelType = None):
        """Classify traffic sign using specified model type"""
        if model_type is None:
            model_type = self._current_model_type
        
        strategy = self.get_strategy(model_type)
        context = TrafficSignModelContext(strategy)
        return context.classify_sign(image)

    def process_video(self, video_content: bytes, filename: str, model_type: ModelType = ModelType.YOLO) -> Path:
        self.current_model_type = model_type
        return self._strategies[model_type].process_video(video_content, filename)

    def process_stream(self, frame: np.ndarray, model_type: ModelType = ModelType.YOLO):
        self.current_model_type = model_type
        return self._strategies[model_type].process_stream(frame)