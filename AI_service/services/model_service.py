import numpy as np
from config.settings import ModelType
from services.cnn_service import load_cnn_models, detect_sign_cnn, classify_sign_cnn, cnn_models_loaded
from services.yolo_service import load_yolo_model, detect_sign_yolo, classify_sign_yolo, yolo_model_loaded

# Biến toàn cục
current_model_type = ModelType.CNN

def get_current_model():
    """Lấy model hiện tại"""
    return current_model_type

def set_model(model_type: ModelType):
    """Thay đổi model sử dụng"""
    global current_model_type
    
    if model_type == ModelType.CNN and not cnn_models_loaded:
        load_cnn_models()
    elif model_type == ModelType.YOLO and not yolo_model_loaded:
        load_yolo_model()
    
    current_model_type = model_type
    return current_model_type

def detectTrafficSignService(image: np.ndarray, model_type: ModelType = None):
    """Phát hiện biển báo với model tùy chọn"""
    use_model = model_type if model_type else current_model_type
    
    if use_model == ModelType.CNN:
        if not cnn_models_loaded:
            load_cnn_models()
        return detect_sign_cnn(image), use_model
    else:  
        if not yolo_model_loaded:
            load_yolo_model()
        return detect_sign_yolo(image), use_model

def classifyTrafficSignService(image: np.ndarray, model_type: ModelType = None):
    """Phân loại biển báo với model tùy chọn"""
    use_model = model_type if model_type else current_model_type
    
    if use_model == ModelType.CNN:
        if not cnn_models_loaded:
            load_cnn_models()
        return classify_sign_cnn(image), use_model
    else:  # YOLO
        if not yolo_model_loaded:
            load_yolo_model()
        return classify_sign_yolo(image), use_model

def get_model_status():
    """Lấy trạng thái các model"""
    return {
        "available_models": [model.value for model in ModelType],
        "current_model": current_model_type,
        "cnn_loaded": cnn_models_loaded,
        "yolo_loaded": yolo_model_loaded
    }

def initialize_default_model():
    """Khởi tạo model mặc định khi ứng dụng khởi động"""
    global current_model_type
    try:
        if current_model_type == ModelType.CNN:
            load_cnn_models()
        else:
            load_yolo_model()
    except Exception as e:
        print(f"Lỗi khi tải model ban đầu: {str(e)}")
        if current_model_type == ModelType.YOLO:
            current_model_type = ModelType.CNN
            try:
                load_cnn_models()
            except Exception as inner_e:
                print(f"Cũng không thể tải CNN: {str(inner_e)}")
