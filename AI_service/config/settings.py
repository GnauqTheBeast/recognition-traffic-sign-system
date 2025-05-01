import os
from enum import Enum

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["TF_FORCE_CPU_ALLOW_GROWTH"] = "true"

class ModelType(str, Enum):
    CNN = "cnn"
    YOLO = "yolo"

CNN_DETECTION_MODEL_PATH = 'models/detection_model.keras'
CNN_CLASSIFICATION_MODEL_PATH = 'models/classification_model.keras'
YOLO_MODEL_PATH = "models/best.pt"

MAX_IMAGE_SIZE = 640  # Kích thước tối đa cho xử lý YOLO trên CPU

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
