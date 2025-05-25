from pydantic import BaseModel
from typing import Optional

class Label(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    code: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_label()

    def validate_label(self):
        """Validate label data"""
        if self.id < 0:
            raise ValueError("Label ID must be non-negative")
        if not self.name:
            raise ValueError("Label name cannot be empty")
        if len(self.name) > 100:
            raise ValueError("Label name too long") 