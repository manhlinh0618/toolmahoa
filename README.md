# ToolMaHoa — Công cụ Mã hóa & Giải mã

Dự án môn học: Công cụ mã hóa văn bản và file với giao diện đồ họa (Tkinter).

## Cấu trúc thư mục

```
ToolMaHoa/
├── main.py               # Điểm khởi động
├── controller.py         # Controller điều phối logic
├── gui/
│   ├── main_window.py    # Cửa sổ chính + Menu + Notebook
│   ├── text_tab.py       # Tab mã hóa văn bản
│   └── file_tab.py       # Tab mã hóa file
├── crypto/
│   ├── aes_cipher.py     # AES: encrypt/decrypt text & file
│   ├── caesar_cipher.py  # Caesar cipher
│   ├── md5_hash.py       # MD5 hash
│   └── key_manager.py    # Quản lý khóa AES
├── services/
│   ├── file_service.py   # Đọc/ghi file
│   ├── clipboard_service.py  # Clipboard
│   └── benchmark.py      # Benchmark tốc độ AES
└── assets/               # Icon, logo
```

## Yêu cầu

- Python 3.11+
- PyCryptodome

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```

## Tính năng

| Tính năng              | Chi tiết                              |
|------------------------|---------------------------------------|
| AES mã hóa văn bản     | CBC, ECB, CFB, CTR, GCM              |
| AES mã hóa file        | CBC, ECB, CFB, CTR, GCM              |
| Key size               | AES-128, AES-192, AES-256             |
| Caesar cipher          | Mã hóa / Giải mã, Brute-force        |
| MD5 hash               | Văn bản & File                        |
| Key Manager            | Sinh, lưu, tải, xóa file .key        |
| Benchmark              | So sánh tốc độ AES trên 1 MB         |
| Clipboard              | Copy key, copy kết quả               |

## Kiến trúc

```
GUI (Tkinter) → Controller → Algorithms (AES, Caesar, MD5)
                           → Services (File, Clipboard)
```

Thiết kế theo mô hình phân lớp:
- **GUI**: Chỉ hiển thị, không chứa logic.
- **Controller**: Nhận sự kiện, gọi đúng hàm.
- **Crypto**: Thuật toán thuần túy.
- **Services**: Tiện ích (file, clipboard, benchmark).
