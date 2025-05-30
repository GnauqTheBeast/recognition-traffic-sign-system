import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from typing import Dict, Optional
from pathlib import Path
from config.settings import ModelType, SIGN_NAMES
from models import (
    DetectionResponse,
    ClassificationResponse,
    ModelStatusResponse,
)
from services.model_service import ModelService
from utils.image_utils import load_image
import os
import cv2
import io
import numpy as np
from fastapi.staticfiles import StaticFiles
from models.video_detection_responses import VideoDetectionResponse
from utils.video_utils import reencode_video

class TrafficSignController:
    def __init__(self):
        self.model_service = ModelService()
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """Setup all routes for the controller"""
        self.router.get("/current-model")(self.get_current_model)
        self.router.post("/detect", response_model=DetectionResponse)(self.detect_traffic_sign)
        self.router.post("/classify", response_model=ClassificationResponse)(self.classify_traffic_sign)
        self.router.get("/classes", response_model=Dict[int, str])(self.get_classes)
        self.router.get("/images/{filename}")(self.get_image)
        self.router.get("/models", response_model=ModelStatusResponse)(self.get_all_models)
        self.router.post("/detect-video")(self.detect_video)
        self.router.post("/detect-video-stream")(self.detect_video_stream)
        self.router.delete("/videos/{filename}")(self.delete_video)
        self.router.get("/videos/{filename}")(self.serve_video)

    async def get_current_model(self):
        """Get current model type"""
        return {"current_model": self.model_service.get_current_model()}

    async def detect_traffic_sign(
        self,
        file: UploadFile = File(...),
        model_type: Optional[ModelType] = Query(None, description="Model to use: cnn or yolo")
    ) -> DetectionResponse:
        """Detect traffic sign in image"""
        try:
            image = load_image(file)
            detection_result, model_used = self.model_service.detect_traffic_sign(image, model_type)
            
            return DetectionResponse(
                bounding_box=detection_result,  
                model_used=model_used
            )
        except Exception as e:
            print(f"Lỗi khi detect: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi phát hiện: {str(e)}")

    async def classify_traffic_sign(
        self,
        file: UploadFile = File(...),
        model_type: Optional[ModelType] = Query(None)
    ):
        try:
            image = load_image(file)
            result, model_used = self.model_service.classify_traffic_sign(image, model_type)
            
            return result.to_response(
                model_used=model_used,
                sample_id=None
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_classes(self):
        """Get all traffic sign classes"""
        return SIGN_NAMES

    async def get_image(self, filename: str):
        """Get image by filename"""
        file_path = os.path.join("./images", filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Ảnh không tồn tại")
        
        return FileResponse(file_path, media_type="image/jpeg")

    async def get_all_models(self):
        """Get status of all models"""
        return self.model_service.get_model_status()

    async def detect_video(
        self,
        file: UploadFile = File(...),
        model_type: Optional[ModelType] = Query(ModelType.YOLO)
    ) -> VideoDetectionResponse:
        try:
            # Generate unique filename
            original_name = Path(file.filename).stem
            unique_id = str(uuid.uuid4())[:8] 
            unique_filename = f"{original_name}_{unique_id}.mp4"
            
            content = await file.read()
            # Xử lý video detection (đã bao gồm re-encode trong service)
            output_path = self.model_service.process_video(
                video_content=content,
                filename=unique_filename, 
                model_type=model_type
            )
            
            video_filename = output_path.name
            video_url = f"/api/videos/{video_filename}"
            
            # Lấy thông tin video
            cap = cv2.VideoCapture(str(output_path))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            return VideoDetectionResponse(
                success=True,
                video_url=video_url,
                filename=video_filename,
                model_used=model_type,
                frame_count=frame_count,
                duration=duration
            )
            
        except Exception as e:
            return VideoDetectionResponse(
                success=False,
                video_url="",
                filename="",
                model_used=model_type,
                error_message=str(e)
            )

    async def detect_video_stream(
        self,
        file: UploadFile = File(...),
        model_type: Optional[ModelType] = Query(ModelType.YOLO)
    ):
        """Stream detection results frame by frame"""
        try:
            video_bytes = await file.read()
            return StreamingResponse(
                self._stream_video(video_bytes, model_type),
                media_type="multipart/x-mixed-replace; boundary=frame"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_video(self, filename: str):
        try:
            video_path = Path("output_videos") / filename
            if video_path.exists():
                video_path.unlink()
                return {"success": True, "message": f"Đã xóa video {filename}"}
            return {"success": False, "message": "Video không tồn tại"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Không thể xóa video: {str(e)}")

    async def serve_video(self, filename: str):
        """Serve video file"""
        video_path = Path("output_videos") / filename
        if not video_path.exists():
            raise HTTPException(status_code=404, detail="Video not found")
        
        headers = {
            'Accept-Ranges': 'bytes',
            'Content-Disposition': f'inline; filename={filename}',
            'Cache-Control': 'public, max-age=3600',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
        
        return FileResponse(
            path=str(video_path),
            media_type="video/mp4",
            headers=headers,
            filename=filename,
            method='GET'  # Chỉ định rõ method
        )

traffic_sign_controller = TrafficSignController()
router = traffic_sign_controller.router
