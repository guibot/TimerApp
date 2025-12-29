# pyinstaller --windowed --onefile --name "TimerApp" --icon=icon.ico --add-data "timer2.wav:." Timer_UI.py

import tkinter as tk
import time
import sys
import os
import subprocess

# --------------------------------------------------
# Resource path (PyInstaller compatible)
# --------------------------------------------------
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

AUDIO_PATH = resource_path("timer2.wav")

# --------------------------------------------------
# Audio (macOS)
# --------------------------------------------------
def play_audio(path, volume):
    vol = max(0.0, min(volume / 10.0, 1.0))  # 0–10 -> 0.0–1.0
    subprocess.Popen(["afplay", path, "-v", str(vol)])

# --------------------------------------------------
# App
# --------------------------------------------------
class TimerApp:
    def __init__(self, root):
        self.repeat = False
        self.base_time = 0

        self.root = root
        root.title("Timer App")

        # Always on top
        self.always_on_top = True
        self.root.attributes("-topmost", True)

        # State
        self.time_left = 0
        self.running = False
        self.volume = 0.1

        # --------------------------------------------------
        # UI
        # --------------------------------------------------
        self.time_label = tk.Label(root, font=("Helvetica", 48))
        self.time_label.grid(row=0, column=0, columnspan=4)

        self.start_stop_button = tk.Button(
            root, text="Start / Stop", command=self.start_stop, width=10
        )
        self.start_stop_button.grid(row=1, column=0, columnspan=2)

        self.restart_button = tk.Button(
            root, text="Restart", command=self.restart, width=10
        )
        self.restart_button.grid(row=1, column=2, columnspan=2)

        self.time_entry = tk.Entry(root, width=10)
        self.time_entry.grid(row=2, column=0, columnspan=2)
        self.time_entry.insert(0, "10")

        self.set_button = tk.Button(
            root, text="Set", command=self.set_time, width=10
        )
        self.set_button.grid(row=2, column=2, columnspan=2)

        # Always on top toggle
        self.top_button = tk.Button(
            root, text="Top: ON", command=self.toggle_top, width=10
        )
        self.top_button.grid(row=3, column=0, columnspan=2, sticky="we")


        # Volume input
        self.volume_entry = tk.Entry(root, width=3)
        self.volume_entry.grid(row=3, column=2)
        self.volume_entry.insert(0, "0.1")

        self.volume_set_button = tk.Button(
            root, text="Set Volume", command=self.set_volume, width=7
        )
        self.volume_set_button.grid(row=3, column=3)

        # Footer
        self.footer = tk.Label(
            root,
            text="© 2025 TimerApp by guilhermemartins.net",
            font=("Helvetica", 11),
            fg="grey"
        )
        self.footer.grid(row=99, column=0, columnspan=4, sticky="we", pady=5)

        for i in range(4):
            root.grid_columnconfigure(i, weight=0)

        self.repeat_button = tk.Button(
         root, text="Repeat: OFF", command=self.toggle_repeat, width=10
        )
        self.repeat_button.grid(row=4, column=0, columnspan=2, sticky="we")



    # --------------------------------------------------
    # Controls
    # --------------------------------------------------

    def toggle_repeat(self):
        self.repeat = not self.repeat
        self.repeat_button.config(
            text="Repeat: ON" if self.repeat else "Repeat: OFF"
        )


    def toggle_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        self.top_button.config(text="Top: ON" if self.always_on_top else "Top: OFF")

    def set_time(self):
        try:
            minutes = float(self.time_entry.get())
            self.base_time = int(minutes * 60)
            self.time_left = self.base_time
            self.time_label.config(
                text=time.strftime("%M:%S", time.gmtime(self.time_left)),
                fg="white"
            )
        except:
            self.time_label.config(text="Invalid", fg="white")

    def set_volume(self):
        try:
            v = float(self.volume_entry.get())
            if 0 <= v <= 10:
                self.volume = v
            else:
                raise ValueError
        except:
            self.volume_entry.delete(0, tk.END)
            self.volume_entry.insert(0, "0-10")

    def start_stop(self):
        if self.running:
            self.running = False
            self.time_label.config(text="Stopped", fg="white")
        else:
            self.running = True
            self.time_label.config(fg="white")
            self.timer()

    def restart(self):
        self.running = False
        try:
            minutes = float(self.time_entry.get())
            self.base_time = int(minutes * 60)
            self.time_left = self.base_time
            self.time_label.config(
                text=time.strftime("%M:%S", time.gmtime(self.time_left)),
                fg="white"
            )
        except:
            self.time_left = 0
            self.time_label.config(text="Invalid", fg="white")

    def timer(self):
        if not self.running:
            return

        self.time_label.config(
            text=time.strftime("%M:%S", time.gmtime(self.time_left))
        )

        self.time_left -= 1

        if self.time_left < 0:
            play_audio(AUDIO_PATH, self.volume)

            if self.repeat:
                self.time_left = self.base_time
                self.root.after(1000, self.timer)
            else:
                self.running = False
                self.time_label.config(text="Time's Up!", fg="white")
        else:
            self.root.after(1000, self.timer)


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    root = tk.Tk()
    TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
