import tkinter as tk
from tkinter import messagebox
import time
import winsound
from threading import Thread

class HydrationReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydration Reminder")
        self.root.geometry("300x200")  # Adjust window size
        self.root.configure(bg="white")  # Set background to white

        # Default countdown time (600 seconds = 10 minutes)
        self.countdown_time = 600
        self.is_running = False  # Flag to check if the timer is running
        self.input_seconds = tk.StringVar(value=str(self.countdown_time))  # Hold the last input

        # Title label with a custom font
        self.title_label = tk.Label(root, text="Stay Hydrated!", font=("Comic Sans MS", 18, "bold"), bg='white')
        self.title_label.pack(pady=10)

        # Input field for countdown time
        self.input_label = tk.Label(root, text="Enter time in seconds:", bg='white')
        self.input_label.pack(pady=5)
        self.input_entry = tk.Entry(root, textvariable=self.input_seconds, font=("Helvetica", 12))
        self.input_entry.pack(pady=5)
        
        # Button to set the countdown time
        self.set_button = tk.Button(root, text="Set Reminder", command=self.set_timer)
        self.set_button.pack(pady=5)

        # Countdown label (initially hidden)
        self.timer_label = tk.Label(root, text=f"Next reminder in {self.countdown_time} seconds", font=("Helvetica", 12), bg='white')
        
        # Progress bar (initially hidden)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.ttk.Progressbar(root, maximum=self.countdown_time, variable=self.progress_var)

        # Button to change timer when the timer is running (initially hidden)
        self.change_timer_button = tk.Button(root, text="Change Timer", command=self.reset_ui)

    def set_timer(self):
        try:
            self.countdown_time = int(self.input_seconds.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return
        
        # Hide the input field and set button, show the timer and progress bar
        self.input_entry.pack_forget()
        self.input_label.pack_forget()
        self.set_button.pack_forget()

        self.timer_label.config(text=f"Next reminder in {self.countdown_time} seconds")
        self.timer_label.pack(pady=5)
        self.progress_bar.pack(pady=5, padx=20, fill='x')
        self.change_timer_button.pack(pady=5)  # Show the change timer button

        self.is_running = True  # Set the running flag to true
        self.start_countdown()

    def start_countdown(self):
        def countdown():
            remaining_time = self.countdown_time
            self.progress_var.set(remaining_time)
            while remaining_time > 0 and self.is_running:
                time.sleep(1)
                remaining_time -= 1
                self.progress_var.set(remaining_time)
                self.timer_label.config(text=f"Next reminder in {remaining_time} seconds")

                if remaining_time <= 0:
                    self.show_reminder()
                    return  # Exit the countdown once the reminder is shown

        countdown_thread = Thread(target=countdown)
        countdown_thread.start()

    def show_reminder(self):
        # Create a topmost window for the alert
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Reminder")
        reminder_window.geometry("300x100")
        reminder_window.configure(bg="white")
        reminder_window.attributes("-topmost", True)  # Make sure the window stays on top

        # Label to display the reminder message
        label = tk.Label(reminder_window, text="Remember to drink water!", font=("Helvetica", 14), bg='white')
        label.pack(pady=20)

        # Button to close the reminder window and restart the timer
        button = tk.Button(reminder_window, text="OK", command=lambda: self.close_reminder(reminder_window))
        button.pack(pady=5)

        # Play 3 beeps with a 3-second interval while the alert window is visible
        beep_thread = Thread(target=self.play_beeps)
        beep_thread.start()

    def play_beeps(self):
        # This will beep 3 times with a 3-second pause between each beep
        for _ in range(3):
            winsound.Beep(1000, 1000)  # Frequency of 1000 Hz for 1 second
            time.sleep(3)

    def close_reminder(self, window):
        window.destroy()  # Close the reminder window
        self.is_running = True  # Set the flag to continue running
        self.start_countdown()  # Restart the countdown

    def reset_ui(self):
        # Stop the current timer
        self.is_running = False

        # Hide the timer and progress bar, show the input fields again
        self.timer_label.pack_forget()
        self.progress_bar.pack_forget()
        self.change_timer_button.pack_forget()

        self.input_entry.pack(pady=5)
        self.input_label.pack(pady=5)
        self.set_button.pack(pady=5)
        self.input_seconds.set(str(self.countdown_time))  # Reset the input field to the last used time


# Main application window
if __name__ == "__main__":
    import tkinter.ttk as ttk
    root = tk.Tk()
    app = HydrationReminderApp(root)
    root.mainloop()
