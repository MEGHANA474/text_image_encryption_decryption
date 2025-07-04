from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
from crypto_utils import generate_key, encrypt_text, encrypt_image, save_key_hex
from access_control import grant_access, log_access

class OwnerWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Owner Panel")
        self.frame = Frame(self.master, padx=50, pady=50)
        self.frame.pack(fill="both", expand=True)

        Label(self.frame, text="Owner Dashboard", font=("Arial", 24, "bold")).pack(pady=20)

        Button(self.frame, text="Encrypt Text", font=("Arial", 16), width=25, command=self.encrypt_text).pack(pady=10)
        Button(self.frame, text="Encrypt Image", font=("Arial", 16), width=25, command=self.encrypt_image).pack(pady=10)
        Button(self.frame, text="Grant Access to User", font=("Arial", 16), width=25, command=self.grant_access_ui).pack(pady=10)
        Button(self.frame, text="Close", font=("Arial", 14), command=self.master.destroy).pack(pady=20)

    def encrypt_text(self):
        text = simpledialog.askstring("Text Input", "Enter text to encrypt:")
        if not text: return
        key = generate_key()
        encrypted = encrypt_text(text, key)
        filename = simpledialog.askstring("Save File", "Enter filename (e.g. note1.txt):")
        if not filename: return

        with open(f"data/encrypted/{filename}", "w") as f:
            f.write(encrypted)

        grant_access(filename, "owner", save_key_hex(key))
        log_access("owner", filename, "owner")
        messagebox.showinfo("Success", f"Encrypted text saved as {filename}")

    def encrypt_image(self):
        path = filedialog.askopenfilename(title="Select an image file")
        if not path: return
        key = generate_key()
        encrypted_data, shape = encrypt_image(path, key)
        name = simpledialog.askstring("Save Image", "Enter name for encrypted image:")
        if not name: return

        enc_path = f"data/encrypted/{name}.bin"
        with open(enc_path, "wb") as f:
            f.write(encrypted_data)

        shape_path = enc_path + ".shape"
        with open(shape_path, "w") as f:
            f.write(','.join(map(str, shape)))

        grant_access(name, "owner", save_key_hex(key))
        log_access("owner", name, "owner")
        messagebox.showinfo("Success", f"Encrypted image saved as {name}.bin")

    def grant_access_ui(self):
        filename = simpledialog.askstring("Filename", "Enter file name to share:")
        username = simpledialog.askstring("Username", "Enter user to grant access to:")
        from access_control import get_key_if_allowed
        key_hex = get_key_if_allowed(filename, "owner")
        if not key_hex:
            messagebox.showerror("Error", "You do not have access to that file.")
            return
        grant_access(filename, username, key_hex)
        log_access("owner", filename, username)
        messagebox.showinfo("Granted", f"Access granted to {username} for {filename}")
