import tensorflow as tf
import cv2
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

def load_models():
    """
    Tải các mô hình đã huấn luyện
    """
    print("Đang tải mô hình phát hiện...")
    detection_model = tf.keras.models.load_model('models/detection_model.h5')
    
    print("Đang tải mô hình phân loại...")
    classification_model = tf.keras.models.load_model('models/classification_model.h5')
    
    return detection_model, classification_model

def preprocess_image(img_path, target_size=(224, 224)):
    """
    Tiền xử lý ảnh đầu vào
    """
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {img_path}")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype(np.float32) / 255.0
    return img

def detect_signs(img, detection_model):
    """
    Phát hiện vùng chứa biển báo trong ảnh
    """
    # Thêm chiều batch
    img_batch = np.expand_dims(img, axis=0)
    
    # Dự đoán
    pred = detection_model.predict(img_batch)[0]
    
    # Chuyển đổi tọa độ tương đối thành tọa độ pixel
    h, w = img.shape[:2]
    x_center, y_center, width, height = pred
    
    x1 = int((x_center - width/2) * w)
    y1 = int((y_center - height/2) * h)
    x2 = int((x_center + width/2) * w)
    y2 = int((y_center + height/2) * h)
    
    return (x1, y1, x2, y2)

def classify_sign(img_crop, classification_model):
    """
    Phân loại biển báo
    """
    # Resize ảnh về kích thước đầu vào của mô hình phân loại
    img_crop = cv2.resize(img_crop, (64, 64))
    img_crop = np.expand_dims(img_crop, axis=0)
    
    # Dự đoán
    pred = classification_model.predict(img_crop)[0]
    class_id = np.argmax(pred)
    confidence = pred[class_id]
    
    return class_id, confidence

def visualize_results(img, detection_box, class_id, confidence):
    """
    Hiển thị kết quả
    """
    # Vẽ bounding box
    x1, y1, x2, y2 = detection_box
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Thêm thông tin phân loại
    text = f"Class: {class_id}, Confidence: {confidence:.2f}"
    cv2.putText(img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Hiển thị ảnh
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def test_image(img_path):
    """
    Test một ảnh với cả hai mô hình
    """
    # Tải mô hình
    detection_model, classification_model = load_models()
    
    # Tiền xử lý ảnh
    img = preprocess_image(img_path)
    
    # Phát hiện biển báo
    detection_box = detect_signs(img, detection_model)
    
    # Cắt ảnh theo bounding box
    x1, y1, x2, y2 = detection_box
    img_crop = img[y1:y2, x1:x2]
    
    # Phân loại biển báo
    class_id, confidence = classify_sign(img_crop, classification_model)
    
    # Hiển thị kết quả
    visualize_results(img, detection_box, class_id, confidence)

if __name__ == '__main__':
    # Test với ảnh từ thư mục test
    test_dir = 'data/test'
    if os.path.exists(test_dir):
        for img_file in os.listdir(test_dir):
            if img_file.endswith(('.jpg', '.png')):
                img_path = os.path.join(test_dir, img_file)
                print(f"\nĐang test ảnh: {img_file}")
                test_image(img_path)
    else:
        print("Thư mục test không tồn tại. Vui lòng tạo thư mục 'data/test' và thêm ảnh test vào đó.") 