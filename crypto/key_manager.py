"""
Module Key Manager
------------------
Quản lý khóa AES: sinh, lưu, đọc, xóa.
Khóa được lưu dưới dạng hex text trong file .key.
"""

import os
from crypto.aes_cipher import generate_key, key_to_hex, hex_to_key


class KeyManager:
    """Lớp quản lý vòng đời của khóa AES."""

    # ------------------------------------------------------------------ #
    # Generate                                                             #
    # ------------------------------------------------------------------ #

    def generate(self, key_size: int = 256) -> str:
        """Sinh khóa AES ngẫu nhiên và trả về dạng hex.

        Args:
            key_size: Kích thước khóa (128, 192, 256).

        Returns:
            Chuỗi hex đại diện cho khóa.
        """
        key_bytes = generate_key(key_size)
        return key_to_hex(key_bytes)

    # ------------------------------------------------------------------ #
    # Save / Load                                                          #
    # ------------------------------------------------------------------ #

    def save_key(self, key_hex: str, file_path: str) -> None:
        """Lưu khóa hex vào file .key.

        Args:
            key_hex: Chuỗi hex của khóa.
            file_path: Đường dẫn file để lưu (nên có đuôi .key).

        Raises:
            ValueError: Nếu key_hex không hợp lệ.
            IOError: Nếu không ghi được file.
        """
        # Validate trước khi lưu
        hex_to_key(key_hex)  # sẽ raise nếu không hợp lệ
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(key_hex.strip().upper())

    def load_key(self, file_path: str) -> str:
        """Đọc khóa từ file .key.

        Args:
            file_path: Đường dẫn file .key.

        Returns:
            Chuỗi hex của khóa.

        Raises:
            FileNotFoundError: Nếu file không tồn tại.
            ValueError: Nếu nội dung file không hợp lệ.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Không tìm thấy file key: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            key_hex = f.read().strip()
        # Validate
        hex_to_key(key_hex)
        return key_hex.upper()

    # ------------------------------------------------------------------ #
    # Delete                                                               #
    # ------------------------------------------------------------------ #

    def delete_key(self, file_path: str) -> None:
        """Xóa file .key.

        Args:
            file_path: Đường dẫn file .key cần xóa.

        Raises:
            FileNotFoundError: Nếu file không tồn tại.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Không tìm thấy file key: {file_path}")
        os.remove(file_path)

    # ------------------------------------------------------------------ #
    # Validate                                                             #
    # ------------------------------------------------------------------ #

    def validate_key_hex(self, key_hex: str) -> tuple[bool, str]:
        """Kiểm tra chuỗi hex có phải khóa AES hợp lệ không.

        Args:
            key_hex: Chuỗi hex cần kiểm tra.

        Returns:
            Tuple (is_valid: bool, message: str).
        """
        try:
            key = hex_to_key(key_hex)
            bits = len(key) * 8
            return True, f"Khóa hợp lệ AES-{bits}"
        except ValueError as e:
            return False, str(e)

    def get_key_info(self, key_hex: str) -> dict:
        """Trả về thông tin về khóa.

        Args:
            key_hex: Chuỗi hex của khóa.

        Returns:
            Dict chứa thông tin: bytes, bits, is_valid.
        """
        try:
            key = hex_to_key(key_hex)
            return {
                "is_valid": True,
                "bytes": len(key),
                "bits": len(key) * 8,
                "algorithm": f"AES-{len(key) * 8}",
            }
        except ValueError as e:
            return {"is_valid": False, "error": str(e)}
