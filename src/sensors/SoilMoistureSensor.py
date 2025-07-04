from machine import Pin, ADC
from .Sensor import Sensor


class SoilMoistureSensor(Sensor):
    def __init__(
        self,
        pin_num,
        topic_suffix="",
        wet_val=25000,
        dry_val=65535,
        samples_for_average=30,
    ):
        super().__init__(topic_suffix, samples_for_average)
        self.adc = ADC(Pin(pin_num))
        self._wet = wet_val
        self._dry = dry_val

    def measure(self):
        val = self.adc.read_u16()
        self._append_read(val)
        self._last_raw = val

    def get_raw(self):
        """
        Returns an int between 0 and 100
        100 means it's submerged in water
        0 means it's completely dry
        """
        if self._last_raw is None:
            self.measure()
        r = self._last_raw
        p = (self._dry - r) / (self._dry - self._wet) * 100
        if p < 0:
            p = 0
        if p > 100:
            p = 100
        return p

    def get_average(self):
        """
        Returns an int between 0 and 100
        100 means it's submerged in water
        0 means it's completely dry
        """
        if not self._reads:
            self.measure()
        avg = super().get_average()
        p = (self._dry - avg) / (self._dry - self._wet) * 100
        if p < 0:
            p = 0
        if p > 100:
            p = 100
        return p
