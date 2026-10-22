"""
Module Main Window (GUI)
------------------------
Cửa sổ chính của ứng dụng ToolMaHoa.
Quản lý: Notebook (Tab Text, Tab File), Thanh menu, Tiêu đề, Icon.
KHÔNG viết thuật toán ở đây.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from gui.text_tab import TextTab
from gui.file_tab import FileTab


class MainWindow:
    """Cửa sổ ứng dụng chính."""

    APP_TITLE = "ToolMaHoa - Công cụ Mã hóa & Giải mã"
    APP_SIZE = "900x680"

    def __init__(self, controller):
        """
        Args:
            controller: Đối tượng CryptoController xử lý logic.
        """
        self.controller = controller
        self.root = tk.Tk()
        self._setup_window()
        self._build_menu()
        self._build_notebook()

    # ------------------------------------------------------------------ #
    # Setup                                                                #
    # ------------------------------------------------------------------ #

    def _setup_window(self):
        """Cấu hình cửa sổ chính."""
        self.root.title(self.APP_TITLE)
        self.root.geometry(self.APP_SIZE)
        self.root.minsize(700, 500)

        # Thử load icon nếu tồn tại
        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "icon.ico"
        )
        if os.path.isfile(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass  # Bỏ qua nếu không load được icon

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", padding=[16, 6], font=("Arial", 10))
        style.configure("TButton", padding=[6, 4])

    def _build_menu(self):
        """Tạo thanh menu."""
        menubar = tk.Menu(self.root)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu Công cụ
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(
            label="Benchmark tốc độ AES",
            command=self._on_benchmark
        )
        menubar.add_cascade(label="Công cụ", menu=tools_menu)

        # Menu Trợ giúp
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn", command=self._on_help)
        help_menu.add_separator()
        help_menu.add_command(label="Thông tin", command=self._on_about)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_notebook(self):
        """Tạo Notebook chứa các tab."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab Text
        self.text_tab = TextTab(self.notebook, self.controller)
        self.notebook.add(self.text_tab, text="  📝 Mã hóa Văn bản  ")

        # Tab File
        self.file_tab = FileTab(self.notebook, self.controller)
        self.notebook.add(self.file_tab, text="  📁 Mã hóa File  ")

    # ------------------------------------------------------------------ #
    # Menu Handlers                                                        #
    # ------------------------------------------------------------------ #

    def _on_benchmark(self):
        """Mở cửa sổ benchmark AES."""
        from services.benchmark import run_benchmark_window
        run_benchmark_window(self.root)

    def _on_help(self):
        """Hiển thị hướng dẫn sử dụng."""
        help_text = (
            "HƯỚNG DẪN SỬ DỤNG\n\n"
            "Tab Văn bản:\n"
            "  1. Chọn thuật toán (AES / Caesar / MD5)\n"
            "  2. Nhập văn bản vào ô đầu vào\n"
            "  3. Với AES: nhập hoặc sinh khóa, chọn Mode\n"
            "  4. Với Caesar: nhập giá trị Shift\n"
            "  5. Nhấn 'Mã hóa' hoặc 'Giải mã'\n\n"
            "Tab File:\n"
            "  1. Chọn file đầu vào\n"
            "  2. Chọn đường dẫn lưu kết quả\n"
            "  3. Nhập hoặc sinh khóa AES\n"
            "  4. Nhấn 'Mã hóa File' hoặc 'Giải mã File'\n"
        )
        messagebox.showinfo("Hướng dẫn", help_text)

    def _on_about(self):
        """Hiển thị thông tin ứng dụng."""
        messagebox.showinfo(
            "Thông tin",
            "ToolMaHoa v1.0\n\n"
            "Công cụ mã hóa & giải mã văn bản và file.\n"
            "Hỗ trợ: AES (128/192/256), Caesar, MD5.\n\n"
            "Sử dụng: Python 3.11+ / PyCryptodome."
        )

    # ------------------------------------------------------------------ #
    # Run                                                                  #
    # ------------------------------------------------------------------ #

    def run(self):
        """Khởi chạy vòng lặp sự kiện Tkinter."""
        self.root.mainloop()
