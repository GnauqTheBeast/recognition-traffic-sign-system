from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class ModelType(str, Enum):
    YOLO = "yolo"
    CNN = "cnn"

class VideoDetectionResponse(BaseModel):
    """Response model cho video detection API"""
    success: bool
    video_url: str
    filename: str
    model_used: ModelType
    processed_at: datetime = Field(default_factory=datetime.now)
    duration: Optional[float] = None  # Thời lượng video
    frame_count: Optional[int] = None  # Số frame đã xử lý
    error_message: Optional[str] = None

    def to_storage_format(self) -> dict:
        """Convert to format suitable for localStorage"""
        return {
            "id": int(self.processed_at.timestamp() * 1000),
            "name": f"detect_video_{self.processed_at.strftime('%Y%m%d%H%M%S')}",
            "videoPath": self.video_url,
            "date": self.processed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "modelUsed": self.model_used
        } 