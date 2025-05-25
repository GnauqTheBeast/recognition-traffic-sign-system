# services/context.py

from .strategy import TrafficSignStrategy

class TrafficSignModelContext:
    def __init__(self, strategy: TrafficSignStrategy):
        self.strategy = strategy

    def detect_sign(self, image):
        return self.strategy.detect(image)

    def classify_sign(self, image):
        return self.strategy.classify(image)
