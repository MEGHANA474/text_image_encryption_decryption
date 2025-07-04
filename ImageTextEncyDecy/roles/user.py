# File: roles/user.py

from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
from crypto_utils import load_key_hex, decrypt_text, decrypt_image
from access_control import get_key_if_allowed
from PIL import ImageTk, Image
import os
import numpy as np

class UserWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("User Panel")
        self.frame = Frame(self.master, padx=50, pady=40)
        self.frame.pack(fill="both", expand=True)

        Label(self.frame, text="User Dashboard", font=("Arial", 24, "bold")).pack(pady=20)

        Button(self.frame, text="Decrypt Text", font=("Arial", 16), width=25, command=self.decrypt_text_ui).pack(pady=10)
        Button(self.frame, text="Decrypt Image", font=("Arial", 16), width=25, command=self.decrypt_image_ui).pack(pady=10)
        Button(self.frame, text="Close", font=("Arial", 14), command=self.master.destroy).pack(pady=20)

    def decrypt_text_ui(self):
        filename = simpledialog.askstring("Filename", "Enter encrypted text filename (e.g. note1.txt):")
        if not filename:
            return

        file_path = os.path.join("data/encrypted", filename)
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found.")
            return

        key_hex = get_key_if_allowed(filename, "user")
        if not key_hex:
            messagebox.showerror("Access Denied", "You don't have access to this file.")
            return

        with open(file_path, "r") as f:
            encrypted = f.read()

        key = load_key_hex(key_hex)
        try:
            decrypted = decrypt_text(encrypted, key)
            messagebox.showinfo("Decrypted Text", decrypted)
        except Exception:
            messagebox.showerror("Error", "Decryption failed.")

    def decrypt_image_ui(self):
        filename = simpledialog.askstring("Filename", "Enter encrypted image filename (without .bin):")
        if not filename:
            return

        bin_path = os.path.join("data/encrypted", filename + ".bin")
        shape_path = bin_path + ".shape"

        if not os.path.exists(bin_path) or not os.path.exists(shape_path):
            messagebox.showerror("Error", "Encrypted image or shape file not found.")
            return

        key_hex = get_key_if_allowed(filename, "user")
        if not key_hex:
            messagebox.showerror("Access Denied", "You don't have permission to view this image.")
            return

        with open(bin_path, "rb") as f:
            encrypted_data = f.read()

        with open(shape_path, "r") as f:
            shape = tuple(map(int, f.read().split(",")))

        key = load_key_hex(key_hex)
        img = decrypt_image(encrypted_data, shape, key)
        if img is None:
            messagebox.showerror("Decryption Failed", "Invalid key or corrupted image.")
            return

        img = img.resize((400, 400))
        win = Toplevel(self.master)
        win.title("Decrypted Image")
        tk_img = ImageTk.PhotoImage(img)
        label = Label(win, image=tk_img)
        label.image = tk_img
        label.pack(pady=20)
