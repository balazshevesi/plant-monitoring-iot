from ucollections import deque


class Sensor:
    """Sensor superclass"""

    def __init__(self, topic_suffix="", samples_for_average=30):
        self._topic_suffix = topic_suffix
        self.maxlen = samples_for_average
        self._reads = deque([], samples_for_average)
        self._last_raw = None

    def get_topic_suffix(self):
        return self._topic_suffix

    def get_raw(self):
        if self._last_raw is None:
            self.measure()
        return self._last_raw

    def get_average(self):
        if not self._reads:
            self.measure()
        return sum(self._reads) / len(self._reads)

    def _append_read(self, value):
        self._reads.append(value)

    def measure(self):
        raise NotImplementedError("Subclasses must implement measure()")
