import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split

def load_detection_data(data_dir, batch_size=32):
    """
    Tải dữ liệu cho mô hình phát hiện theo từng batch
    """
    # Lấy danh sách tất cả các file ảnh
    image_files = [f for f in os.listdir(data_dir) if f.endswith('.jpg')]
    total_samples = len(image_files)
    
    print(f"Tìm thấy {total_samples} ảnh trong thư mục {data_dir}")
    
    # Generator để load từng batch
    def data_generator():
        while True:
            # Shuffle files
            np.random.shuffle(image_files)
            
            for i in range(0, len(image_files), batch_size):
                batch_files = image_files[i:i + batch_size]
                batch_images = []
                batch_boxes = []
                
                for img_file in batch_files:
                    try:
                        # Đọc ảnh
                        img_path = os.path.join(data_dir, img_file)
                        img = cv2.imread(img_path)
                        if img is None:
                            print(f"Không thể đọc ảnh: {img_path}")
                            continue
                            
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (224, 224))
                        img = img.astype(np.float32) / 255.0  # Chuyển sang float32
                        
                        # Đọc file chú thích
                        txt_path = os.path.join(data_dir, img_file.replace('.jpg', '.txt'))
                        if not os.path.exists(txt_path):
                            print(f"Không tìm thấy file chú thích: {txt_path}")
                            continue
                            
                        with open(txt_path, 'r') as f:
                            box = list(map(float, f.read().strip().split()[1:]))  # Bỏ qua class_id
                        
                        batch_images.append(img)
                        batch_boxes.append(box)
                        
                    except Exception as e:
                        print(f"Lỗi khi xử lý ảnh {img_file}: {str(e)}")
                        continue
                
                if batch_images:  # Kiểm tra nếu batch không rỗng
                    yield np.array(batch_images, dtype=np.float32), np.array(batch_boxes, dtype=np.float32)
    
    return data_generator(), total_samples

def create_detection_model():
    """
    Tạo mô hình CNN để phát hiện vùng chứa biển báo
    """
    model = models.Sequential([
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Block 4
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Dense layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dense(4)  # 4 giá trị cho bounding box (x, y, width, height)
    ])
    
    return model

def train_detection_model():
    # Cấu hình
    batch_size = 16  # Giảm batch size xuống
    epochs = 10
    
    # Tạo thư mục lưu model nếu chưa tồn tại
    os.makedirs('models', exist_ok=True)
    
    # Tải dữ liệu
    print("Đang tải dữ liệu...")
    train_gen, total_samples = load_detection_data('data/train', batch_size)
    
    # Tính số bước mỗi epoch
    steps_per_epoch = total_samples // batch_size
    
    # Tạo mô hình
    print("Đang tạo mô hình...")
    model = create_detection_model()
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    # Callbacks
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            'models/detection_model.h5',
            save_best_only=True,
            monitor='loss'
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor='loss',
            patience=5
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='loss',
            factor=0.2,
            patience=3
        )
    ]
    
    # Huấn luyện
    print("Bắt đầu huấn luyện...")
    try:
        history = model.fit(
            train_gen,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            callbacks=callbacks
        )
        print("Huấn luyện hoàn tất!")
        return history
    except Exception as e:
        print(f"Lỗi trong quá trình huấn luyện: {str(e)}")
        return None

if __name__ == '__main__':
    train_detection_model() 