import cv2
import numpy as np
from typing import Generator

def create_video_writer(cap: cv2.VideoCapture, output_path: str) -> cv2.VideoWriter:
    """Create video writer with same parameters as input video"""
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def video_frame_generator(video_bytes: bytes) -> Generator[np.ndarray, None, None]:
    """Generate frames from video bytes"""
    video_array = np.frombuffer(video_bytes, np.uint8)
    cap = cv2.VideoCapture()
    cap.open(video_array)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
    finally:
        cap.release() 