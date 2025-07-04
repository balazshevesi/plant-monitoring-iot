import time
import network
from secrets import (
    AIO_USER,
    AIO_KEY,
    SSID,
    NETWORK_PASS,
    MQTT_BROKER,
    MQTT_PORT,
)


def get_wlan(ssid: str, network_pass: str):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, network_pass)

    timeout = 10  # seconds
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            raise RuntimeError("Wi-Fi connection failed")
        time.sleep(0.5)
    return wlan
