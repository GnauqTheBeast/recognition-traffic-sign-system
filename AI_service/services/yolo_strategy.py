# services/yolo_strategy.py

from .strategy import TrafficSignStrategy
from .yolo_service import YOLOService
from pathlib import Path

class YOLOStrategy(TrafficSignStrategy):
    def __init__(self):
        self.yolo_service = YOLOService()

    def detect(self, image):
        return self.yolo_service.detect_sign(image), "yolo"

    def classify(self, image):
        return self.yolo_service.classify_sign(image), "yolo"

    def process_video(self, video_content: bytes, filename: str) -> Path:
        return self.yolo_service.process_video(video_content, filename)
