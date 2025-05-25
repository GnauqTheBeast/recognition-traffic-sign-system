# services/yolo_strategy.py

from .strategy import TrafficSignStrategy
from .yolo_service import YOLOService

class YOLOStrategy(TrafficSignStrategy):
    def __init__(self):
        self.yolo_service = YOLOService()

    def detect(self, image):
        return self.yolo_service.detect_sign(image), "yolo"

    def classify(self, image):
        return self.yolo_service.classify_sign(image), "yolo"
