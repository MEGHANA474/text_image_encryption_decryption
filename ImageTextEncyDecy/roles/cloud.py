# File: roles/cloud.py

from tkinter import *
from access_control import view_log

class CloudWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Cloud Viewer")
        self.frame = Frame(self.master, padx=50, pady=40)
        self.frame.pack(fill="both", expand=True)

        Label(self.frame, text="Cloud Viewer - Encrypted Sharing Log", font=("Arial", 24, "bold")).pack(pady=20)

        text_area = Text(self.frame, width=80, height=25, font=("Courier", 12))
        text_area.pack(pady=20)

        logs = view_log()
        for log in logs:
            line = f"[{log['timestamp']}] {log['owner']} shared '{log['filename']}' with {log['shared_with']}\n"
            text_area.insert(END, line)

        Button(self.frame, text="Close", font=("Arial", 14), command=self.master.destroy).pack(pady=10)
