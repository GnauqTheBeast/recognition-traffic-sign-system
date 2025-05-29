import numpy as np
import time
from utils.image_utils import resize_image_for_yolo
from config.settings import SIGN_NAMES, YOLO_MODEL_PATH, MAX_IMAGE_SIZE
from models import BoundingBox, ClassificationResult, Label, ClassificationResponse
from services.label_service import LabelService
import cv2
from typing import Generator, Tuple
from pathlib import Path
import uuid
from fastapi import HTTPException
import shutil

class YOLOService:
    _instance = None
    _model = None
    _model_loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YOLOService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._model_loaded:
            self._load_model()
        self.label_service = LabelService()
        self.valid_extensions = ('.mp4', '.avi', '.mov')
        self.output_dir = Path("output_videos")
        self.output_dir.mkdir(exist_ok=True)

    def _load_model(self):
        """Load YOLO model using singleton pattern"""
        if self._model_loaded:
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
                self._model = YOLO(YOLO_MODEL_PATH, task='detect')
                print("Model YOLO được tạo thành công")
                
                self._model.to('cpu')
                print("Đã chuyển model sang CPU")
                
                # Test inference
                dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
                _ = self._model.predict(dummy_image, verbose=False)
                print("Đã thực hiện inference thử nghiệm thành công")
                
                self._model_loaded = True
                print(f"Đã tải mô hình YOLO thành công! Thời gian: {time.time() - start_time:.2f} giây")
            except Exception as model_error:
                print(f"Lỗi khi khởi tạo model YOLO: {str(model_error)}")
                raise
        except Exception as e:
            print(f"Lỗi chung khi tải mô hình YOLO: {str(e)}")
            raise

    def detect_sign(self, image: np.ndarray) -> BoundingBox:
        """Detect traffic sign in image and return BoundingBox object"""
        try:
            resized_image, scale = resize_image_for_yolo(image, MAX_IMAGE_SIZE)
            
            results = self._model.predict(
                source=resized_image, 
                conf=0.25,
                iou=0.45,
                verbose=False,
                device='cpu'
            )
            
            if len(results) > 0 and len(results[0].boxes) > 0:
                boxes = results[0].boxes
                box = boxes[0]
                
                xyxy = box.xyxy[0].cpu().numpy()
                
                x1, y1, x2, y2 = xyxy
                if scale != 1.0:
                    x1 = int(x1 / scale)
                    y1 = int(y1 / scale)
                    x2 = int(x2 / scale)
                    y2 = int(y2 / scale)
                
                return BoundingBox(x1=int(x1), y1=int(y1), x2=int(x2), y2=int(y2))
            else:
                return self._get_default_box(image)
        except Exception as e:
            print(f"Lỗi khi phát hiện với YOLO: {str(e)}")
            return self._get_default_box(image)

    def classify_sign(self, image: np.ndarray) -> ClassificationResult:
        """
        Classify traffic sign in image
        Returns:
            ClassificationResult: Object containing class_id and confidence
        """
        try:
            resized_image, _ = resize_image_for_yolo(image, MAX_IMAGE_SIZE)
            
            results = self._model.predict(
                source=resized_image, 
                conf=0.25,
                verbose=False,
                device='cpu'
            )
            
            if len(results) > 0 and len(results[0].boxes) > 0:
                boxes = results[0].boxes
                box = boxes[0]
                
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
            
                label = Label(
                    id=class_id,
                    name=SIGN_NAMES.get(class_id, "Unknown")
                )

                return ClassificationResult(
                    label=label,
                    confidence=confidence
                )
            else:
                return ClassificationResult(
                    label=Label(id=0, name="Unknown"),
                    confidence=0.0
                )
        except Exception as e:
            print(f"Lỗi khi phân loại với YOLO: {str(e)}")
            return ClassificationResult(
                label=Label(id=0, name="Unknown"),
                confidence=0.0
            )

    def _get_default_box(self, image: np.ndarray) -> BoundingBox:
        """Get default bounding box for image as BoundingBox object"""
        h, w = image.shape[:2]
        x1, y1 = int(w * 0.25), int(h * 0.25)
        x2, y2 = int(w * 0.75), int(h * 0.75)
        return BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)

    def process_video(self, video_content: bytes, filename: str) -> Path:
        if not filename.lower().endswith(self.valid_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng tệp không hợp lệ. Các định dạng được hỗ trợ: {self.valid_extensions}"
            )

        temp_file = Path(f"temp_{uuid.uuid4()}_{filename}")
        output_name = f"detect_{uuid.uuid4().hex[:8]}"
        
        try:
            # Tạo thư mục output nếu chưa tồn tại
            self.output_dir.mkdir(exist_ok=True)
            
            # Lưu video input vào file tạm
            with temp_file.open("wb") as buffer:
                buffer.write(video_content)
            
            print(f"Tệp tạm đã được tạo: {temp_file}")

            results = self._model.predict(
                source=str(temp_file),
                save=True,
                project=str(self.output_dir),
                name=output_name,
                stream=True,
                conf=0.25,
                show_labels=False,
                show_conf=False,
                line_width=2,
                save_txt=False
            )

            # Process all frames
            results_list = list(results)
            print(f"Đã xử lý {len(results_list)} khung hình")

            # Tìm file output trong thư mục predict/output_name
            predict_dir = self.output_dir / output_name
            video_files = [
                f for f in predict_dir.glob("*")
                if f.is_file() and f.suffix.lower() in self.valid_extensions
            ]
            
            if not video_files:
                raise HTTPException(
                    status_code=500,
                    detail="Không tạo được tệp video đầu ra"
                )

            output_path = video_files[0]
            final_output = self.output_dir / f"result_{filename}"
            
            # Copy file kết quả ra thư mục output chính
            shutil.copy2(output_path, final_output)
            
            # Cleanup thư mục predict và file tạm
            shutil.rmtree(predict_dir)
            temp_file.unlink()
            
            return final_output

        except Exception as e:
            # Cleanup trong trường hợp lỗi
            if temp_file.exists():
                temp_file.unlink()
            if 'predict_dir' in locals() and predict_dir.exists():
                shutil.rmtree(predict_dir)
            raise e

    def process_video_batch(self, video_array: np.ndarray, batch_size: int = 4):
        """Process video in batches for better performance"""
        cap = cv2.VideoCapture()
        cap.open(video_array)

        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frames.append(frame)
            if len(frames) == batch_size:
                # Xử lý batch frames
                results = self._model.predict(
                    source=frames,
                    conf=0.25,
                    iou=0.45,
                    verbose=False
                )
                
                # Xử lý và yield từng frame với kết quả
                for frame, result in zip(frames, results):
                    processed_frame = self._process_detection_result(frame, result)
                    _, buffer = cv2.imencode('.jpg', processed_frame)
                    yield buffer.tobytes()
                
                frames = []

        cap.release()
