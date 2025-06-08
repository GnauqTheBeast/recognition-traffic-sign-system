# services/cnn_strategy.py

from .strategy import TrafficSignStrategy
from .cnn_service import CNNService
from models import BoundingBox, ClassificationResult
from pathlib import Path
import numpy as np

class CNNStrategy(TrafficSignStrategy):
    def __init__(self):
        self.cnn_service = CNNService()

    def detect(self, image):
        return self.cnn_service.detect_sign(image), "cnn"

    def classify(self, image):
        return self.cnn_service.classify_sign(image), "cnn"

    def process_video(self, video_content: bytes, filename: str) -> Path:
        raise NotImplementedError("CNN model không hỗ trợ xử lý video")
    
    def process_stream(self, frame: np.ndarray):
        raise NotImplementedError("Stream processing not implemented for CNN strategy")

