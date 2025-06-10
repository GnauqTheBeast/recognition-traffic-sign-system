from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np
from typing import AsyncGenerator

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
    async def process_rtsp_stream(self, rtsp_url: str):
        pass
