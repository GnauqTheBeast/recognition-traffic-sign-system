from abc import ABC, abstractmethod
from pathlib import Path

class TrafficSignStrategy(ABC):
    @abstractmethod
    def detect(self, image):
        pass

    @abstractmethod
    def classify(self, image):
        pass

    @abstractmethod
    def process_video(self, video_content: bytes, filename: str) -> Path:
        pass
