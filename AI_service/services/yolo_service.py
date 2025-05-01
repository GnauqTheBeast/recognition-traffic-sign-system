import numpy as np
import time
from utils.image_utils import resize_image_for_yolo
from config.settings import YOLO_MODEL_PATH, MAX_IMAGE_SIZE

yolo_model = None
yolo_model_loaded = False

def load_yolo_model():
    """Tải model YOLO"""
    global yolo_model, yolo_model_loaded
    if yolo_model_loaded:
        return
    
    try:
        print("Đang tải mô hình YOLO trên CPU...")
        start_time = time.time()
        
        import torch
        torch.set_num_threads(4) 
        
        try:
            from ultralytics import YOLO
            print("Đã import thành công ultralytics")
        except Exception as import_error:
            print(f"Lỗi khi import ultralytics: {str(import_error)}")
            raise
        
        try:
            yolo_model = YOLO(YOLO_MODEL_PATH, task='detect')
            print("Model YOLO được tạo thành công")
            
            yolo_model.to('cpu')
            print("Đã chuyển model sang CPU")
            
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
        raise

def detect_sign_yolo(image: np.ndarray) -> tuple:
    """Phát hiện biển báo bằng YOLO"""
    try:
        resized_image, scale = resize_image_for_yolo(image, MAX_IMAGE_SIZE)
        
        results = yolo_model.predict(
            source=resized_image, 
            conf=0.25,  # Ngưỡng confidence
            iou=0.45,   # Ngưỡng IOU cho NMS
            verbose=False,
            device='cpu'  # Đảm bảo chạy trên CPU
        )
        
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

def classify_sign_yolo(image: np.ndarray) -> tuple:
    """Phân loại biển báo bằng YOLO"""
    try:
        # Resize ảnh để tối ưu hiệu suất
        resized_image, _ = resize_image_for_yolo(image, MAX_IMAGE_SIZE)
        
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
