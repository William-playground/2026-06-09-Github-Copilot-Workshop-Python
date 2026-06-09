import tkinter as tk
from tkinter import messagebox
import math

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x500")

        # Config variables
        self.work_time_var = tk.IntVar(value=25)
        self.break_time_var = tk.IntVar(value=5)
        self.theme_var = tk.StringVar(value="Light")
        
        self.sound_start_var = tk.BooleanVar(value=True)
        self.sound_end_var = tk.BooleanVar(value=True)
        self.sound_tick_var = tk.BooleanVar(value=False)
        
        self.timer = None
        self.is_running = False
        self.time_left = 0
        self.mode = "Work" # Work or Break

        self.setup_ui()
        self.apply_theme()
        self.reset_timer()

    def setup_ui(self):
        # Top Frame for Timer
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.timer_frame, text="Work", font=("Helvetica", 24, "bold"))
        self.title_label.pack()

        self.time_label = tk.Label(self.timer_frame, text="25:00", font=("Helvetica", 48, "bold"))
        self.time_label.pack(pady=10)

        # Buttons
        self.btn_frame = tk.Frame(self.timer_frame)
        self.btn_frame.pack()
        
        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.start_timer, width=10)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.reset_btn = tk.Button(self.btn_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_btn.grid(row=0, column=1, padx=5)

        # Settings Frame
        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.pack(pady=10, fill=tk.X, padx=20)

        # Work Time
        tk.Label(self.settings_frame, text="Work Time (min):").grid(row=0, column=0, sticky="w")
        work_frame = tk.Frame(self.settings_frame)
        work_frame.grid(row=0, column=1, sticky="w")
        for val in (15, 25, 35, 45):
            tk.Radiobutton(work_frame, text=str(val), variable=self.work_time_var, value=val, command=self.reset_timer).pack(side=tk.LEFT)

        # Break Time
        tk.Label(self.settings_frame, text="Break Time (min):").grid(row=1, column=0, sticky="w")
        break_frame = tk.Frame(self.settings_frame)
        break_frame.grid(row=1, column=1, sticky="w")
        for val in (5, 10, 15):
            tk.Radiobutton(break_frame, text=str(val), variable=self.break_time_var, value=val).pack(side=tk.LEFT)

        # Theme
        tk.Label(self.settings_frame, text="Theme:").grid(row=2, column=0, sticky="w")
        theme_frame = tk.Frame(self.settings_frame)
        theme_frame.grid(row=2, column=1, sticky="w")
        for val in ("Light", "Dark", "Focus"):
            tk.Radiobutton(theme_frame, text=val, variable=self.theme_var, value=val, command=self.apply_theme).pack(side=tk.LEFT)

        # Sounds
        tk.Label(self.settings_frame, text="Sounds:").grid(row=3, column=0, sticky="w")
        sound_frame = tk.Frame(self.settings_frame)
        sound_frame.grid(row=3, column=1, sticky="w")
        tk.Checkbutton(sound_frame, text="Start", variable=self.sound_start_var).pack(side=tk.LEFT)
        tk.Checkbutton(sound_frame, text="End", variable=self.sound_end_var).pack(side=tk.LEFT)
        tk.Checkbutton(sound_frame, text="Tick", variable=self.sound_tick_var).pack(side=tk.LEFT)

        try:
            self.img = tk.PhotoImage(file="1.pomodoro/pomodoro.png")
            self.img = self.img.subsample(4, 4) # scale down
            self.img_label = tk.Label(self.timer_frame, image=self.img)
            self.img_label.pack(pady=10)
        except Exception:
            pass

    def apply_theme(self):
        theme = self.theme_var.get()
        if theme == "Dark":
            bg_color = "#2E2E2E"
            fg_color = "#FFFFFF"
        elif theme == "Focus":
            bg_color = "#000000"
            fg_color = "#00FF00"
        else: # Light
            bg_color = "#F0F0F0"
            fg_color = "#000000"

        self.root.configure(bg=bg_color)
        self.timer_frame.configure(bg=bg_color)
        self.btn_frame.configure(bg=bg_color)
        self.settings_frame.configure(bg=bg_color)

        self.title_label.configure(bg=bg_color, fg=fg_color)
        self.time_label.configure(bg=bg_color, fg=fg_color)
        if hasattr(self, 'img_label'):
            self.img_label.configure(bg=bg_color)
        
        for widget in self.settings_frame.winfo_children():
            widget.configure(bg=bg_color, fg=fg_color)
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg_color)
                for child in widget.winfo_children():
                    child.configure(bg=bg_color, fg=fg_color)
                    if isinstance(child, tk.Radiobutton) or isinstance(child, tk.Checkbutton):
                        child.configure(selectcolor=bg_color)

    def play_sound(self, sound_type):
        if sound_type == "start" and self.sound_start_var.get():
            self.root.bell()
        elif sound_type == "end" and self.sound_end_var.get():
            self.root.bell()
            self.root.after(500, self.root.bell)
        elif sound_type == "tick" and self.sound_tick_var.get():
            pass # We don't have a small tick sound in tkinter bell, so just pass or log

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.play_sound("start")
            self.count_down()

    def reset_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self.is_running = False
        self.mode = "Work"
        self.time_left = self.work_time_var.get() * 60
        self.update_timer_label()
        self.title_label.config(text="Work")

    def count_down(self):
        if self.time_left > 0:
            self.update_timer_label()
            if self.sound_tick_var.get() and self.time_left % 2 == 0:
                print("tick") # console tick indicator
            self.time_left -= 1
            self.timer = self.root.after(1000, self.count_down)
        else:
            self.is_running = False
            self.update_timer_label()
            self.play_sound("end")
            
            if self.mode == "Work":
                self.mode = "Break"
                self.time_left = self.break_time_var.get() * 60
                self.title_label.config(text="Break")
            else:
                self.mode = "Work"
                self.time_left = self.work_time_var.get() * 60
                self.title_label.config(text="Work")
                
            self.start_timer()

    def update_timer_label(self):
        mins = math.floor(self.time_left / 60)
        secs = self.time_left % 60
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
