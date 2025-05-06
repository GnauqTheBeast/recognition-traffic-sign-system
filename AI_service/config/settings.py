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
# SIGN_NAMES = {
#     0: "Giới hạn tốc độ (20km/h)", 1: "Giới hạn tốc độ (30km/h)", 2: "Giới hạn tốc độ (50km/h)",
#     3: "Giới hạn tốc độ (60km/h)", 4: "Giới hạn tốc độ (70km/h)", 5: "Giới hạn tốc độ (80km/h)",
#     6: "Hết giới hạn tốc độ (80km/h)", 7: "Giới hạn tốc độ (100km/h)", 8: "Giới hạn tốc độ (120km/h)",
#     9: "Cấm vượt", 10: "Cấm xe trên 3.5 tấn vượt",
#     11: "Ưu tiên ở ngã tư tiếp theo", 12: "Đường ưu tiên", 13: "Nhường đường",
#     14: "Dừng lại", 15: "Cấm xe", 16: "Cấm xe trên 3.5 tấn",
#     17: "Cấm vào", 18: "Cảnh báo chung", 19: "Khúc cua nguy hiểm bên trái",
#     20: "Khúc cua nguy hiểm bên phải", 21: "Hai khúc cua liên tiếp", 22: "Đường gồ ghề",
#     23: "Đường trơn", 24: "Đường hẹp bên phải", 25: "Công trường",
#     26: "Tín hiệu giao thông", 27: "Người đi bộ", 28: "Trẻ em băng qua đường",
#     29: "Xe đạp băng qua", 30: "Cẩn thận băng/tuyết", 31: "Động vật hoang dã băng qua",
#     32: "Hết mọi giới hạn tốc độ và cấm vượt", 33: "Rẽ phải phía trước",
#     34: "Rẽ trái phía trước", 35: "Chỉ được đi thẳng", 36: "Đi thẳng hoặc rẽ phải",
#     37: "Đi thẳng hoặc rẽ trái", 38: "Giữ bên phải", 39: "Giữ bên trái",
#     40: "Bắt buộc đi vòng xuyến", 41: "Hết cấm vượt",
#     42: "Hết cấm xe trên 3.5 tấn vượt"
# }

# Mapping các nhãn GTSRB (0–42) sang nhóm chức năng
SIGN_NAMES = {
    0: 'Cảnh báo', 1: 'Cảnh báo', 2: 'Cảnh báo', 3: 'Cảnh báo', 4: 'Cảnh báo',
    5: 'Cấm', 6: 'Cấm', 7: 'Cấm', 8: 'Cấm', 9: 'Cấm', 10: 'Cấm', 11: 'Cấm', 12: 'Cấm', 13: 'Cấm', 14: 'Cấm', 15: 'Cấm',
    16: 'Cấm', 17: 'Cấm', 18: 'Cấm',
    19: 'Hạn chế', 20: 'Hạn chế', 21: 'Hạn chế', 22: 'Hạn chế',
    23: 'Chỉ dẫn', 24: 'Chỉ dẫn', 25: 'Chỉ dẫn', 26: 'Chỉ dẫn', 27: 'Chỉ dẫn', 28: 'Chỉ dẫn', 29: 'Chỉ dẫn',
    30: 'Chỉ dẫn', 31: 'Chỉ dẫn', 32: 'Chỉ dẫn', 33: 'Chỉ dẫn', 34: 'Chỉ dẫn',
    35: 'Cảnh báo', 36: 'Cảnh báo', 37: 'Cảnh báo', 38: 'Cảnh báo',
    39: 'Chỉ dẫn', 40: 'Chỉ dẫn', 41: 'Cảnh báo', 42: 'Cảnh báo'
}

                   