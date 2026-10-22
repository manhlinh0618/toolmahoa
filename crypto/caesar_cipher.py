"""
Module Caesar Cipher
--------------------
Mã hóa / giải mã văn bản bằng mật mã Caesar.
Hỗ trợ toàn bộ ký tự Unicode (dịch chuyển theo ordinal).
"""


def encrypt(text: str, shift: int) -> str:
    """Mã hóa văn bản bằng Caesar cipher.

    Với chữ cái Latin (A-Z, a-z): dịch chuyển trong bảng chữ cái.
    Với ký tự khác: giữ nguyên.

    Args:
        text: Văn bản cần mã hóa.
        shift: Số bước dịch chuyển (có thể âm).

    Returns:
        Văn bản đã mã hóa.
    """
    shift = shift % 26  # Chuẩn hóa shift vào [0, 25]
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def decrypt(text: str, shift: int) -> str:
    """Giải mã văn bản đã mã hóa bằng Caesar cipher.

    Args:
        text: Văn bản đã mã hóa.
        shift: Số bước dịch chuyển đã dùng khi mã hóa.

    Returns:
        Văn bản gốc.
    """
    return encrypt(text, -shift)


def brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """Thử tất cả 25 bước dịch chuyển có thể.

    Args:
        ciphertext: Văn bản đã mã hóa.

    Returns:
        Danh sách tuple (shift, plaintext) cho tất cả 25 trường hợp.
    """
    results = []
    for shift in range(1, 26):
        results.append((shift, decrypt(ciphertext, shift)))
    return results
