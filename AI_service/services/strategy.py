from abc import ABC, abstractmethod

class TrafficSignStrategy(ABC):
    @abstractmethod
    def detect(self, image):
        pass

    @abstractmethod
    def classify(self, image):
        pass
