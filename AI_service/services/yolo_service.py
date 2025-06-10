import numpy as np
import time
from utils.image_utils import resize_image_for_yolo
from utils.video_utils import reencode_video
from config.settings import SIGN_NAMES, YOLO_MODEL_PATH, MAX_IMAGE_SIZE
from models import BoundingBox, ClassificationResult, Label, ClassificationResponse
from services.label_service import LabelService
import cv2
from pathlib import Path
import uuid
from fastapi import HTTPException
import shutil
import asyncio

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
        self.frame_queue = asyncio.Queue(maxsize=10)
        self.latest_processed_frame = None
        self.is_processing = False
        self.model_service = None

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

            results_list = list(results)
            print(f"Đã xử lý {len(results_list)} khung hình")

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
            
            # Sử dụng trực tiếp hàm utils để re-encode
            try:
                reencode_video(output_path, final_output)
            except Exception as e:
                print(f"Warning: Could not re-encode video: {str(e)}")
                # Nếu encode thất bại, copy file gốc
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

    def set_model_service(self, model_service):
        self.model_service = model_service

    async def process_frame_queue(self):
        self.is_processing = True
        while self.is_processing:
            try:
                if not self.frame_queue.empty():
                    frame = await self.frame_queue.get()
                    
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    frame = cv2.resize(frame, (360, 480))
                    
                    # Resize frame for YOLO
                    resized_frame, _ = resize_image_for_yolo(frame, MAX_IMAGE_SIZE)
                    
                    # Process frame with YOLO
                    results = self._model.predict(
                        source=resized_frame,
                        conf=0.25,      # Confidence threshold
                        iou=0.45,       # NMS IoU threshold
                        verbose=False,
                        device='cpu'
                    )
                    
                    # Get first result
                    result = next(iter(results), None)
                    
                    if result is not None:
                        boxes = result.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            conf = box.conf[0]
                            cls_id = int(box.cls[0])
                            
                            cv2.rectangle(frame, 
                                        (int(x1), int(y1)), 
                                        (int(x2), int(y2)), 
                                        (0, 255, 0), 2)
                            
                            label = f"{SIGN_NAMES[cls_id]}: {conf:.2f}"
                            cv2.putText(frame, label, 
                                      (int(x1), int(y1) - 10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.5, (0, 255, 0), 2)

                    self.latest_processed_frame = frame
                    
                await asyncio.sleep(0.01)
            except Exception as e:
                print(f"Frame processing error: {str(e)}")
                continue

    async def process_rtsp_stream(self, rtsp_url: str):
        cap = None
        try:
            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_FPS, 15)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
            
            process_task = asyncio.create_task(self.process_frame_queue())
            
            error_count = 0
            max_errors = 5
            
            while True:
                try:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        error_count += 1
                        print(f"Frame read error: {error_count}")
                        if error_count > max_errors:
                            print("Too many errors, restarting capture...")
                            if cap is not None:
                                cap.release()
                            cap = cv2.VideoCapture(rtsp_url)
                            error_count = 0
                        await asyncio.sleep(0.1)
                        continue

                    error_count = 0

                    try:
                        self.frame_queue.put_nowait(frame.copy())
                    except asyncio.QueueFull:
                        pass

                    if self.latest_processed_frame is not None:
                        encode_param = [
                            cv2.IMWRITE_JPEG_QUALITY, 75,
                            cv2.IMWRITE_JPEG_OPTIMIZE, 1
                        ]
                        _, buffer = cv2.imencode('.jpg', self.latest_processed_frame, encode_param)
                        frame_bytes = buffer.tobytes()
                        
                        yield (b'--frame\r\n'
                              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    
                    await asyncio.sleep(0.03)

                except Exception as frame_error:
                    print(f"Frame processing error: {str(frame_error)}")
                    error_count += 1
                    if error_count > max_errors:
                        break

        except Exception as e:
            print(f"Stream processing error: {str(e)}")
            raise
        finally:
            self.is_processing = False
            if cap is not None:
                cap.release()
