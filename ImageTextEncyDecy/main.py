import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from roles.owner import OwnerWindow
from roles.cloud import CloudWindow
from roles.user import UserWindow


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Image and Text Sharing Platform")
        
        # Set window to full screen
        self.root.state('zoomed')

        # Main frame with padding
        frame = tk.Frame(root, padx=50, pady=50)
        frame.pack(expand=True, fill="both")

        title = tk.Label(frame, text="Secure Image and Text Sharing", font=("Arial", 36, "bold"))
        title.pack(pady=(40, 60))

        # Role Buttons
        btn_owner = tk.Button(frame, text="Owner", font=("Arial", 24), width=20, height=2, command=self.open_owner)
        btn_cloud = tk.Button(frame, text="Cloud Provider", font=("Arial", 24), width=20, height=2, command=self.open_cloud)
        btn_user = tk.Button(frame, text="User", font=("Arial", 24), width=20, height=2, command=self.open_user)

        btn_owner.pack(pady=30)
        btn_cloud.pack(pady=30)
        btn_user.pack(pady=30)

        footer = tk.Label(frame, text="Built with ❤️ using Python", font=("Arial", 14))
        footer.pack(side="bottom", pady=20)

    def open_owner(self):
        new_window = tk.Toplevel(self.root)
        OwnerWindow(new_window)

    def open_cloud(self):
        new_window = tk.Toplevel(self.root)
        CloudWindow(new_window)

    def open_user(self):
        new_window = tk.Toplevel(self.root)
        UserWindow(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
