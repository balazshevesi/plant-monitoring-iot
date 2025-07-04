from machine import Pin
from dht import DHT11
from .Sensor import Sensor


class HumiditySensor(Sensor):
    def __init__(
        self,
        pin_num,
        topic_suffix="",
        samples_for_average=30,
    ):
        super().__init__(topic_suffix, samples_for_average)
        self.sensor = DHT11(Pin(pin_num))

    def measure(self):
        self.sensor.measure()
        val = self.sensor.humidity()
        self._append_read(val)
        self._last_raw = val

    def raw(self):
        if self._last_raw is None:
            self.measure()
        return self._last_raw
