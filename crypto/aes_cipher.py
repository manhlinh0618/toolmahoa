"""
Module AES Cipher
-----------------
Hỗ trợ mã hóa / giải mã văn bản và file bằng AES.
Các mode: ECB, CBC, CFB, CTR, GCM.
Sử dụng PyCryptodome.
"""

import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# ------------------------------------------------------------------ #
# Key generation                                                       #
# ------------------------------------------------------------------ #

def generate_key(key_size: int = 256) -> bytes:
    """Sinh khóa AES ngẫu nhiên.

    Args:
        key_size: Kích thước khóa theo bit (128, 192 hoặc 256).

    Returns:
        Bytes khóa ngẫu nhiên.

    Raises:
        ValueError: Nếu key_size không hợp lệ.
    """
    valid_sizes = {128: 16, 192: 24, 256: 32}
    if key_size not in valid_sizes:
        raise ValueError(f"key_size phải là 128, 192 hoặc 256. Nhận được: {key_size}")
    return get_random_bytes(valid_sizes[key_size])


def key_to_hex(key: bytes) -> str:
    """Chuyển bytes khóa sang chuỗi hex."""
    return key.hex().upper()


def hex_to_key(hex_str: str) -> bytes:
    """Chuyển chuỗi hex sang bytes khóa.

    Raises:
        ValueError: Nếu chuỗi hex không hợp lệ hoặc độ dài sai.
    """
    try:
        key = bytes.fromhex(hex_str.strip())
    except ValueError:
        raise ValueError("Khóa không phải chuỗi hex hợp lệ.")
    if len(key) not in (16, 24, 32):
        raise ValueError(
            f"Độ dài khóa phải là 16, 24 hoặc 32 bytes (nhận {len(key)} bytes)."
        )
    return key


# ------------------------------------------------------------------ #
# Internal helpers                                                     #
# ------------------------------------------------------------------ #

def _get_mode_const(mode: str):
    """Trả về hằng số AES mode từ chuỗi tên."""
    modes = {
        "ECB": AES.MODE_ECB,
        "CBC": AES.MODE_CBC,
        "CFB": AES.MODE_CFB,
        "CTR": AES.MODE_CTR,
        "GCM": AES.MODE_GCM,
    }
    m = mode.upper()
    if m not in modes:
        raise ValueError(f"Mode không hợp lệ: {mode}. Chọn ECB, CBC, CFB, CTR, GCM.")
    return modes[m]


def _create_cipher(key: bytes, mode: str, iv: bytes = None):
    """Tạo đối tượng cipher phù hợp mode."""
    m = mode.upper()
    if m == "ECB":
        return AES.new(key, AES.MODE_ECB), None
    elif m == "CBC":
        iv = iv or get_random_bytes(16)
        return AES.new(key, AES.MODE_CBC, iv=iv), iv
    elif m == "CFB":
        iv = iv or get_random_bytes(16)
        return AES.new(key, AES.MODE_CFB, iv=iv), iv
    elif m == "CTR":
        # CTR dùng nonce 8-byte + counter
        nonce = iv[:8] if iv else get_random_bytes(8)
        return AES.new(key, AES.MODE_CTR, nonce=nonce), nonce
    elif m == "GCM":
        nonce = iv or get_random_bytes(16)
        return AES.new(key, AES.MODE_GCM, nonce=nonce), nonce
    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")


# ------------------------------------------------------------------ #
# Text encrypt / decrypt                                               #
# ------------------------------------------------------------------ #

def encrypt_text(plaintext: str, key: bytes, mode: str = "CBC") -> str:
    """Mã hóa văn bản.

    Quy trình: UTF-8 → Padding → AES → Base64.

    Args:
        plaintext: Văn bản gốc (chuỗi Python).
        key: Bytes khóa (16, 24 hoặc 32 bytes).
        mode: Mode hoạt động AES (ECB, CBC, CFB, CTR, GCM).

    Returns:
        Chuỗi Base64 chứa [IV/nonce (nếu có)] + ciphertext.
    """
    data = plaintext.encode("utf-8")
    m = mode.upper()

    if m == "GCM":
        cipher, nonce = _create_cipher(key, mode)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        # Format: nonce(16) + tag(16) + ciphertext
        combined = nonce + tag + ciphertext
        return base64.b64encode(combined).decode("utf-8")

    elif m in ("ECB",):
        cipher, _ = _create_cipher(key, mode)
        padded = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded)
        return base64.b64encode(ciphertext).decode("utf-8")

    elif m in ("CBC", "CFB"):
        cipher, iv = _create_cipher(key, mode)
        padded = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded)
        combined = iv + ciphertext
        return base64.b64encode(combined).decode("utf-8")

    elif m == "CTR":
        cipher, nonce = _create_cipher(key, mode)
        ciphertext = cipher.encrypt(data)
        combined = nonce + ciphertext
        return base64.b64encode(combined).decode("utf-8")

    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")


