# Facial Emotion Recognition

## 1. Giới thiệu dự án

Facial Emotion Recognition là ứng dụng nhận diện cảm xúc khuôn mặt theo thời gian thực bằng webcam. Dự án sử dụng OpenCV để phát hiện khuôn mặt, mô hình deep learning để dự đoán cảm xúc, và giao diện Tkinter để người dùng thao tác trực quan.

Ứng dụng có thể nhận diện 7 nhóm cảm xúc:

- `angry`
- `disgust`
- `scared`
- `happy`
- `sad`
- `surprised`
- `neutral`

Sau khi nhận diện, chương trình có thể hiển thị xác suất từng cảm xúc, đưa ra gợi ý phù hợp và phát nhạc từ thư mục `music/` theo cảm xúc được phát hiện.

Một số thành phần chính của dự án:

```text
facial-emotion-recognition/
├── emotion.py                         # File chạy giao diện chính
├── live_emotion.py                    # Xử lý nhận diện cảm xúc realtime
├── recommender.py                     # Nội dung gợi ý theo cảm xúc
├── load_and_process.py                # Tải và tiền xử lý dữ liệu
├── train_emotion_classifier.py        # Huấn luyện mô hình
├── models/                            # Chứa mô hình đã huấn luyện
├── haarcascade_files/                 # File Haar Cascade phát hiện khuôn mặt
├── music/                             # Nhạc theo từng cảm xúc
├── data/                              # Dữ liệu train/validation
└── outputs/                           # Nơi lưu ảnh kết quả
```

## 2. Thiết lập dự án

Yêu cầu cơ bản:

- Python 3.10 trở lên
- Webcam hoạt động bình thường
- Hệ điều hành Windows được khuyến nghị
- VLC Player nếu muốn phát nhạc trực tiếp bằng `python-vlc`

Clone hoặc tải dự án về máy:

```powershell
git clone <URL_REPO>
cd facial-emotion-recognition
```

Tạo môi trường ảo:

```powershell
python -m venv .venv
```

Kích hoạt môi trường ảo trên PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn việc chạy script, có thể chạy lệnh sau trong phiên làm việc hiện tại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Cài đặt các thư viện cần thiết:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-min.txt
```

Nếu cần cài đầy đủ các phụ thuộc cũ của dự án, có thể dùng:

```powershell
python -m pip install -r requirements.txt
```

## 3. Biên dịch và chạy dự án

Dự án là ứng dụng Python nên không cần biên dịch như các ngôn ngữ C/C++/Java. Sau khi cài đặt thư viện, có thể chạy trực tiếp các file Python.

Kiểm tra nhanh các file quan trọng trước khi chạy:

- `models/_mini_XCEPTION.102-0.66.hdf5`: mô hình nhận diện cảm xúc
- `haarcascade_files/haarcascade_frontalface_default.xml`: file phát hiện khuôn mặt
- `music/*.mp3`: nhạc ứng với từng cảm xúc
- `outputs/`: thư mục lưu ảnh kết quả

Nếu muốn huấn luyện lại mô hình, chạy:

```powershell
python .\train_emotion_classifier.py
```

Nếu chỉ muốn chạy ứng dụng nhận diện đã có model sẵn, không cần huấn luyện lại.

## 4. Chạy dự án

Chạy ứng dụng giao diện chính:

```powershell
python .\emotion.py
```

Sau khi chạy, cửa sổ giao diện sẽ hiển thị nút bắt đầu nhận diện cảm xúc. Khi nhận diện, ứng dụng sẽ mở webcam, hiển thị khuôn mặt được phát hiện và cập nhật kết quả cảm xúc theo thời gian thực.

Có thể chạy file xử lý realtime riêng nếu muốn kiểm tra nhanh phần nhận diện:

```powershell
python .\live_emotion.py
```

## 5. Cách sử dụng

1. Mở terminal tại thư mục `facial-emotion-recognition`.
2. Kích hoạt môi trường ảo nếu đã tạo:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Chạy ứng dụng:

```powershell
python .\emotion.py
```

4. Trong giao diện, bấm nút `Start - Nhan dien cam xuc`.
5. Đặt khuôn mặt trước webcam để chương trình nhận diện.
6. Xem kết quả cảm xúc và xác suất hiển thị trên cửa sổ chương trình.
7. Nếu cảm xúc được nhận diện ổn định, ứng dụng sẽ cập nhật phần gợi ý và có thể phát nhạc từ thư mục `music/`.
8. Bấm phím `q` trong cửa sổ webcam để dừng nhận diện.
9. Ảnh kết quả sau khi dừng sẽ được lưu tại:

```text
outputs/output.jpg
```

Một số lỗi thường gặp:

- Nếu không mở được webcam, hãy đóng các ứng dụng đang dùng camera như Zoom, Meet, Teams hoặc OBS.
- Nếu thiếu thư viện, cài lại bằng `python -m pip install -r requirements-min.txt`.
- Nếu không phát được nhạc, kiểm tra VLC Player, gói `python-vlc` và các file `.mp3` trong thư mục `music/`.
