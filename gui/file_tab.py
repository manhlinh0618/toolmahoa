"""
Module File Tab (GUI)
---------------------
Tab mã hóa / giải mã file bằng AES trong giao diện Tkinter.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileTab(ttk.Frame):
    """Frame chứa toàn bộ giao diện Tab File."""

    AES_MODES = ["CBC", "ECB", "CFB", "CTR", "GCM"]
    AES_KEY_SIZES = ["128", "192", "256"]

    def __init__(self, parent, controller):
        """
        Args:
            parent: Widget cha (Notebook).
            controller: Đối tượng Controller xử lý logic.
        """
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    # ------------------------------------------------------------------ #
    # UI Construction                                                      #
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        """Xây dựng toàn bộ giao diện tab file."""
        self.columnconfigure(1, weight=1)

        # ── Hàng 0: Chọn file đầu vào ─────────────────────────────────
        ttk.Label(self, text="File đầu vào:").grid(
            row=0, column=0, sticky="w", padx=10, pady=(14, 6)
        )
        file_in_frame = ttk.Frame(self)
        file_in_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=(14, 6))
        file_in_frame.columnconfigure(0, weight=1)
        self.input_path_var = tk.StringVar()
        ttk.Entry(file_in_frame, textvariable=self.input_path_var,
                  state="readonly").grid(row=0, column=0, sticky="ew")
        ttk.Button(file_in_frame, text="Chọn file", width=10,
                   command=self._on_browse_input).grid(row=0, column=1, padx=(6, 0))

        # ── Hàng 1: File đầu ra ───────────────────────────────────────
        ttk.Label(self, text="File đầu ra:").grid(
            row=1, column=0, sticky="w", padx=10, pady=6
        )
        file_out_frame = ttk.Frame(self)
        file_out_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        file_out_frame.columnconfigure(0, weight=1)
        self.output_path_var = tk.StringVar()
        ttk.Entry(file_out_frame, textvariable=self.output_path_var).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Button(file_out_frame, text="Lưu tại...", width=10,
                   command=self._on_browse_output).grid(row=0, column=1, padx=(6, 0))

        # ── Hàng 2: Mode AES ──────────────────────────────────────────
        ttk.Label(self, text="Mode AES:").grid(
            row=2, column=0, sticky="w", padx=10, pady=6
        )
        self.mode_var = tk.StringVar(value="CBC")
        ttk.Combobox(self, textvariable=self.mode_var,
                     values=self.AES_MODES, state="readonly", width=10).grid(
            row=2, column=1, sticky="w", padx=10, pady=6
        )

        # ── Hàng 3: Key size ──────────────────────────────────────────
        ttk.Label(self, text="Key size (bit):").grid(
            row=3, column=0, sticky="w", padx=10, pady=6
        )
        self.keysize_var = tk.StringVar(value="256")
        ttk.Combobox(self, textvariable=self.keysize_var,
                     values=self.AES_KEY_SIZES, state="readonly", width=10).grid(
            row=3, column=1, sticky="w", padx=10, pady=6
        )

        # ── Hàng 4: Khóa AES ──────────────────────────────────────────
        ttk.Label(self, text="Khóa (hex):").grid(
            row=4, column=0, sticky="w", padx=10, pady=6
        )
        key_frame = ttk.Frame(self)
        key_frame.grid(row=4, column=1, sticky="ew", padx=10, pady=6)
        key_frame.columnconfigure(0, weight=1)
        self.key_var = tk.StringVar()
        ttk.Entry(key_frame, textvariable=self.key_var).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Button(key_frame, text="Sinh khóa", width=10,
                   command=self._on_generate_key).grid(row=0, column=1, padx=(6, 0))
        ttk.Button(key_frame, text="Tải .key", width=10,
                   command=self._on_load_key).grid(row=0, column=2, padx=(6, 0))
        ttk.Button(key_frame, text="Lưu .key", width=10,
                   command=self._on_save_key).grid(row=0, column=3, padx=(6, 0))

        # ── Hàng 5: Nút hành động ─────────────────────────────────────
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="🔒 Mã hóa File", width=18,
                   command=self._on_encrypt_file).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="🔓 Giải mã File", width=18,
                   command=self._on_decrypt_file).pack(side="left", padx=10)

        # ── Hàng 6: Thanh trạng thái ──────────────────────────────────
        self.status_var = tk.StringVar(value="Vui lòng chọn file để tiếp tục.")
        ttk.Label(self, textvariable=self.status_var,
                  foreground="gray").grid(
            row=6, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10)
        )

        # ── Hàng 7: Thanh tiến trình ──────────────────────────────────
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.grid(row=7, column=0, columnspan=2,
                           sticky="ew", padx=10, pady=(0, 14))

    # ------------------------------------------------------------------ #
    # Event Handlers                                                       #
    # ------------------------------------------------------------------ #

    def _on_browse_input(self):
        """Mở hộp thoại chọn file đầu vào."""
        path = filedialog.askopenfilename(
            title="Chọn file cần mã hóa / giải mã"
        )
        if path:
            self.input_path_var.set(path)
            # Tự động đề xuất đường dẫn output
            if path.endswith(".enc"):
                self.output_path_var.set(path[:-4])
            else:
                self.output_path_var.set(path + ".enc")
            self._set_status(f"Đã chọn: {os.path.basename(path)}")

    def _on_browse_output(self):
        """Mở hộp thoại chọn vị trí lưu file đầu ra."""
        path = filedialog.asksaveasfilename(
            title="Chọn vị trí lưu file kết quả"
        )
        if path:
            self.output_path_var.set(path)

    def _on_generate_key(self):
        """Sinh khóa AES ngẫu nhiên."""
        key_size = int(self.keysize_var.get())
        key_hex = self.controller.generate_aes_key(key_size)
        self.key_var.set(key_hex)
        self._set_status(f"Đã sinh khóa AES-{key_size}.")

    def _on_load_key(self):
        """Tải khóa từ file .key."""
        path = filedialog.askopenfilename(
            title="Chọn file khóa",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        if path:
            try:
                key_hex = self.controller.load_key(path)
                self.key_var.set(key_hex)
                self._set_status("Đã tải khóa thành công.")
            except Exception as e:
                messagebox.showerror("Lỗi tải khóa", str(e))

    def _on_save_key(self):
        """Lưu khóa hiện tại vào file .key."""
        key_hex = self.key_var.get().strip()
        if not key_hex:
            messagebox.showwarning("Cảnh báo", "Chưa có khóa để lưu.")
            return
        path = filedialog.asksaveasfilename(
            title="Lưu khóa",
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        if path:
            try:
                self.controller.save_key(key_hex, path)
                self._set_status(f"Đã lưu khóa: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Lỗi lưu khóa", str(e))

    def _on_encrypt_file(self):
        """Mã hóa file."""
        if not self._validate_inputs():
            return
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        key_hex = self.key_var.get().strip()
        mode = self.mode_var.get()
        self._start_progress("Đang mã hóa...")
        try:
            self.controller.encrypt_aes_file(input_path, output_path, key_hex, mode)
            self._set_status(f"✅ Mã hóa thành công → {os.path.basename(output_path)}")
        except Exception as e:
            messagebox.showerror("Lỗi mã hóa file", str(e))
            self._set_status("❌ Mã hóa thất bại.")
        finally:
            self._stop_progress()

    def _on_decrypt_file(self):
        """Giải mã file."""
        if not self._validate_inputs():
            return
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        key_hex = self.key_var.get().strip()
        mode = self.mode_var.get()
        self._start_progress("Đang giải mã...")
        try:
            self.controller.decrypt_aes_file(input_path, output_path, key_hex, mode)
            self._set_status(f"✅ Giải mã thành công → {os.path.basename(output_path)}")
        except Exception as e:
            messagebox.showerror("Lỗi giải mã file", str(e))
            self._set_status("❌ Giải mã thất bại.")
        finally:
            self._stop_progress()

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _validate_inputs(self) -> bool:
        """Kiểm tra các trường bắt buộc trước khi xử lý."""
        if not self.input_path_var.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file để tiếp tục.")
            return False
        if not self.output_path_var.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đường dẫn file đầu ra.")
            return False
        if not self.key_var.get().strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập hoặc sinh khóa AES.")
            return False
        return True

    def _set_status(self, msg: str):
        """Cập nhật thông báo trạng thái."""
        self.status_var.set(msg)

    def _start_progress(self, msg: str = "Đang xử lý..."):
        self._set_status(msg)
        self.progress.start(10)

    def _stop_progress(self):
        self.progress.stop()
