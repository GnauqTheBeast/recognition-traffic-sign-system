from enum import Enum

class LabelType(str, Enum):
    WARNING = "Cảnh báo"
    PROHIBITED = "Cấm"
    INFORMATION = "Thông tin" 