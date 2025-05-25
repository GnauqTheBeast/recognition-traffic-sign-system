# services/cnn_strategy.py

from .strategy import TrafficSignStrategy
from .cnn_service import CNNService
from models import BoundingBox, ClassificationResult

class CNNStrategy(TrafficSignStrategy):
    def __init__(self):
        self.cnn_service = CNNService()

    def detect(self, image):
        return self.cnn_service.detect_sign(image), "cnn"

    def classify(self, image):
        return self.cnn_service.classify_sign(image), "cnn"
