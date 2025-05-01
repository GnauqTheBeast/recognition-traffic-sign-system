import cv2
import numpy as np
import io
from PIL import Image
from fastapi import UploadFile

def load_image(file: UploadFile) -> np.ndarray:
    """Đọc ảnh từ UploadFile"""
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    image = np.array(image)

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    return image

# def save_uploaded_image(image: np.ndarray, filename: str) -> str:
#     """Lưu ảnh vào thư mục và trả về đường dẫn"""
#     # Đảm bảo thư mục tồn tại
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
#     # Đường dẫn đầy đủ đến file
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
    
#     # Lưu ảnh
#     cv2.imwrite(file_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
#     # Trả về đường dẫn tương đối
#     return file_path

def resize_image_for_yolo(image: np.ndarray, max_size: int = 640) -> tuple:
    """Thay đổi kích thước ảnh để tối ưu hiệu suất, trả về ảnh đã resize và tỷ lệ"""
    h, w = image.shape[:2]
    
    # Lưu tỷ lệ gốc
    scale = 1.0
    
    # Nếu ảnh quá lớn, resize để tăng tốc độ
    if max(h, w) > max_size:
        if h > w:
            new_h = max_size
            new_w = int(w * (max_size / h))
            scale = max_size / h
        else:
            new_w = max_size
            new_h = int(h * (max_size / w))
            scale = max_size / w
        
        resized_image = cv2.resize(image, (new_w, new_h))
        return resized_image, scale
    
    return image, scale

def preprocess_image_cnn(image: np.ndarray, target_size: tuple = (224, 224)) -> np.ndarray:
    """Tiền xử lý ảnh cho CNN"""
    image = cv2.resize(image, target_size)
    image = image.astype(np.float32) / 255.0
    return image