def decrypt_text(ciphertext_b64: str, key: bytes, mode: str = "CBC") -> str:
    """Giải mã văn bản đã mã hóa bởi encrypt_text().

    Args:
        ciphertext_b64: Chuỗi Base64 từ encrypt_text().
        key: Bytes khóa (16, 24 hoặc 32 bytes).
        mode: Mode hoạt động AES.

    Returns:
        Văn bản gốc.
    """
    combined = base64.b64decode(ciphertext_b64)
    m = mode.upper()

    if m == "GCM":
        nonce = combined[:16]
        tag = combined[16:32]
        ciphertext = combined[32:]
        cipher, _ = _create_cipher(key, mode, iv=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")

    elif m == "ECB":
        cipher, _ = _create_cipher(key, mode)
        padded = cipher.decrypt(combined)
        return unpad(padded, AES.block_size).decode("utf-8")

    elif m in ("CBC", "CFB"):
        iv = combined[:16]
        ciphertext = combined[16:]
        cipher, _ = _create_cipher(key, mode, iv=iv)
        padded = cipher.decrypt(ciphertext)
        return unpad(padded, AES.block_size).decode("utf-8")

    elif m == "CTR":
        nonce = combined[:8]
        ciphertext = combined[8:]
        cipher, _ = _create_cipher(key, mode, iv=nonce)
        return cipher.decrypt(ciphertext).decode("utf-8")

    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")


# ------------------------------------------------------------------ #
# File encrypt / decrypt                                               #
# ------------------------------------------------------------------ #

def encrypt_file(input_path: str, output_path: str, key: bytes, mode: str = "CBC") -> None:
    """Mã hóa file.

    Luồng: Đọc file → Padding → AES → Ghi file .enc.
    Output file format: [IV/nonce] + [ciphertext].

    Args:
        input_path: Đường dẫn file cần mã hóa.
        output_path: Đường dẫn file kết quả (thường .enc).
        key: Bytes khóa.
        mode: Mode AES.
    """
    with open(input_path, "rb") as f:
        data = f.read()

    m = mode.upper()

    if m == "GCM":
        cipher, nonce = _create_cipher(key, mode)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(output_path, "wb") as f:
            f.write(nonce + tag + ciphertext)

    elif m == "ECB":
        cipher, _ = _create_cipher(key, mode)
        padded = pad(data, AES.block_size)
        with open(output_path, "wb") as f:
            f.write(cipher.encrypt(padded))

    elif m in ("CBC", "CFB"):
        cipher, iv = _create_cipher(key, mode)
        padded = pad(data, AES.block_size)
        with open(output_path, "wb") as f:
            f.write(iv + cipher.encrypt(padded))

    elif m == "CTR":
        cipher, nonce = _create_cipher(key, mode)
        with open(output_path, "wb") as f:
            f.write(nonce + cipher.encrypt(data))

    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")


def decrypt_file(input_path: str, output_path: str, key: bytes, mode: str = "CBC") -> None:
    """Giải mã file đã mã hóa bởi encrypt_file().

    Luồng: Đọc .enc → AES → Bỏ padding → Khôi phục file.

    Args:
        input_path: Đường dẫn file .enc.
        output_path: Đường dẫn file kết quả sau giải mã.
        key: Bytes khóa.
        mode: Mode AES.
    """
    with open(input_path, "rb") as f:
        combined = f.read()

    m = mode.upper()

    if m == "GCM":
        nonce = combined[:16]
        tag = combined[16:32]
        ciphertext = combined[32:]
        cipher, _ = _create_cipher(key, mode, iv=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

    elif m == "ECB":
        cipher, _ = _create_cipher(key, mode)
        padded = cipher.decrypt(combined)
        data = unpad(padded, AES.block_size)

    elif m in ("CBC", "CFB"):
        iv = combined[:16]
        ciphertext = combined[16:]
        cipher, _ = _create_cipher(key, mode, iv=iv)
        padded = cipher.decrypt(ciphertext)
        data = unpad(padded, AES.block_size)

    elif m == "CTR":
        nonce = combined[:8]
        ciphertext = combined[8:]
        cipher, _ = _create_cipher(key, mode, iv=nonce)
        data = cipher.decrypt(ciphertext)

    else:
        raise ValueError(f"Mode không hợp lệ: {mode}")

    with open(output_path, "wb") as f:
        f.write(data)
