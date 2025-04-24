from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io
from PIL import Image
import uvicorn
from typing import Dict, List, Optional
import os
import time
import tensorflow as tf
from enum import Enum

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["TF_FORCE_CPU_ALLOW_GROWTH"] = "true"

# Thiết lập cho TensorFlow chỉ sử dụng CPU
tf.config.set_visible_devices([], 'GPU')

# Thiết lập cho chạy đa model
class ModelType(str, Enum):
    CNN = "cnn"
    YOLO = "yolo"

# Khởi tạo API
app = FastAPI(
    title="Traffic Sign Recognition API",
    description="API for detecting and classifying traffic signs with multiple model options",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_model_type = ModelType.CNN  # Mặc định sử dụng CNN

CNN_DETECTION_MODEL_PATH = 'models/detection_model.keras'
CNN_CLASSIFICATION_MODEL_PATH = 'models/classification_model.keras'
YOLO_MODEL_PATH = "models/best.pt"

# Thiết lập cho YOLO
MAX_IMAGE_SIZE = 640  # Kích thước tối đa cho xử lý YOLO trên CPU

# Load CNN models
cnn_detection_model = None
cnn_classification_model = None
yolo_model = None

# Cờ để biết model đã được tải hay chưa
cnn_models_loaded = False
yolo_model_loaded = False

# Danh sách nhãn
SIGN_NAMES = {
    0: "Giới hạn tốc độ (20km/h)", 1: "Giới hạn tốc độ (30km/h)", 2: "Giới hạn tốc độ (50km/h)",
    3: "Giới hạn tốc độ (60km/h)", 4: "Giới hạn tốc độ (70km/h)", 5: "Giới hạn tốc độ (80km/h)",
    6: "Hết giới hạn tốc độ (80km/h)", 7: "Giới hạn tốc độ (100km/h)", 8: "Giới hạn tốc độ (120km/h)",
    9: "Cấm vượt", 10: "Cấm xe trên 3.5 tấn vượt",
    11: "Ưu tiên ở ngã tư tiếp theo", 12: "Đường ưu tiên", 13: "Nhường đường",
    14: "Dừng lại", 15: "Cấm xe", 16: "Cấm xe trên 3.5 tấn",
    17: "Cấm vào", 18: "Cảnh báo chung", 19: "Khúc cua nguy hiểm bên trái",
    20: "Khúc cua nguy hiểm bên phải", 21: "Hai khúc cua liên tiếp", 22: "Đường gồ ghề",
    23: "Đường trơn", 24: "Đường hẹp bên phải", 25: "Công trường",
    26: "Tín hiệu giao thông", 27: "Người đi bộ", 28: "Trẻ em băng qua đường",
    29: "Xe đạp băng qua", 30: "Cẩn thận băng/tuyết", 31: "Động vật hoang dã băng qua",
    32: "Hết mọi giới hạn tốc độ và cấm vượt", 33: "Rẽ phải phía trước",
    34: "Rẽ trái phía trước", 35: "Chỉ được đi thẳng", 36: "Đi thẳng hoặc rẽ phải",
    37: "Đi thẳng hoặc rẽ trái", 38: "Giữ bên phải", 39: "Giữ bên trái",
    40: "Bắt buộc đi vòng xuyến", 41: "Hết cấm vượt",
    42: "Hết cấm xe trên 3.5 tấn vượt"
}

# Hàm load CNN models
def load_cnn_models():
    global cnn_detection_model, cnn_classification_model, cnn_models_loaded
    
    if cnn_models_loaded:
        return
    
    try:
        print("Đang tải mô hình CNN...")
        start_time = time.time()
        
        cnn_detection_model = tf.keras.models.load_model(
            CNN_DETECTION_MODEL_PATH,
            custom_objects={
                'mse': tf.keras.losses.MeanSquaredError(),
                'mean_squared_error': tf.keras.losses.MeanSquaredError(),
                'mae': tf.keras.metrics.MeanAbsoluteError()
            },
            compile=False
        )
        cnn_detection_model.compile(optimizer='adam',
                                loss=tf.keras.losses.MeanSquaredError(),
                                metrics=[tf.keras.metrics.MeanAbsoluteError()])

        cnn_classification_model = tf.keras.models.load_model(CNN_CLASSIFICATION_MODEL_PATH)
        
        cnn_models_loaded = True
        print(f"Đã tải mô hình CNN thành công! Thời gian: {time.time() - start_time:.2f} giây")
    except Exception as e:
        print(f"Lỗi khi tải mô hình CNN: {str(e)}")
        raise

# Hàm load YOLO model - với xử lý ngoại lệ mạnh mẽ hơn
def load_yolo_model():
    global yolo_model, yolo_model_loaded
    print("=======================================================")
    if yolo_model_loaded:
        return
    
    try:
        print("Đang tải mô hình YOLO trên CPU...")
        start_time = time.time()
        
        import torch
        torch.set_num_threads(4)  # Giới hạn số luồng
        
        try:
            from ultralytics import YOLO
            print("Đã import thành công ultralytics")
        except Exception as import_error:
            print(f"Lỗi khi import ultralytics: {str(import_error)}")
            raise
        
        try:
            # Tải YOLO với device='cpu' rõ ràng
            yolo_model = YOLO(YOLO_MODEL_PATH, task='detect')
            print("Model YOLO được tạo thành công")
            
            # Thử áp dụng thiết lập CPU
            yolo_model.to('cpu')
            print("Đã chuyển model sang CPU")
            
            # Tiến hành inference thử nghiệm với ảnh trống
            dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
            _ = yolo_model.predict(dummy_image, verbose=False)
            print("Đã thực hiện inference thử nghiệm thành công")
            
            yolo_model_loaded = True
            print(f"Đã tải mô hình YOLO thành công! Thời gian: {time.time() - start_time:.2f} giây")
        except Exception as model_error:
            print(f"Lỗi khi khởi tạo model YOLO: {str(model_error)}")
            raise
    except Exception as e:
        print(f"Lỗi chung khi tải mô hình YOLO: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Không thể tải mô hình YOLO: {str(e)}")

# Hàm đọc ảnh từ UploadFile
def load_image(file: UploadFile) -> np.ndarray:
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    image = np.array(image)

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    return image

# Resize ảnh cho YOLO
def resize_image_for_yolo(image: np.ndarray) -> tuple:
    """Thay đổi kích thước ảnh để tối ưu hiệu suất, trả về ảnh đã resize và tỷ lệ"""
    h, w = image.shape[:2]
    
    # Lưu tỷ lệ gốc
    scale = 1.0
    
    # Nếu ảnh quá lớn, resize để tăng tốc độ
    if max(h, w) > MAX_IMAGE_SIZE:
        if h > w:
            new_h = MAX_IMAGE_SIZE
            new_w = int(w * (MAX_IMAGE_SIZE / h))
            scale = MAX_IMAGE_SIZE / h
        else:
            new_w = MAX_IMAGE_SIZE
            new_h = int(h * (MAX_IMAGE_SIZE / w))
            scale = MAX_IMAGE_SIZE / w
        
        resized_image = cv2.resize(image, (new_w, new_h))
        return resized_image, scale
    
    return image, scale

# Hàm tiền xử lý ảnh cho CNN
def preprocess_image_cnn(image: np.ndarray, target_size: tuple = (224, 224)) -> np.ndarray:
    image = cv2.resize(image, target_size)
    image = image.astype(np.float32) / 255.0
    return image

# Hàm detect sử dụng CNN
def detect_sign_cnn(image: np.ndarray) -> tuple:
    img = preprocess_image_cnn(image)
    img_batch = np.expand_dims(img, axis=0)
    pred = cnn_detection_model.predict(img_batch)[0]

    h, w = image.shape[:2]
    x, y, width, height = pred
    x1 = int(x * w)
    y1 = int(y * h)
    x2 = int((x + width) * w)
    y2 = int((y + height) * h)
    return (x1, y1, x2, y2)

# Hàm phân loại sử dụng CNN
def classify_sign_cnn(image: np.ndarray) -> tuple:
    img = preprocess_image_cnn(image, target_size=(64, 64))
    img_batch = np.expand_dims(img, axis=0)
    pred = cnn_classification_model.predict(img_batch)[0]
    class_id = int(np.argmax(pred))
    confidence = float(pred[class_id])
    return class_id, confidence

# Hàm detect sử dụng YOLO - với xử lý ngoại lệ tốt hơn
def detect_sign_yolo(image: np.ndarray) -> tuple:
    try:
        # Resize ảnh để tối ưu hiệu suất trên CPU
        resized_image, scale = resize_image_for_yolo(image)
        
        # Thực hiện detection
        results = yolo_model.predict(
            source=resized_image, 
            conf=0.25,  # Ngưỡng confidence
            iou=0.45,   # Ngưỡng IOU cho NMS
            verbose=False,
            device='cpu'  # Đảm bảo chạy trên CPU
        )
        
        # Xử lý kết quả - lấy box có confidence cao nhất
        if len(results) > 0 and len(results[0].boxes) > 0:
            # Lấy box đầu tiên có confidence cao nhất
            boxes = results[0].boxes
            box = boxes[0]  # Lấy box có confidence cao nhất
            
            # Lấy tọa độ và kích thước (x1, y1, x2, y2)
            xyxy = box.xyxy[0].cpu().numpy()  # Chuyển về numpy array
            
            # Scale lại về kích thước ảnh gốc
            x1, y1, x2, y2 = xyxy
            if scale != 1.0:
                x1 = int(x1 / scale)
                y1 = int(y1 / scale)
                x2 = int(x2 / scale)
                y2 = int(y2 / scale)
            
            return (int(x1), int(y1), int(x2), int(y2))
        else:
            # Nếu không phát hiện được biển báo, trả về box mặc định
            h, w = image.shape[:2]
            x1, y1 = int(w * 0.25), int(h * 0.25)
            x2, y2 = int(w * 0.75), int(h * 0.75)
            return (x1, y1, x2, y2)
    except Exception as e:
        print(f"Lỗi khi phát hiện với YOLO: {str(e)}")
        # Nếu YOLO gặp lỗi, trả về box mặc định
        h, w = image.shape[:2]
        x1, y1 = int(w * 0.25), int(h * 0.25)
        x2, y2 = int(w * 0.75), int(h * 0.75)
        return (x1, y1, x2, y2)

# Hàm phân loại sử dụng YOLO - với xử lý ngoại lệ tốt hơn
def classify_sign_yolo(image: np.ndarray) -> tuple:
    try:
        # Resize ảnh để tối ưu hiệu suất
        resized_image, _ = resize_image_for_yolo(image)
        
        # Thực hiện detection/classification
        results = yolo_model.predict(
            source=resized_image, 
            conf=0.25,
            verbose=False,
            device='cpu'  # Đảm bảo chạy trên CPU
        )
        
        if len(results) > 0 and len(results[0].boxes) > 0:
            # Lấy box đầu tiên có confidence cao nhất
            boxes = results[0].boxes
            box = boxes[0]
            
            # Lấy class_id và confidence
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            
            return class_id, confidence
        else:
            # Nếu không phát hiện được, trả về class không xác định
            return 0, 0.0  # Class_id 0 với confidence 0
    except Exception as e:
        print(f"Lỗi khi phân loại với YOLO: {str(e)}")
        # Nếu YOLO gặp lỗi, trả về class không xác định
        return 0, 0.0

@app.post("/set-model")
async def set_model(model_type: ModelType):
    global current_model_type
    
    try:
        if model_type == ModelType.CNN and not cnn_models_loaded:
            load_cnn_models()
        elif model_type == ModelType.YOLO and not yolo_model_loaded:
            load_yolo_model()
        
        current_model_type = model_type
        return {"status": "success", "current_model": current_model_type}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể thay đổi model sang {model_type}: {str(e)}"
        )

