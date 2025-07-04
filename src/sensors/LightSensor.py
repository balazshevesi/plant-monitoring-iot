from machine import Pin, ADC
from .Sensor import Sensor


class LightSensor(Sensor):
    def __init__(self, pin_num, topic_suffix="", samples_for_average=30):
        super().__init__(topic_suffix, samples_for_average)
        self.adc = ADC(Pin(pin_num))

    def measure(self):
        val = self.adc.read_u16()
        self._append_read(val)
        self._last_raw = val

    def raw(self):
        if self._last_raw is None:
            self.measure()
        return self._last_raw
