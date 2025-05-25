from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Dict, Optional
from config.settings import ModelType, SIGN_NAMES
from models import (
    DetectionResponse,
    ClassificationResponse,
    ModelStatusResponse,
)
from services.model_service import ModelService
from utils.image_utils import load_image
import os

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


traffic_sign_controller = TrafficSignController()
router = traffic_sign_controller.router
