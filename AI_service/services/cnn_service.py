import numpy as np
import tensorflow as tf
import time
from utils.image_utils import preprocess_image_cnn
from config.settings import CNN_DETECTION_MODEL_PATH, CNN_CLASSIFICATION_MODEL_PATH, SIGN_NAMES
from models import BoundingBox, ClassificationResult, Label

class CNNService:
    _instance = None
    _detection_model = None
    _classification_model = None
    _models_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CNNService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._models_loaded:
            self._load_models()

    def _load_models(self):
        """Load CNN models using singleton pattern"""
        if self._models_loaded:
            return
        
        try:
            print("Đang tải mô hình CNN...")
            start_time = time.time()
            
            # Load detection model
            self._detection_model = tf.keras.models.load_model(
                CNN_DETECTION_MODEL_PATH,
                custom_objects={
                    'mse': tf.keras.losses.MeanSquaredError(),
                    'mean_squared_error': tf.keras.losses.MeanSquaredError(),
                    'mae': tf.keras.metrics.MeanAbsoluteError()
                },
                compile=False
            )
            self._detection_model.compile(
                optimizer='adam',
                loss=tf.keras.losses.MeanSquaredError(),
                metrics=[tf.keras.metrics.MeanAbsoluteError()]
            )

            # Load classification model
            self._classification_model = tf.keras.models.load_model(
                CNN_CLASSIFICATION_MODEL_PATH
            )
            
            self._models_loaded = True
            print(f"Đã tải mô hình CNN thành công! Thời gian: {time.time() - start_time:.2f} giây")
        except Exception as e:
            print(f"Lỗi khi tải mô hình CNN: {str(e)}")
            raise

    def detect_sign(self, image: np.ndarray) -> BoundingBox:
        """Detect traffic sign in image and return BoundingBox object"""
        try:
            img = preprocess_image_cnn(image)
            img_batch = np.expand_dims(img, axis=0)
            pred = self._detection_model.predict(img_batch)[0]

            h, w = image.shape[:2]
            x, y, width, height = pred
            x1 = int(x * w)
            y1 = int(y * h)
            x2 = int((x + width) * w)
            y2 = int((y + height) * h)
            return BoundingBox(
                x1=int(x1),
                y1=int(y1),
                x2=int(x2),
                y2=int(y2)
            )
        except Exception as e:
            print(f"Lỗi khi phát hiện với CNN: {str(e)}")
            return self._get_default_box(image)

    def classify_sign(self, image: np.ndarray) -> ClassificationResult:
        """Classify traffic sign and return ClassificationResult object"""
        try:
            img = preprocess_image_cnn(image, target_size=(64, 64))
            img_batch = np.expand_dims(img, axis=0)
            pred = self._classification_model.predict(img_batch)[0]
            class_id = int(np.argmax(pred))
            confidence = float(pred[class_id])
            
            # Tạo Label object
            label = Label(
                id=class_id,
                name=SIGN_NAMES.get(class_id, "Unknown")
            )
            
            return ClassificationResult(
                label=label,
                confidence=float(confidence)
            )
        except Exception as e:
            print(f"Lỗi khi phân loại với CNN: {str(e)}")
            # Tạo default label khi có lỗi
            default_label = Label(
                id=0,
                name="Unknown"
            )
            return ClassificationResult(
                label=default_label,
                confidence=0.0
            )

    def _get_default_box(self, image: np.ndarray) -> BoundingBox:
        """Get default bounding box as BoundingBox object"""
        h, w = image.shape[:2]
        x1, y1 = int(w * 0.25), int(h * 0.25)
        x2, y2 = int(w * 0.75), int(h * 0.75)
        return BoundingBox(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )

cnn_detection_model = None
cnn_classification_model = None
cnn_models_loaded = False

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

def detect_sign_cnn(image: np.ndarray) -> BoundingBox:
    img = preprocess_image_cnn(image)
    img_batch = np.expand_dims(img, axis=0)
    pred = cnn_detection_model.predict(img_batch)[0]

    h, w = image.shape[:2]
    x, y, width, height = pred
    x1 = int(x * w)
    y1 = int(y * h)
    x2 = int((x + width) * w)
    y2 = int((y + height) * h)
    return BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)

def classify_sign_cnn(image: np.ndarray) -> ClassificationResult:
    img = preprocess_image_cnn(image, target_size=(64, 64))
    img_batch = np.expand_dims(img, axis=0)
    pred = cnn_classification_model.predict(img_batch)[0]
    class_id = int(np.argmax(pred))
    confidence = float(pred[class_id])
    
    # Tạo Label object
    label = Label(
        id=class_id,
        name=SIGN_NAMES.get(class_id, "Unknown")
    )
    
    return ClassificationResult(
        label=label,
        confidence=confidence
    )
