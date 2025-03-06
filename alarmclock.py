import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Canvas
from datetime import datetime
import time
import threading
import random
import os
import playsound
import math

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Alarm Clock")
        self.root.geometry("700x750")  # Increased size for better visibility
        
        self.alarms = []
        self.alarm_sounds = {}
        self.snooze_time = 5
        self.dark_mode = False
        
        # Color Themes with Gradient
        self.light_theme = {'bg': '#2C2F33', 'fg': '#FFFFFF'}  # Grey background with white text
        self.dark_theme = {'bg': '#191970', 'fg': '#00FFFF'}  # Dark navy with neon white-blue
        
        self.current_theme = self.light_theme
        self.apply_theme()
        
        # Heading
        self.heading = tk.Label(self.root, text="Alarm Clock", font=("Arial", 22, "bold"), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.heading.pack(pady=15)
        
        # Analog Clock Canvas
        self.canvas = Canvas(self.root, width=250, height=250, bg=self.current_theme['bg'], highlightthickness=0)
        self.canvas.pack(pady=15)
        self.update_clock()
        
        # Time input
        self.time_label = tk.Label(self.root, text="Set Alarm (HH:MM:SS):", fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.time_label.pack()
        self.time_entry = tk.Entry(self.root, font=("Arial", 16), width=15)
        self.time_entry.pack(pady=5)
        
        # Sound Picker
        self.sound_label = tk.Label(self.root, text="Select Sound:", fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.sound_label.pack()
        self.sound_button = tk.Button(self.root, text="Choose File", command=self.choose_sound)
        self.sound_button.pack()
        
        # Add Alarm Button
        self.add_alarm_button = tk.Button(self.root, text="Add Alarm", command=self.add_alarm)
        self.add_alarm_button.pack(pady=5)
        
        # Alarm List
        self.alarm_listbox = tk.Listbox(self.root, width=50, height=12)
        self.alarm_listbox.pack(pady=15)
        
        # Theme Toggle Button
        self.theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=5)
        
        # Start Alarm Thread
        self.check_alarm_thread = threading.Thread(target=self.check_alarm, daemon=True)
        self.check_alarm_thread.start()
    
    def apply_theme(self):
        self.root.configure(bg=self.current_theme['bg'])
    
    def choose_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.alarm_sounds[self.time_entry.get()] = file_path
            messagebox.showinfo("Success", "Alarm sound selected!")
    
    def add_alarm(self):
        alarm_time = self.time_entry.get()
        if alarm_time:
            self.alarms.append(alarm_time)
            self.alarm_listbox.insert(tk.END, alarm_time)
    
    def check_alarm(self):
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            if now in self.alarms:
                self.trigger_alarm(now)
            time.sleep(1)
    
    def trigger_alarm(self, alarm_time):
        sound_file = self.alarm_sounds.get(alarm_time, None)
        if sound_file:
            threading.Thread(target=playsound.playsound, args=(sound_file,), daemon=True).start()
        
        # Puzzle to stop alarm
        self.solve_puzzle(alarm_time)
    
    def solve_puzzle(self, alarm_time):
        puzzle_window = tk.Toplevel(self.root)
        puzzle_window.title("Solve the Puzzle")
        puzzle_window.geometry("350x200")
        
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        answer = num1 + num2
        
        puzzle_label = tk.Label(puzzle_window, text=f"Solve: {num1} + {num2} = ?", font=("Arial", 14))
        puzzle_label.pack(pady=10)
        
        puzzle_entry = tk.Entry(puzzle_window, font=("Arial", 14), width=10)
        puzzle_entry.pack(pady=5)
        
        def check_answer():
            if puzzle_entry.get().isdigit() and int(puzzle_entry.get()) == answer:
                puzzle_window.destroy()
                if alarm_time in self.alarms:
                    self.alarms.remove(alarm_time)
                    self.alarm_listbox.delete(0, tk.END)
                    for alarm in self.alarms:
                        self.alarm_listbox.insert(tk.END, alarm)
            else:
                messagebox.showerror("Wrong Answer", "Try again!")
        
        submit_button = tk.Button(puzzle_window, text="Submit", font=("Arial", 12), command=check_answer)
        submit_button.pack(pady=10)
    
    def toggle_theme(self):
        self.current_theme = self.light_theme if self.current_theme == self.dark_theme else self.dark_theme
        self.apply_theme()
        self.heading.configure(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.time_label.configure(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.sound_label.configure(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
        self.theme_button.configure(bg=self.current_theme['bg'], fg=self.current_theme['fg'])
    
    def update_clock(self):
        self.canvas.delete("all")
        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second
        
        def draw_hand(angle, length, color):
            x = 125 + length * math.cos(math.radians(angle - 90))
            y = 125 + length * math.sin(math.radians(angle - 90))
            self.canvas.create_line(125, 125, x, y, fill=color, width=3)
        
        self.canvas.create_oval(25, 25, 225, 225, outline=self.current_theme['fg'], width=2)
        draw_hand(hour * 30 + minute * 0.5, 50, "red")
        draw_hand(minute * 6, 70, "blue")
        draw_hand(second * 6, 90, "green")
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()