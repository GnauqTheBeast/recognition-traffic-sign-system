from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Dict, Optional
from config.settings import ModelType, SIGN_NAMES
from models.schemas import DetectionResponse, ClassificationResponse, ModelStatusResponse, ModelTypeRequest
from services.model_service import detectTrafficSignService, classifyTrafficSignService, get_current_model, set_model, get_model_status
from utils.image_utils import load_image
import os

router = APIRouter()

@router.post("/set-model")
async def setModel(request: ModelTypeRequest):
    try:
        current_model = set_model(request.model_type)
        return {"status": "success", "current_model": current_model}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể thay đổi model sang {request.model_type}: {str(e)}"
        )
    
@router.get("/current-model")
async def getCurrentModel():
    """Lấy thông tin model đang sử dụng"""
    return {"current_model": get_current_model()}

@router.post("/detect", response_model=DetectionResponse)
async def detectTrafficSign(
    file: UploadFile = File(...),
    model_type: Optional[ModelType] = Query(None, description="Model to use: cnn or yolo")
):
    """Nhận diện biển báo với model tùy chọn"""
    try:
        image = load_image(file)
        
        (x1, y1, x2, y2), used_model = detectTrafficSignService(image, model_type)

        return {
            "bounding_box": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            },
            "model_used": used_model
        }
    except Exception as e:
        print(f"Lỗi khi detect: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phát hiện: {str(e)}")

@router.post("/classify", response_model=ClassificationResponse)
async def classifyTrafficSign(
    file: UploadFile = File(...),
    model_type: Optional[ModelType] = Query(None, description="Model to use: cnn or yolo")
):
    """Phân loại biển báo với model tùy chọn"""
    try:
        image = load_image(file)
        
        (class_id, confidence), used_model = classifyTrafficSignService(image, model_type)

        return {
            "class_id": class_id,
            "sign_name": SIGN_NAMES.get(class_id, "Unknown"),
            "confidence": confidence,
            "model_used": used_model
        }
    except Exception as e:
        print(f"Lỗi khi classify: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phân loại: {str(e)}")

@router.get("/classes", response_model=Dict[int, str])
async def get_classes():
    """Trả về danh sách nhãn biển báo"""
    return SIGN_NAMES

IMAGE_DIR = "./images"

@router.get("/images/{filename}")
async def get_image(filename: str):
    """Trả về ảnh từ server theo tên tệp"""
    file_path = os.path.join(IMAGE_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Ảnh không tồn tại")
    
    return FileResponse(file_path, media_type="image/jpeg")

@router.get("/models", response_model=ModelStatusResponse)
async def getAllModels():
    """Trả về danh sách model có sẵn"""
    return get_model_status()
