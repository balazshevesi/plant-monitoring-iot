TICK_MODULO = 65536


class EventLoopItem:
    def __init__(self, callback, interval_ticks: int = 1):
        self.callback = callback
        self.interval = interval_ticks
        self.last_run_tick = 0

    def execute(self, current_tick: int):
        if (current_tick - self.last_run_tick) % TICK_MODULO >= self.interval:
            self.callback()
            self.last_run_tick = current_tick
