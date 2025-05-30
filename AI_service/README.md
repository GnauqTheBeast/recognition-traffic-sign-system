# Hệ Thống Nhận dạng Biển Báo Giao Thông

Dự án này xây dựng một hệ thống Nhận dạng biển báo giao thông sử dụng Deep Learning, bao gồm hai mô hình chính:
1. Mô hình phát hiện vùng chứa biển báo
2. Mô hình phân loại biển báo

## Các Loại Biển Báo Được Nhận Dạng

Hệ thống có thể Nhận dạng 43 loại biển báo giao thông theo tiêu chuẩn GTSRB (German Traffic Sign Recognition Benchmark):

### 1. Biển Báo Cấm (0-9)
- 0: Giới hạn tốc độ (20km/h)
- 1: Giới hạn tốc độ (30km/h)
- 2: Giới hạn tốc độ (50km/h)
- 3: Giới hạn tốc độ (60km/h)
- 4: Giới hạn tốc độ (70km/h)
- 5: Giới hạn tốc độ (80km/h)
- 6: Hết giới hạn tốc độ (80km/h)
- 7: Giới hạn tốc độ (100km/h)
- 8: Giới hạn tốc độ (120km/h)
- 9: Cấm vượt

### 2. Biển Báo Nguy Hiểm (10-19)
- 10: Cấm vượt xe tải
- 11: Giao nhau với đường ưu tiên
- 12: Đường ưu tiên
- 13: Nhường đường
- 14: Dừng lại
- 15: Cấm xe cộ
- 16: Cấm xe tải
- 17: Cấm đi ngược chiều
- 18: Nguy hiểm chung
- 19: Đường cong nguy hiểm bên trái

### 3. Biển Báo Chỉ Dẫn (20-29)
- 20: Đường cong nguy hiểm bên phải
- 21: Đường cong kép
- 22: Đường gồ ghề
- 23: Đường trơn trượt
- 24: Đường hẹp bên phải
- 25: Công trường
- 26: Đèn tín hiệu giao thông
- 27: Người đi bộ
- 28: Trẻ em qua đường
- 29: Xe đạp qua đường

### 4. Biển Báo Hiệu Lệnh (30-42)
- 30: Cẩn thận tuyết/băng
- 31: Động vật hoang dã
- 32: Hết giới hạn tốc độ
- 33: Rẽ phải bắt buộc
- 34: Rẽ trái bắt buộc
- 35: Đi thẳng bắt buộc
- 36: Đi thẳng hoặc rẽ phải
- 37: Đi thẳng hoặc rẽ trái
- 38: Giữ bên phải
- 39: Giữ bên trái
- 40: Vòng xuyến bắt buộc
- 41: Hết cấm vượt
- 42: Hết cấm vượt xe tải

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- TensorFlow 2.x
- OpenCV
- NumPy
- Pillow
- Matplotlib

## Cài Đặt

1. Tạo môi trường ảo (khuyến nghị):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Cấu Trúc Dự Án

```
.
├── data/
│   ├── train/           # Dữ liệu huấn luyện
│   ├── test/            # Dữ liệu kiểm tra
│   └── classification/  # Dữ liệu phân loại
├── models/
│   ├── detection_model.h5      # Mô hình phát hiện
│   └── classification_model.h5 # Mô hình phân loại
├── process_kaggle_data.py      # Xử lý dữ liệu từ Kaggle
├── train_detection_model.py    # Huấn luyện mô hình phát hiện
├── train_classification_model.py # Huấn luyện mô hình phân loại
├── client_app.py               # Ứng dụng giao diện người dùng
└── requirements.txt            # Danh sách thư viện
```

## Hướng Dẫn Sử Dụng

### 1. Chuẩn Bị Dữ Liệu

- Tải dữ liệu từ Kaggle (GTSRB dataset)
- Chạy script xử lý dữ liệu:
```bash
python process_kaggle_data.py
```

### 2. Huấn Luyện Mô Hình

1. Huấn luyện mô hình phát hiện:
```bash
python train_detection_model.py
```

2. Huấn luyện mô hình phân loại:
```bash
python train_classification_model.py
```

### 3. Sử Dụng Ứng Dụng

Chạy ứng dụng giao diện:
```bash
python client_app.py
```

Các chức năng chính:
- Chọn ảnh từ máy tính
- Nhận dạng biển báo trong ảnh
- Hiển thị kết quả với bounding box và thông tin phân loại

## Mô Tả Mô Hình

### Mô Hình Phát Hiện
- Kiến trúc CNN với 4 khối convolutional
- Input: ảnh 224x224x3
- Output: tọa độ bounding box (x, y, width, height)
- Loss function: Mean Squared Error

### Mô Hình Phân Loại
- Kiến trúc CNN với 3 khối convolutional
- Input: ảnh 64x64x3
- Output: xác suất cho mỗi lớp biển báo
- Loss function: Categorical Crossentropy

## Xử Lý Lỗi

1. Lỗi tải mô hình:
   - Kiểm tra phiên bản TensorFlow
   - Đảm bảo file mô hình tồn tại trong thư mục models/
   - Kiểm tra quyền truy cập file

2. Lỗi bộ nhớ:
   - Giảm batch size
   - Giảm kích thước ảnh đầu vào
   - Sử dụng generator thay vì load toàn bộ dữ liệu

## Đóng Góp

Mọi đóng góp cho dự án đều được hoan nghênh. Vui lòng tạo pull request hoặc issue để thảo luận.

## Giấy Phép

Dự án này được phân phối dưới giấy phép MIT. 