# Endpoint để lấy loại model hiện tại
@app.get("/current-model")
async def get_current_model():
    return {"current_model": current_model_type}

# Endpoint detect
@app.post("/detect", response_model=Dict)
async def detect_endpoint(
    file: UploadFile = File(...),
    model_type: Optional[ModelType] = Query(None, description="Model to use: cnn or yolo")
):
    """Nhận diện biển báo với model tùy chọn"""
    # Xác định model sẽ sử dụng
    use_model = model_type if model_type else current_model_type
    
    try:
        # Tải ảnh
        image = load_image(file)
        
        # Phát hiện với model được chọn
        if use_model == ModelType.CNN:
            # Đảm bảo model đã được tải
            if not cnn_models_loaded:
                load_cnn_models()
            
            x1, y1, x2, y2 = detect_sign_cnn(image)
        else:  # YOLO
            # Đảm bảo model đã được tải
            if not yolo_model_loaded:
                load_yolo_model()
            
            x1, y1, x2, y2 = detect_sign_yolo(image)

        return {
            "bounding_box": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            },
            "model_used": use_model
        }
    except Exception as e:
        print(f"Lỗi khi detect: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phát hiện: {str(e)}")

# Endpoint classify
@app.post("/classify", response_model=Dict)
async def classify_endpoint(
    file: UploadFile = File(...),
    model_type: Optional[ModelType] = Query(None, description="Model to use: cnn or yolo")
):
    """Phân loại biển báo với model tùy chọn"""
    # Xác định model sẽ sử dụng
    use_model = model_type if model_type else current_model_type
    
    try:
        # Tải ảnh
        image = load_image(file)
        
        # Phân loại với model được chọn
        if use_model == ModelType.CNN:
            # Đảm bảo model đã được tải
            if not cnn_models_loaded:
                load_cnn_models()
            
            class_id, confidence = classify_sign_cnn(image)
        else:  # YOLO
            # Đảm bảo model đã được tải
            if not yolo_model_loaded:
                load_yolo_model()
            
            class_id, confidence = classify_sign_yolo(image)

        return {
            "class_id": class_id,
            "sign_name": SIGN_NAMES.get(class_id, "Unknown"),
            "confidence": confidence,
            "model_used": use_model
        }
    except Exception as e:
        print(f"Lỗi khi classify: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi phân loại: {str(e)}")

@app.get("/classes", response_model=Dict[int, str])
async def get_classes():
    """Trả về danh sách nhãn biển báo"""
    return SIGN_NAMES

@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái API"""
    return {"status": "ok"}

@app.get("/models")
async def available_models():
    """Trả về danh sách model có sẵn"""
    models = {
        "available_models": [model.value for model in ModelType],
        "current_model": current_model_type,
        "cnn_loaded": cnn_models_loaded,
        "yolo_loaded": yolo_model_loaded
    }
    return models

# Tải model mặc định khi server khởi động
@app.on_event("startup")
async def startup_event():
    # Tải model mặc định (CNN)
    global current_model_type
    try:
        if current_model_type == ModelType.CNN:
            load_cnn_models()
        else:
            load_yolo_model()
    except Exception as e:
        print(f"Lỗi khi tải model ban đầu: {str(e)}")
        # Nếu thất bại với YOLO, chuyển sang CNN
        if current_model_type == ModelType.YOLO:
            current_model_type = ModelType.CNN
            try:
                load_cnn_models()
            except Exception as inner_e:
                print(f"Cũng không thể tải CNN: {str(inner_e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
