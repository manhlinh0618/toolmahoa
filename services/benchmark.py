"""
Module Benchmark
----------------
Đo tốc độ mã hóa AES-128, AES-192, AES-256 trên 1 MB dữ liệu.
Hỗ trợ hiển thị kết quả dưới dạng bảng trong cửa sổ Tkinter.
"""

import time
import os
import tkinter as tk
from tkinter import ttk

from crypto.aes_cipher import generate_key, encrypt_file, decrypt_file


BENCHMARK_DATA_SIZE = 1 * 1024 * 1024  # 1 MB
BENCHMARK_MODES = ["ECB", "CBC", "CFB", "CTR"]
BENCHMARK_KEY_SIZES = [128, 192, 256]


def _benchmark_aes(key_size: int, mode: str, data: bytes, tmp_dir: str) -> dict:
    """Đo thời gian mã hóa + giải mã AES cho một cấu hình.

    Args:
        key_size: Kích thước khóa (128, 192, 256).
        mode: Mode AES (ECB, CBC, CFB, CTR).
        data: Dữ liệu mẫu (bytes).
        tmp_dir: Thư mục tạm để ghi file test.

    Returns:
        Dict chứa kết quả đo: key_size, mode, enc_time, dec_time, throughput.
    """
    key = generate_key(key_size)
    tmp_input = os.path.join(tmp_dir, "bench_input.bin")
    tmp_enc = os.path.join(tmp_dir, "bench_enc.bin")
    tmp_dec = os.path.join(tmp_dir, "bench_dec.bin")

    with open(tmp_input, "wb") as f:
        f.write(data)

    # Đo mã hóa
    t0 = time.perf_counter()
    encrypt_file(tmp_input, tmp_enc, key, mode)
    enc_time = time.perf_counter() - t0

    # Đo giải mã
    t0 = time.perf_counter()
    decrypt_file(tmp_enc, tmp_dec, key, mode)
    dec_time = time.perf_counter() - t0

    # Thông lượng (MB/s)
    throughput = (BENCHMARK_DATA_SIZE / 1024 / 1024) / enc_time

    # Dọn dẹp
    for p in (tmp_input, tmp_enc, tmp_dec):
        if os.path.exists(p):
            os.remove(p)

    return {
        "key_size": key_size,
        "mode": mode,
        "enc_time": enc_time,
        "dec_time": dec_time,
        "throughput": throughput,
    }


def run_benchmark() -> list[dict]:
    """Chạy benchmark cho tất cả tổ hợp key_size + mode.

    Returns:
        Danh sách kết quả (mỗi phần tử là dict từ _benchmark_aes).
    """
    import tempfile
    data = os.urandom(BENCHMARK_DATA_SIZE)
    results = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        for key_size in BENCHMARK_KEY_SIZES:
            for mode in BENCHMARK_MODES:
                result = _benchmark_aes(key_size, mode, data, tmp_dir)
                results.append(result)
    return results


def run_benchmark_window(parent=None):
    """Tạo cửa sổ Tkinter hiển thị kết quả benchmark.

    Args:
        parent: Cửa sổ cha (optional).
    """
    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title("Benchmark AES - So sánh tốc độ")
    win.geometry("700x420")
    win.resizable(False, False)

    ttk.Label(win, text="Benchmark đang chạy...",
              font=("Arial", 12)).pack(pady=10)

    # Bảng kết quả
    cols = ("Thuật toán", "Mode", "Mã hóa (s)", "Giải mã (s)", "Thông lượng (MB/s)")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=14)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=5)

    status_var = tk.StringVar(value="Đang đo... (có thể mất vài giây)")
    ttk.Label(win, textvariable=status_var, foreground="gray").pack(pady=4)

    def run():
        try:
            results = run_benchmark()
            tree.delete(*tree.get_children())
            for r in results:
                tree.insert("", "end", values=(
                    f"AES-{r['key_size']}",
                    r["mode"],
                    f"{r['enc_time']:.4f}",
                    f"{r['dec_time']:.4f}",
                    f"{r['throughput']:.2f}",
                ))
            status_var.set(
                f"✅ Hoàn tất benchmark trên {BENCHMARK_DATA_SIZE // 1024 // 1024} MB dữ liệu ngẫu nhiên."
            )
        except Exception as e:
            status_var.set(f"❌ Lỗi: {e}")

    # Chạy benchmark sau khi cửa sổ hiển thị
    win.after(200, run)

    if parent is None:
        win.mainloop()
