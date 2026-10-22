"""
Module Text Tab (GUI)
---------------------
Tab mã hóa / giải mã văn bản trong giao diện Tkinter.
Hỗ trợ: AES (CBC/ECB/CFB/CTR/GCM), Caesar, MD5.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TextTab(ttk.Frame):
    """Frame chứa toàn bộ giao diện Tab Text."""

    ALGORITHMS = ["AES", "Caesar", "MD5"]
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
        """Xây dựng toàn bộ giao diện tab."""
        self.columnconfigure(1, weight=1)

        # ── Hàng 0: Chọn thuật toán ──────────────────────────────────
        ttk.Label(self, text="Thuật toán:").grid(
            row=0, column=0, sticky="w", padx=10, pady=(10, 4)
        )
        self.algo_var = tk.StringVar(value="AES")
        self.algo_combo = ttk.Combobox(
            self, textvariable=self.algo_var,
            values=self.ALGORITHMS, state="readonly", width=15
        )
        self.algo_combo.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 4))
        self.algo_combo.bind("<<ComboboxSelected>>", self._on_algo_change)

        # ── Hàng 1: Mode AES (ẩn khi không dùng AES) ─────────────────
        self.mode_label = ttk.Label(self, text="Mode AES:")
        self.mode_label.grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.mode_var = tk.StringVar(value="CBC")
        self.mode_combo = ttk.Combobox(
            self, textvariable=self.mode_var,
            values=self.AES_MODES, state="readonly", width=10
        )
        self.mode_combo.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        # ── Hàng 2: Key size (ẩn khi không dùng AES) ─────────────────
        self.keysize_label = ttk.Label(self, text="Key size (bit):")
        self.keysize_label.grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.keysize_var = tk.StringVar(value="256")
        self.keysize_combo = ttk.Combobox(
            self, textvariable=self.keysize_var,
            values=self.AES_KEY_SIZES, state="readonly", width=10
        )
        self.keysize_combo.grid(row=2, column=1, sticky="w", padx=10, pady=4)

        # ── Hàng 3: Shift (ẩn khi không dùng Caesar) ─────────────────
        self.shift_label = ttk.Label(self, text="Shift (Caesar):")
        self.shift_label.grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.shift_var = tk.StringVar(value="3")
        self.shift_entry = ttk.Entry(self, textvariable=self.shift_var, width=10)
        self.shift_entry.grid(row=3, column=1, sticky="w", padx=10, pady=4)

        # ── Hàng 4: Khóa AES ──────────────────────────────────────────
        self.key_label = ttk.Label(self, text="Khóa (hex):")
        self.key_label.grid(row=4, column=0, sticky="w", padx=10, pady=4)
        key_frame = ttk.Frame(self)
        key_frame.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        key_frame.columnconfigure(0, weight=1)
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var)
        self.key_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(key_frame, text="Sinh khóa", width=10,
                   command=self._on_generate_key).grid(row=0, column=1, padx=(4, 0))
        ttk.Button(key_frame, text="Copy Key", width=10,
                   command=self._on_copy_key).grid(row=0, column=2, padx=(4, 0))

        # ── Hàng 5: Văn bản đầu vào ───────────────────────────────────
        ttk.Label(self, text="Văn bản đầu vào:").grid(
            row=5, column=0, sticky="nw", padx=10, pady=(10, 4)
        )
        self.input_text = tk.Text(self, height=7, wrap="word")
        self.input_text.grid(
            row=5, column=1, sticky="nsew", padx=10, pady=(10, 4)
        )

        # ── Hàng 6: Nút hành động ─────────────────────────────────────
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=6, column=1, sticky="w", padx=10, pady=6)
        ttk.Button(btn_frame, text="🔒 Mã hóa", width=14,
                   command=self._on_encrypt).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="🔓 Giải mã", width=14,
                   command=self._on_decrypt).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="🗑 Xóa", width=10,
                   command=self._on_clear).pack(side="left")

        # ── Hàng 7: Kết quả ───────────────────────────────────────────
        ttk.Label(self, text="Kết quả:").grid(
            row=7, column=0, sticky="nw", padx=10, pady=(10, 4)
        )
        result_frame = ttk.Frame(self)
        result_frame.grid(row=7, column=1, sticky="nsew", padx=10, pady=(10, 4))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        self.result_text = tk.Text(result_frame, height=7, wrap="word",
                                   state="disabled", bg="#f4f4f4")
        self.result_text.grid(row=0, column=0, sticky="nsew")
        ttk.Button(result_frame, text="Copy kết quả",
                   command=self._on_copy_result).grid(row=1, column=0, sticky="e", pady=(4, 0))

        self.rowconfigure(5, weight=1)
        self.rowconfigure(7, weight=1)

        # Khởi tạo trạng thái ban đầu
        self._update_visibility()

    # ------------------------------------------------------------------ #
    # Event Handlers                                                       #
    # ------------------------------------------------------------------ #

    def _on_algo_change(self, event=None):
        """Cập nhật giao diện khi người dùng đổi thuật toán."""
        self._update_visibility()

    def _on_generate_key(self):
        """Yêu cầu controller sinh khóa AES."""
        key_size = int(self.keysize_var.get())
        key_hex = self.controller.generate_aes_key(key_size)
        self.key_var.set(key_hex)

    def _on_copy_key(self):
        """Copy khóa vào clipboard."""
        key = self.key_var.get().strip()
        if not key:
            messagebox.showwarning("Cảnh báo", "Chưa có khóa để copy.")
            return
        self.controller.copy_to_clipboard(key)
        messagebox.showinfo("Thông báo", "Đã copy khóa vào clipboard!")

    def _on_copy_result(self):
        """Copy kết quả vào clipboard."""
        result = self.result_text.get("1.0", "end").strip()
        if not result:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để copy.")
            return
        self.controller.copy_to_clipboard(result)
        messagebox.showinfo("Thông báo", "Đã copy kết quả vào clipboard!")

    def _on_encrypt(self):
        """Xử lý sự kiện bấm nút Mã hóa."""
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản để mã hóa.")
            return

        algo = self.algo_var.get()
        try:
            if algo == "AES":
                key_hex = self.key_var.get().strip()
                if not key_hex:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập hoặc sinh khóa AES.")
                    return
                mode = self.mode_var.get()
                result = self.controller.encrypt_aes_text(text, key_hex, mode)

            elif algo == "Caesar":
                shift = self._get_shift()
                if shift is None:
                    return
                result = self.controller.encrypt_caesar(text, shift)

            elif algo == "MD5":
                result = self.controller.hash_md5(text)

            else:
                messagebox.showerror("Lỗi", f"Thuật toán không hỗ trợ: {algo}")
                return

            self._set_result(result)

        except Exception as e:
            messagebox.showerror("Lỗi mã hóa", str(e))

    def _on_decrypt(self):
        """Xử lý sự kiện bấm nút Giải mã."""
        if self.algo_var.get() == "MD5":
            messagebox.showinfo("Thông báo", "MD5 là hàm băm một chiều, không thể giải mã.")
            return

        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản để giải mã.")
            return

        algo = self.algo_var.get()
        try:
            if algo == "AES":
                key_hex = self.key_var.get().strip()
                if not key_hex:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập khóa AES.")
                    return
                mode = self.mode_var.get()
                result = self.controller.decrypt_aes_text(text, key_hex, mode)

            elif algo == "Caesar":
                shift = self._get_shift()
                if shift is None:
                    return
                result = self.controller.decrypt_caesar(text, shift)

            else:
                messagebox.showerror("Lỗi", f"Thuật toán không hỗ trợ: {algo}")
                return

            self._set_result(result)

        except Exception as e:
            messagebox.showerror("Lỗi giải mã", str(e))

    def _on_clear(self):
        """Xóa nội dung ô nhập và ô kết quả."""
        self.input_text.delete("1.0", "end")
        self._set_result("")

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _update_visibility(self):
        """Hiển thị / ẩn các widget dựa theo thuật toán được chọn."""
        algo = self.algo_var.get()
        is_aes = algo == "AES"
        is_caesar = algo == "Caesar"

        widgets_aes = [self.mode_label, self.mode_combo,
                       self.keysize_label, self.keysize_combo,
                       self.key_label, self.key_entry]
        widgets_caesar = [self.shift_label, self.shift_entry]

        for w in widgets_aes:
            w.grid() if is_aes else w.grid_remove()
        for w in widgets_caesar:
            w.grid() if is_caesar else w.grid_remove()

    def _get_shift(self):
        """Lấy và validate giá trị shift Caesar."""
        try:
            return int(self.shift_var.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Shift phải là số nguyên.")
            return None

    def _set_result(self, text: str):
        """Hiển thị kết quả vào ô result."""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.config(state="disabled")
