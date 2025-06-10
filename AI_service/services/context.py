# services/context.py

from .strategy import TrafficSignStrategy

class TrafficSignModelContext:
    def __init__(self, strategy: TrafficSignStrategy):
        self.strategy = strategy

    def detect_sign(self, image):
        return self.strategy.detect(image)

    def classify_sign(self, image):
        return self.strategy.classify(image)
    
    def process_video(self, video_content: bytes, filename: str):
        return self.strategy.process_video(video_content, filename)
    
    def process_rtsp_stream(self, rtsp_url: str):
        return self.strategy.process_rtsp_stream(rtsp_url)
    