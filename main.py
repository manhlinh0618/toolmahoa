"""
main.py — Điểm khởi động ứng dụng ToolMaHoa
============================================
Chạy: python main.py
"""

import sys
import os

# them thu muc goc vao sys.path de import dung
sys.path.insert(0, os.path.dirname(__file__))

from controller import CryptoController
from gui.main_window import MainWindow


def main():
    """Khởi tạo Controller và MainWindow, sau đó chạy vòng lặp sự kiện."""
    controller = CryptoController()
    window = MainWindow(controller)
    window.run()


if __name__ == "__main__":
    main()
