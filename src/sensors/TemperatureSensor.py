from machine import Pin, ADC
from .Sensor import Sensor


class TemperatureSensor(Sensor):
    def __init__(self, pin_num, topic_suffix="", samples_for_average=30):
        super().__init__(topic_suffix, samples_for_average)
        self.adc = ADC(Pin(pin_num))

    def measure(self):
        raw = self.adc.read_u16()
        voltage = raw / 65535 * 3.3
        temp = (voltage * 1000 - 500) / 10
        self._append_read(temp)
        self._last_raw = temp

    def raw(self):
        if self._last_raw is None:
            self.measure()
        return self._last_raw

    def get_average(self):
        if not self._reads:
            self.measure()
        return sum(self._reads) / len(self._reads)
