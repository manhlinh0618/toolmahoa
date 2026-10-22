"""
Module Controller
-----------------
Trung gian giữa GUI và các module thuật toán.
Controller chỉ làm nhiệm vụ gọi đúng hàm — không chứa thuật toán.

Luồng:
  GUI (event) → Controller → Algorithms / Services → trả về kết quả → GUI
"""

from crypto.aes_cipher import (
    encrypt_text, decrypt_text,
    encrypt_file, decrypt_file,
    hex_to_key,
)
from crypto.caesar_cipher import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from crypto.md5_hash import hash_text as md5_hash_text, hash_file as md5_hash_file
from crypto.key_manager import KeyManager
from services.clipboard_service import copy_to_clipboard as _copy


class CryptoController:
    """Lớp Controller điều phối tất cả nghiệp vụ mã hóa."""

    def __init__(self):
        self._key_manager = KeyManager()

    # ------------------------------------------------------------------ #
    # AES - Text                                                           #
    # ------------------------------------------------------------------ #

    def encrypt_aes_text(self, plaintext: str, key_hex: str, mode: str = "CBC") -> str:
        """Mã hóa văn bản bằng AES.

        Args:
            plaintext: Văn bản gốc.
            key_hex: Khóa dạng hex (32/48/64 ký tự).
            mode: Mode AES (ECB, CBC, CFB, CTR, GCM).

        Returns:
            Chuỗi Base64 đã mã hóa.

        Raises:
            ValueError: Nếu key không hợp lệ.
        """
        key = hex_to_key(key_hex)
        return encrypt_text(plaintext, key, mode)

    def decrypt_aes_text(self, ciphertext_b64: str, key_hex: str, mode: str = "CBC") -> str:
        """Giải mã văn bản AES.

        Args:
            ciphertext_b64: Chuỗi Base64 từ encrypt_aes_text().
            key_hex: Khóa dạng hex.
            mode: Mode AES.

        Returns:
            Văn bản gốc.
        """
        key = hex_to_key(key_hex)
        return decrypt_text(ciphertext_b64, key, mode)

    # ------------------------------------------------------------------ #
    # AES - File                                                           #
    # ------------------------------------------------------------------ #

    def encrypt_aes_file(
        self, input_path: str, output_path: str, key_hex: str, mode: str = "CBC"
    ) -> None:
        """Mã hóa file bằng AES.

        Args:
            input_path: Đường dẫn file cần mã hóa.
            output_path: Đường dẫn file kết quả (.enc).
            key_hex: Khóa dạng hex.
            mode: Mode AES.
        """
        key = hex_to_key(key_hex)
        encrypt_file(input_path, output_path, key, mode)

    def decrypt_aes_file(
        self, input_path: str, output_path: str, key_hex: str, mode: str = "CBC"
    ) -> None:
        """Giải mã file AES.

        Args:
            input_path: Đường dẫn file .enc.
            output_path: Đường dẫn file kết quả sau giải mã.
            key_hex: Khóa dạng hex.
            mode: Mode AES.
        """
        key = hex_to_key(key_hex)
        decrypt_file(input_path, output_path, key, mode)

    # ------------------------------------------------------------------ #
    # AES - Key                                                            #
    # ------------------------------------------------------------------ #

    def generate_aes_key(self, key_size: int = 256) -> str:
        """Sinh khóa AES ngẫu nhiên và trả về hex.

        Args:
            key_size: Kích thước khóa (128, 192, 256).

        Returns:
            Chuỗi hex của khóa.
        """
        return self._key_manager.generate(key_size)

    def save_key(self, key_hex: str, file_path: str) -> None:
        """Lưu khóa vào file .key."""
        self._key_manager.save_key(key_hex, file_path)

    def load_key(self, file_path: str) -> str:
        """Tải khóa từ file .key. Trả về hex string."""
        return self._key_manager.load_key(file_path)

    def validate_key(self, key_hex: str) -> tuple[bool, str]:
        """Kiểm tra tính hợp lệ của khóa hex."""
        return self._key_manager.validate_key_hex(key_hex)

    # ------------------------------------------------------------------ #
    # Caesar                                                               #
    # ------------------------------------------------------------------ #

    def encrypt_caesar(self, text: str, shift: int) -> str:
        """Mã hóa Caesar.

        Args:
            text: Văn bản gốc.
            shift: Số bước dịch chuyển.

        Returns:
            Văn bản đã mã hóa.
        """
        return caesar_encrypt(text, shift)

    def decrypt_caesar(self, text: str, shift: int) -> str:
        """Giải mã Caesar.

        Args:
            text: Văn bản đã mã hóa.
            shift: Số bước dịch chuyển đã dùng.

        Returns:
            Văn bản gốc.
        """
        return caesar_decrypt(text, shift)

    # ------------------------------------------------------------------ #
    # MD5                                                                  #
    # ------------------------------------------------------------------ #

    def hash_md5(self, text: str) -> str:
        """Tính MD5 hash của văn bản.

        Args:
            text: Văn bản cần băm.

        Returns:
            Chuỗi hex 32 ký tự.
        """
        return md5_hash_text(text)

    def hash_md5_file(self, file_path: str) -> str:
        """Tính MD5 hash của file.

        Args:
            file_path: Đường dẫn tới file.

        Returns:
            Chuỗi hex 32 ký tự.
        """
        return md5_hash_file(file_path)

    # ------------------------------------------------------------------ #
    # Clipboard                                                            #
    # ------------------------------------------------------------------ #

    def copy_to_clipboard(self, text: str) -> None:
        """Copy văn bản vào clipboard hệ thống.

        Args:
            text: Văn bản cần copy.
        """
        _copy(text)
