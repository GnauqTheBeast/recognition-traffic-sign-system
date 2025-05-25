from typing import Dict, Optional
from models.label import Label
from models.label_type import LabelType
from config.settings import SIGN_NAMES

class LabelService:
    _instance = None
    _labels: Dict[int, Label] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LabelService, cls).__new__(cls)
            cls._instance._initialize_labels()
        return cls._instance

    def _initialize_labels(self):
        """Khởi tạo các label từ SIGN_NAMES"""
        for class_id, label_type in SIGN_NAMES.items():
            self._labels[class_id] = Label(
                id=class_id,
                name=label_type,
                code=f"SIGN_{class_id}"
            )

    def get_label(self, class_id: int) -> Optional[Label]:
        """Lấy label theo class_id"""
        return self._labels.get(class_id)

    def get_all_labels(self) -> Dict[int, Label]:
        """Lấy tất cả labels"""
        return self._labels 