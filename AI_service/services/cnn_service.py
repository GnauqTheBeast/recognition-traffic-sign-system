import numpy as np
import tensorflow as tf
import time
from utils.image_utils import preprocess_image_cnn
from config.settings import CNN_DETECTION_MODEL_PATH, CNN_CLASSIFICATION_MODEL_PATH

# Biến toàn cục cho model
cnn_detection_model = None
cnn_classification_model = None
cnn_models_loaded = False

def load_cnn_models():
    """Tải các model CNN"""
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

def detect_sign_cnn(image: np.ndarray) -> tuple:
    """Phát hiện biển báo bằng CNN"""
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

def classify_sign_cnn(image: np.ndarray) -> tuple:
    """Phân loại biển báo bằng CNN"""
    img = preprocess_image_cnn(image, target_size=(64, 64))
    img_batch = np.expand_dims(img, axis=0)
    pred = cnn_classification_model.predict(img_batch)[0]
    class_id = int(np.argmax(pred))
    confidence = float(pred[class_id])
    return class_id, confidence
