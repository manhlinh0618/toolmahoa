"""
Module Clipboard Service
------------------------
Copy văn bản vào clipboard hệ thống.
Sử dụng tkinter.Tk để không phụ thuộc thêm thư viện bên ngoài.
"""

import tkinter as tk


def copy_to_clipboard(text: str) -> None:
    """Copy văn bản vào clipboard hệ thống.

    Args:
        text: Văn bản cần copy.
    """
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ phụ
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Cần thiết để dữ liệu clipboard tồn tại sau khi destroy
    root.destroy()


def get_from_clipboard() -> str:
    """Lấy văn bản từ clipboard hệ thống.

    Returns:
        Nội dung clipboard hiện tại (chuỗi).
        Trả về chuỗi rỗng nếu clipboard không chứa văn bản.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        content = root.clipboard_get()
        root.destroy()
        return content
    except tk.TclError:
        return ""
