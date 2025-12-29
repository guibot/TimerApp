# pip install pyinstaller
# mac:
# pyinstaller --windowed --onefile --name "DailyTimer" --icon=icon.ico --add-data "timer1.wav:." --add-data "timer2.wav:." Daily_Timer.py
# windows:
# pyinstaller --windowed --onefile --name "DailyTimer" --icon=icon.ico  --add-data "timer1.wav;."  --add-data "timer2.wav;." Daily_Timer.py

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

AUDIO_PATH  = resource_path("timer1.wav")
AUDIO2_PATH = resource_path("timer2.wav")

# --------------------------------------------------
# Colors
# --------------------------------------------------
TIMER1_COLOR = "red"
TIMER2_COLOR = "green"
TIMERS_IDLE  = "#444444"   # dark grey

# --------------------------------------------------
# Layout sizes
# --------------------------------------------------
WIDTH_WINDOW = 260
HEIGHT_WINDOW = 200

WIDTH_LEFT_COLUMN  = 10   # px
WIDTH_RIGHT_COLUMN = 10   # px

INPUT_FIELD_WIDTH  = 3     # chars
SET_BUTTON_WIDTH   = 8    # chars

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
        # ---------------- State ----------------
        self.repeat = False
        self.base_time = 0

        self.second_time = 0
        self.second_base_time = 0
        self.in_second_timer = False

        self.root = root
        root.title("DailyTimer")
        #root.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}")
        root.resizable(False, False)

        self.always_on_top = True
        self.root.attributes("-topmost", True)

        self.time_left = 0
        self.running = False
        self.volume = 0.1

        # ---------------- Grid ----------------
        # Left side (actions) – 2 colunas
        root.grid_columnconfigure(0, minsize=WIDTH_LEFT_COLUMN // 2)
        root.grid_columnconfigure(1, minsize=WIDTH_LEFT_COLUMN // 2)

        # Right side (input + set) – 2 colunas
        root.grid_columnconfigure(2, minsize=WIDTH_RIGHT_COLUMN // 3)
        root.grid_columnconfigure(3, minsize=(WIDTH_RIGHT_COLUMN * 2) // 3)

        # ---------------- Timer label ----------------
        self.time_label = tk.Label(root, font=("Menlo", 42))
        self.time_label.grid(row=0, column=0, columnspan=4)

        # ---------------- Indicators ----------------
        self.indicator_frame = tk.Frame(root)
        self.indicator_frame.grid(row=0, column=3, sticky="e", padx=(5, 0))

        self.indicator_1 = tk.Label(self.indicator_frame, width=2, height=1, bg=TIMER1_COLOR)
        self.indicator_1.pack(pady=2)

        self.indicator_2 = tk.Label(self.indicator_frame, width=2, height=1, bg=TIMERS_IDLE)
        self.indicator_2.pack(pady=2)

        # ---------------- ROW 1 ----------------
        self.start_stop_button = tk.Button(
            root, text="Start / Stop", command=self.start_stop, width=10
        )
        self.start_stop_button.grid(row=1, column=0, columnspan=2, sticky="we")

        self.time_entry = tk.Entry(root, width=INPUT_FIELD_WIDTH)
        self.time_entry.grid(row=1, column=2)
        self.time_entry.insert(0, "30")

        self.set_button = tk.Button(
            root, text="Set 1st Timer", command=self.set_time, width=SET_BUTTON_WIDTH
        )
        self.set_button.grid(row=1, column=3)

        # ---------------- ROW 2 ----------------
        self.restart_button = tk.Button(
            root, text="Restart", command=self.restart, width=10
        )
        self.restart_button.grid(row=2, column=0, columnspan=2, sticky="we")

        self.second_time_entry = tk.Entry(root, width=INPUT_FIELD_WIDTH)
        self.second_time_entry.grid(row=2, column=2)
        self.second_time_entry.insert(0, "5")

        self.second_set_button = tk.Button(
            root, text="Set 2nd Timer", command=self.set_second_timer, width=SET_BUTTON_WIDTH
        )
        self.second_set_button.grid(row=2, column=3)

        # ---------------- ROW 3 ----------------
        self.repeat_button = tk.Button(
            root, text="Repeat: OFF", command=self.toggle_repeat, width=10
        )
        self.repeat_button.grid(row=3, column=0, columnspan=2, sticky="we")

        self.volume_entry = tk.Entry(root, width=INPUT_FIELD_WIDTH)
        self.volume_entry.grid(row=3, column=2)
        self.volume_entry.insert(0, "0.1")

        self.volume_set_button = tk.Button(
            root, text="Set Volume", command=self.set_volume, width=SET_BUTTON_WIDTH
        )
        self.volume_set_button.grid(row=3, column=3)

        # ---------------- ROW 4 ----------------
        self.top_button = tk.Button(
            root, text="Top: ON", command=self.toggle_top, width=10
        )
        self.top_button.grid(row=4, column=0, columnspan=2, sticky="we")

        # ---------------- Footer ----------------
        self.footer = tk.Label(
            root,
            text="© 2025 TimerApp by guilhermemartins.net",
            font=("Helvetica", 11),
            fg="grey"
        )
        self.footer.grid(row=99, column=0, columnspan=4, sticky="we", pady=5)

        # ---------------- Initial state ----------------
        self.show_timer_1()
        self.set_time()

    # --------------------------------------------------
    # Controls
    # --------------------------------------------------
    def toggle_repeat(self):
        self.repeat = not self.repeat
        self.repeat_button.config(text="Repeat: ON" if self.repeat else "Repeat: OFF")

    def toggle_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        self.top_button.config(text="Top: ON" if self.always_on_top else "Top: OFF")

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

    def set_time(self):
        self.in_second_timer = False
        self.show_timer_1()
        try:
            minutes = float(self.time_entry.get())
            self.base_time = int(minutes * 60)
            self.time_left = self.base_time
            self.time_label.config(
                text=time.strftime("%M:%S", time.gmtime(self.time_left)), fg="white"
            )
        except:
            self.time_label.config(text="Invalid", fg="white")

    def restart(self):
        self.running = False
        self.in_second_timer = False
        self.show_timer_1()
        try:
            minutes = float(self.time_entry.get())
            self.base_time = int(minutes * 60)
            self.time_left = self.base_time
            self.time_label.config(
                text=time.strftime("%M:%S", time.gmtime(self.time_left)), fg="white"
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
            if not self.in_second_timer:
                play_audio(AUDIO_PATH, self.volume)
                if self.second_base_time > 0:
                    self.in_second_timer = True
                    self.time_left = self.second_base_time
                    self.show_timer_2()
                    self.root.after(1000, self.timer)
                    return
            else:
                play_audio(AUDIO2_PATH, self.volume)
                self.in_second_timer = False

            if self.repeat:
                self.time_left = self.base_time
                self.show_timer_1()
                self.root.after(1000, self.timer)
            else:
                self.running = False
                self.time_label.config(text="Time's Up!", fg="white")
        else:
            self.root.after(1000, self.timer)

    def set_second_timer(self):
        try:
            minutes = float(self.second_time_entry.get())
            self.second_base_time = int(minutes * 60)
            self.second_time = self.second_base_time
        except:
            self.second_base_time = 0
            self.second_time = 0

    def show_timer_1(self):
        self.indicator_1.config(bg=TIMER1_COLOR)
        self.indicator_2.config(bg=TIMERS_IDLE)

    def show_timer_2(self):
        self.indicator_1.config(bg=TIMERS_IDLE)
        self.indicator_2.config(bg=TIMER2_COLOR)

# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    root = tk.Tk()
    TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
