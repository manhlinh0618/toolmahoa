"""
Module MD5 Hash
---------------
Băm văn bản và file bằng thuật toán MD5.
Lưu ý: MD5 chỉ dùng để kiểm tra tính toàn vẹn dữ liệu,
        KHÔNG dùng để bảo mật mật khẩu.
"""

import hashlib


def hash_text(text: str, encoding: str = "utf-8") -> str:
    """Tính MD5 hash của văn bản.

    Args:
        text: Văn bản cần băm.
        encoding: Encoding để chuyển chuỗi sang bytes (mặc định utf-8).

    Returns:
        Chuỗi hex 32 ký tự (chữ thường).

    Example:
        >>> hash_text("hello")
        '5d41402abc4b2a76b9719d911017c592'
    """
    return hashlib.md5(text.encode(encoding)).hexdigest()


def hash_file(file_path: str) -> str:
    """Tính MD5 hash của file.

    Đọc file theo từng chunk để xử lý file lớn hiệu quả.

    Args:
        file_path: Đường dẫn tới file cần băm.

    Returns:
        Chuỗi hex 32 ký tự.

    Raises:
        FileNotFoundError: Nếu file không tồn tại.
        IOError: Nếu không đọc được file.
    """
    md5 = hashlib.md5()
    chunk_size = 65536  # 64 KB
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


def verify_text(text: str, expected_hash: str, encoding: str = "utf-8") -> bool:
    """Kiểm tra MD5 của văn bản có khớp với hash mong đợi không.

    Args:
        text: Văn bản cần kiểm tra.
        expected_hash: Hash MD5 mong đợi (32 ký tự hex).
        encoding: Encoding (mặc định utf-8).

    Returns:
        True nếu khớp, False nếu không.
    """
    return hash_text(text, encoding) == expected_hash.strip().lower()


def verify_file(file_path: str, expected_hash: str) -> bool:
    """Kiểm tra MD5 của file có khớp với hash mong đợi không.

    Args:
        file_path: Đường dẫn tới file.
        expected_hash: Hash MD5 mong đợi (32 ký tự hex).

    Returns:
        True nếu khớp, False nếu không.
    """
    return hash_file(file_path) == expected_hash.strip().lower()
