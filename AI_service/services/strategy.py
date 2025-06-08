from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np

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

    @abstractmethod
    def process_stream(self, frame: np.ndarray):
        pass
