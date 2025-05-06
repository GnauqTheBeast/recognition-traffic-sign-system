import numpy as np
from config.settings import ModelType
from services.cnn_service import load_cnn_models, detect_sign_cnn, classify_sign_cnn, cnn_models_loaded
from services.yolo_service import load_yolo_model, detect_sign_yolo, classify_sign_yolo, yolo_model_loaded

# Biến toàn cục
current_model_type = ModelType.CNN

def get_model_status():
    """Lấy trạng thái các model"""
    return {
        "available_models": [model.value for model in ModelType],
        "current_model": current_model_type,
        "cnn_loaded": cnn_models_loaded,
        "yolo_loaded": yolo_model_loaded
    }

def get_current_model():
    """Lấy model hiện tại (dùng nếu cần hiện mặc định)"""
    return current_model_type

def detectTrafficSignService(image: np.ndarray, model_type: ModelType = None):
    """Phát hiện biển báo với model được chọn"""
    use_model = model_type if model_type else current_model_type

    if use_model == ModelType.CNN:
        return detect_sign_cnn(image), use_model
    elif use_model == ModelType.YOLO:
        return detect_sign_yolo(image), use_model
    else:
        raise ValueError(f"Model không hợp lệ: {use_model}")

def classifyTrafficSignService(image: np.ndarray, model_type: ModelType = None):
    """Phân loại biển báo với model được chọn"""
    use_model = model_type if model_type else current_model_type

    if use_model == ModelType.CNN:
        return classify_sign_cnn(image), use_model
    elif use_model == ModelType.YOLO:
        return classify_sign_yolo(image), use_model
    else:
        raise ValueError(f"Model không hợp lệ: {use_model}")

def initialize_default_model():
    """Khởi tạo cả 2 model ngay từ đầu"""
    global current_model_type
    try:
        load_cnn_models()
    except Exception as e:
        print(f"[Lỗi] Không thể tải CNN: {str(e)}")

    try:
        load_yolo_model()
    except Exception as e:
        print(f"[Lỗi] Không thể tải YOLO: {str(e)}")
    