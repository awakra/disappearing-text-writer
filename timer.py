class CountdownTimer:
    def __init__(self, start_seconds, tick_callback=None, end_callback=None):
        self.start_seconds = start_seconds
        self.seconds_left = start_seconds
        self.tick_callback = tick_callback  # Called every tick with seconds_left
        self.end_callback = end_callback    # Called when timer reaches zero

    def reset(self):
        self.seconds_left = self.start_seconds
        self._notify_tick()

    def tick(self):
        self.seconds_left -= 1
        self._notify_tick()
        if self.seconds_left <= 0:
            if self.end_callback:
                self.end_callback()
            self.reset()

    def _notify_tick(self):
        if self.tick_callback:
            self.tick_callback(self.seconds_left)