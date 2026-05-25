# Facial Emotion Recognition - AI Recommender

Ứng dụng nhận diện cảm xúc khuôn mặt realtime bằng webcam, sau đó gợi ý nhạc, hoạt động, câu nói và phim phù hợp.

## Tính năng chính
- Nhận diện 7 cảm xúc: `angry`, `disgust`, `scared`, `happy`, `sad`, `surprised`, `neutral`.
- Hiển thị cửa sổ webcam + cửa sổ xác suất cảm xúc (`Emotion Probabilities`).
- Mở **cửa sổ phản hồi tiếng Việt riêng** và cập nhật realtime khi cảm xúc ổn định.
- Phát nhạc theo cảm xúc ngay trong lúc webcam đang chạy.
- Ảnh kết quả khi bấm `q` được lưu vào thư mục `outputs/output.jpg`.

## Cấu trúc thư mục quan trọng
```text
facial-emotion-recognition/
├─ emotion.py                          # GUI chính (Tkinter)
├─ live_emotion.py                     # Nhận diện realtime (OpenCV + model)
├─ recommender.py                      # Nội dung gợi ý
├─ models/_mini_XCEPTION.102-0.66.hdf5
├─ haarcascade_files/haarcascade_frontalface_default.xml
├─ emojis/
├─ music/
└─ outputs/                            # Tự tạo khi chạy
```

## Yêu cầu hệ thống
- Windows 10/11 (khuyến nghị, vì có `os.startfile` fallback phát nhạc).
- Python `3.12.x`.
- Webcam hoạt động bình thường.

## Hướng dẫn chạy từ đầu đến cuối

### 1. Clone project
```powershell
git clone <URL_REPO_CUA_BAN>
cd facial-emotion-recognition
```

### 2. Tạo virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script, chạy tạm lệnh này rồi activate lại:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Cài thư viện để chạy app
Khuyến nghị dùng file tối thiểu (đã test với code hiện tại):
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-min.txt
```

Lưu ý:
- `python-vlc` cần VLC Player đã cài trong máy để phát nhạc trực tiếp trong app.
- Nếu chưa có VLC, app sẽ fallback mở file mp3 bằng trình mặc định của Windows.

### 4. Chạy ứng dụng
```powershell
python .\emotion.py
```

### 5. Cách sử dụng
1. Bấm `Start - Nhan dien cam xuc`.
2. Webcam mở ra, đồng thời mở cửa sổ `Emotion Probabilities`.
3. Cửa sổ `Phản hồi tiếng Việt (Realtime)` sẽ cập nhật trả lời riêng ngay khi cảm xúc ổn định.
4. Bấm `q` trong cửa sổ webcam để thoát nhận diện.
5. Ảnh snapshot lưu tại: `outputs/output.jpg`.

## Xử lý lỗi thường gặp

### `ModuleNotFoundError: No module named 'PIL'`
```powershell
python -m pip install Pillow
```

### `ModuleNotFoundError: No module named 'keras'`
```powershell
python -m pip install tensorflow keras
```

### Không phát được nhạc
- Kiểm tra thư mục `music/` có đủ file `.mp3`.
- Cài VLC Player + `python-vlc`.
- Nếu vẫn lỗi, app sẽ cố mở nhạc bằng ứng dụng mặc định của Windows.

### Không mở được webcam
- Đóng ứng dụng khác đang chiếm camera (Zoom, Meet, Teams, OBS...).
- Kiểm tra quyền camera trong Windows Settings.

## Đẩy project sang repo Git mới

### Cách nhanh (đổi remote hiện tại sang repo mới)
```powershell
git remote rename origin old-origin
git remote add origin <URL_REPO_MOI>
git add .
git commit -m "Initial import: facial emotion recognition app"
git branch -M main
git push -u origin main
```

### Nếu muốn giữ repo cũ và thêm remote mới
```powershell
git remote add new-origin <URL_REPO_MOI>
git add .
git commit -m "Initial import: facial emotion recognition app"
git push -u new-origin main
```

## Ghi chú
- `requirements.txt` hiện là danh sách phụ thuộc cũ và rất lớn; để chạy nhanh, ưu tiên `requirements-min.txt`.
