# pyinstaller --windowed --onefile --name "TimerApp" --icon=icon.ico --add-data "timer2.wav:." Timer_UI.py;

import tkinter as tk
import time
import os
from playsound import playsound

import sys
import os

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

AUDIO_PATH = resource_path("timer2.wav")


class TimerApp:
    def __init__(self, root):
        self.root = root
        root.title("Timer App")
        
        self.always_on_top = True
        self.root.attributes("-topmost", True)

        self.top_button = tk.Button(root, text="Top ON/OFF", command=self.toggle_top)
        self.top_button.grid(row=3, column=0, columnspan=4)

        self.time_left = 0
        self.running = False

        self.time_label = tk.Label(root, font=('Helvetica', 48))
        self.time_label.grid(row=0, column=0, columnspan=4)

        self.start_stop_button = tk.Button(root, text="Start/Stop", command=self.start_stop, width=10)
        self.start_stop_button.grid(row=1, column=0, columnspan=2)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart, width=10)
        self.restart_button.grid(row=1, column=2, columnspan=2)

        self.time_entry = tk.Entry(root, width=10)
        self.time_entry.grid(row=2, column=0, columnspan=2)
        self.time_entry.insert(0, "10")

        self.set_button = tk.Button(root, text="Set", command=self.set_time, width=10)
        self.set_button.grid(row=2, column=2, columnspan=2)

        self.footer = tk.Label(root, text="© 2025 TimerApp by guilhermemartins.net", font=("Helvetica", 11), fg="grey")
        self.footer.grid(row=99, column=0, columnspan=4, sticky="we", pady=5)



    def toggle_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)

        if self.always_on_top:
            self.top_button.config(text="Top: ON")
        else:
            self.top_button.config(text="Top: OFF")


    def set_time(self):
        try:
            minutes = float(self.time_entry.get())
            self.time_left = minutes * 60  # converter para segundos
            self.time_label.config(text=time.strftime("%M:%S", time.gmtime(self.time_left)))
        except:
            self.time_label.config(text="Invalid")

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
            self.time_left = int(minutes * 60)  # minutos -> segundos
            self.time_label.config(
                text=time.strftime("%M:%S", time.gmtime(self.time_left)),
                fg="white"
            )
        except:
            self.time_left = 0
            self.time_label.config(text="Invalid", fg="white")


    def timer(self):
        if self.running:
            time_str = time.strftime("%M:%S", time.gmtime(self.time_left))
            self.time_label.config(text=time_str)

            self.time_left -= 1

            if self.time_left < 0:
                self.running = False
                self.time_label.config(text="Time's Up!", fg="white")
                playsound(AUDIO_PATH)   # caminho para o ficheiro

            else:
                self.root.after(1000, self.timer)

def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
