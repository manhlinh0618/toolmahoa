"""
Module File Service
-------------------
Xử lý đọc / ghi file thuần túy.
KHÔNG chứa thuật toán mã hóa.
"""

import os


def read_file(file_path: str) -> bytes:
    """Đọc file và trả về nội dung dạng bytes.

    Args:
        file_path: Đường dẫn tới file.

    Returns:
        Nội dung file dạng bytes.

    Raises:
        FileNotFoundError: Nếu file không tồn tại.
        IOError: Nếu không đọc được file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    with open(file_path, "rb") as f:
        return f.read()


def read_text_file(file_path: str, encoding: str = "utf-8") -> str:
    """Đọc file text và trả về chuỗi.

    Args:
        file_path: Đường dẫn tới file text.
        encoding: Encoding (mặc định utf-8).

    Returns:
        Nội dung file dạng chuỗi.
    """
    with open(file_path, "r", encoding=encoding) as f:
        return f.read()


def write_file(file_path: str, data: bytes) -> None:
    """Ghi bytes vào file.

    Tạo các thư mục cha nếu chưa tồn tại.

    Args:
        file_path: Đường dẫn file đích.
        data: Dữ liệu bytes cần ghi.
    """
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(data)


def write_text_file(file_path: str, text: str, encoding: str = "utf-8") -> None:
    """Ghi chuỗi vào file text.

    Args:
        file_path: Đường dẫn file đích.
        text: Nội dung chuỗi cần ghi.
        encoding: Encoding (mặc định utf-8).
    """
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding=encoding) as f:
        f.write(text)


def get_extension(file_path: str) -> str:
    """Lấy phần mở rộng của file (chữ thường, không có dấu chấm).

    Args:
        file_path: Đường dẫn hoặc tên file.

    Returns:
        Phần mở rộng (ví dụ: 'txt', 'enc', 'png').
    """
    _, ext = os.path.splitext(file_path)
    return ext.lstrip(".").lower()


def get_enc_output_path(original_path: str) -> str:
    """Tạo đường dẫn file .enc từ file gốc.

    Args:
        original_path: Đường dẫn file gốc.

    Returns:
        Đường dẫn file kết quả với đuôi .enc.

    Example:
        >>> get_enc_output_path("documents/report.pdf")
        'documents/report.pdf.enc'
    """
    return original_path + ".enc"


def get_dec_output_path(enc_path: str) -> str:
    """Tạo đường dẫn file đã giải mã từ file .enc.

    Bỏ đuôi .enc để khôi phục tên file gốc.

    Args:
        enc_path: Đường dẫn file .enc.

    Returns:
        Đường dẫn file sau giải mã.

    Example:
        >>> get_dec_output_path("documents/report.pdf.enc")
        'documents/report.pdf'
    """
    if enc_path.endswith(".enc"):
        return enc_path[:-4]
    return enc_path + ".dec"


def get_file_size(file_path: str) -> int:
    """Lấy kích thước file tính theo bytes.

    Args:
        file_path: Đường dẫn tới file.

    Returns:
        Kích thước file (bytes).
    """
    return os.path.getsize(file_path)


def format_file_size(size_bytes: int) -> str:
    """Định dạng kích thước file thành chuỗi dễ đọc.

    Args:
        size_bytes: Kích thước tính bằng bytes.

    Returns:
        Chuỗi đã định dạng (B, KB, MB, GB).
    """
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
