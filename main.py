import tkinter as tk
from timer import CountdownTimer


class DisappearingTextWriter:
    def __init__(self, root, countdown_start=5, check_interval=1000):
        self.root = root
        self.countdown_start = countdown_start
        self.check_interval = check_interval  # milliseconds
        self.last_text = ""
        self.typing_started = False  # Flag to track if user typed at least once

        self._setup_ui()

        self.timer = CountdownTimer(
            start_seconds=countdown_start,
            tick_callback=self._update_timer_label,
            end_callback=self._clear_text
        )

        self._start_timer()

    def _setup_ui(self):
        self.root.title("Disappearing Text Writer")

        self.text_widget = tk.Text(self.root, wrap="word", font=("Arial", 14))
        self.text_widget.pack(expand=True, fill="both")
        self.text_widget.bind("<Key>", self._on_key_press)

        # Container frame for timer label and its indicator
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.place(relx=1.0, anchor="ne", x=-10, y=10)

        # Static label indicating the timer
        self.timer_indicator_label = tk.Label(self.timer_frame, text="Timer:", font=("Arial", 12), fg="black")
        self.timer_indicator_label.pack(side="left")

        # Dynamic label showing countdown seconds
        self.timer_label = tk.Label(self.timer_frame, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(side="left")

    def _on_key_press(self, event):
        if not self.typing_started:
            self.typing_started = True
            self.timer.reset()  # Start timer countdown after first key press
        else:
            self.timer.reset()

    def _update_timer_label(self, seconds_left):
        self.timer_label.config(text=str(seconds_left) if self.typing_started else "")

    def _clear_text(self):
        self.text_widget.delete("1.0", "end")
        self.typing_started = False  # Reset flag after clearing text
        self.timer_label.config(text="")  # Hide timer label until typing restarts

    def _check_typing(self):
        current_text = self.text_widget.get("1.0", "end-1c")
        if not self.typing_started:
            # Timer does not run until user types at least once
            self.last_text = current_text
            return

        if current_text != self.last_text:
            self.timer.reset()
        else:
            self.timer.tick()
        self.last_text = current_text

    def _start_timer(self):
        self._check_typing()
        self.root.after(self.check_interval, self._start_timer)


if __name__ == "__main__":
    root = tk.Tk()
    app = DisappearingTextWriter(root)
    root.mainloop()