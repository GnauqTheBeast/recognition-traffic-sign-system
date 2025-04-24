from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io
from PIL import Image
import uvicorn
from typing import Dict
import tensorflow as tf

app = FastAPI(
    title="Traffic Sign Recognition API",
    description="API for detecting and classifying traffic signs in images",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
try:
    detection_model = tf.keras.models.load_model(
        'models/detection_model.keras',
        custom_objects={
            'mse': tf.keras.losses.MeanSquaredError(),
            'mean_squared_error': tf.keras.losses.MeanSquaredError(),
            'mae': tf.keras.metrics.MeanAbsoluteError()
        },
        compile=False
    )
    detection_model.compile(optimizer='adam',
                            loss=tf.keras.losses.MeanSquaredError(),
                            metrics=[tf.keras.metrics.MeanAbsoluteError()])

    classification_model = tf.keras.models.load_model('models/classification_model.keras')
    print("Đã tải mô hình thành công!")
except Exception as e:
    print(f"Lỗi khi tải mô hình: {str(e)}")
    raise

# Danh sách nhãn
# SIGN_NAMES = {
#     0: "Speed limit (20km/h)", 1: "Speed limit (30km/h)", 2: "Speed limit (50km/h)",
#     3: "Speed limit (60km/h)", 4: "Speed limit (70km/h)", 5: "Speed limit (80km/h)",
#     6: "End of speed limit (80km/h)", 7: "Speed limit (100km/h)", 8: "Speed limit (120km/h)",
#     9: "No passing", 10: "No passing for vehicles over 3.5 metric tons",
#     11: "Right-of-way at the next intersection", 12: "Priority road", 13: "Yield",
#     14: "Stop", 15: "No vehicles", 16: "Vehicles over 3.5 metric tons prohibited",
#     17: "No entry", 18: "General caution", 19: "Dangerous curve to the left",
#     20: "Dangerous curve to the right", 21: "Double curve", 22: "Bumpy road",
#     23: "Slippery road", 24: "Road narrows on the right", 25: "Road work",
#     26: "Traffic signals", 27: "Pedestrians", 28: "Children crossing",
#     29: "Bicycles crossing", 30: "Beware of ice/snow", 31: "Wild animals crossing",
#     32: "End of all speed and passing limits", 33: "Turn right ahead",
#     34: "Turn left ahead", 35: "Ahead only", 36: "Go straight or right",
#     37: "Go straight or left", 38: "Keep right", 39: "Keep left",
#     40: "Roundabout mandatory", 41: "End of no passing",
#     42: "End of no passing by vehicles over 3.5 metric tons"
# }

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


def preprocess_image(image: np.ndarray, target_size: tuple = (224, 224)) -> np.ndarray:
    image = cv2.resize(image, target_size)
    image = image.astype(np.float32) / 255.0
    return image

def detect_sign(image: np.ndarray) -> tuple:
    img = preprocess_image(image)
    img_batch = np.expand_dims(img, axis=0)
    pred = detection_model.predict(img_batch)[0]

    h, w = image.shape[:2]
    x, y, width, height = pred
    x1 = int(x * w)
    y1 = int(y * h)
    x2 = int((x + width) * w)
    y2 = int((y + height) * h)
    return (x1, y1, x2, y2)

def classify_sign(image: np.ndarray) -> tuple:
    img = preprocess_image(image, target_size=(64, 64))
    img_batch = np.expand_dims(img, axis=0)
    pred = classification_model.predict(img_batch)[0]
    class_id = int(np.argmax(pred))
    confidence = float(pred[class_id])
    return class_id, confidence

def load_image(file: UploadFile) -> np.ndarray:
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    image = np.array(image)

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    return image

@app.post("/detect", response_model=Dict)
async def detect_endpoint(file: UploadFile = File(...)):
    """Chỉ nhận diện (detect) biển báo"""
    try:
        image = load_image(file)
        x1, y1, x2, y2 = detect_sign(image)

        return {
            "bounding_box": {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phát hiện: {str(e)}")

@app.post("/classify", response_model=Dict)
async def classify_endpoint(file: UploadFile = File(...)):
    """Chỉ phân loại (classify) biển báo - yêu cầu hình đã crop"""
    try:
        image = load_image(file)
        class_id, confidence = classify_sign(image)

        return {
            "class_id": class_id,
            "sign_name": SIGN_NAMES.get(class_id, "Unknown"),
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân loại: {str(e)}")

@app.get("/classes", response_model=Dict[int, str])
async def get_classes():
    """Trả về danh sách nhãn biển báo"""
    return SIGN_NAMES

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
