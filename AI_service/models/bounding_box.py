from pydantic import BaseModel

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_coordinates()

    def validate_coordinates(self):
        """Validate bounding box coordinates"""
        if self.x2 < self.x1 or self.y2 < self.y1:
            raise ValueError("Invalid bounding box coordinates: x2/y2 must be greater than x1/y1")
        if self.x1 < 0 or self.y1 < 0:
            raise ValueError("Invalid bounding box coordinates: coordinates must be non-negative")

    def to_tuple(self):
        return (self.x1, self.y1, self.x2, self.y2)

    @classmethod
    def from_tuple(cls, coords: tuple):
        x1, y1, x2, y2 = coords
        return cls(x1=x1, y1=y1, x2=x2, y2=y2) 