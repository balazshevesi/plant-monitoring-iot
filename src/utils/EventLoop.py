import time
from EventLoopItem import EventLoopItem

TICK_MODULO = 65536


class EventLoop:
    def __init__(self, items: list[EventLoopItem], tick_interval_ms: int = 1000):
        self.items = items
        self.tick_interval = tick_interval_ms / 1000
        self.running = False
        self.tick_count = 0

    def add_item(self, item: EventLoopItem):
        self.items.append(item)

    def start(self):
        self.running = True
        self.tick_count = 0
        while self.running:
            for item in self.items:
                item.execute(self.tick_count)
            self.tick_count = (self.tick_count + 1) % TICK_MODULO
            time.sleep(self.tick_interval)

    def stop(self):
        self.running = False
