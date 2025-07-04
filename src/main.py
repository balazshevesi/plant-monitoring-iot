from secrets import (
    AIO_USER,
    AIO_KEY,
    SSID,
    NETWORK_PASS,
    MQTT_BROKER,
    MQTT_PORT,
)

from machine import Pin
from libs.mqtt_client import MQTTClient

from sensors.LightSensor import LightSensor
from sensors.SoilMoistureSensor import SoilMoistureSensor
from sensors.HumiditySensor import HumiditySensor
from sensors.TemperatureSensor import TemperatureSensor
from sensors.Sensor import Sensor

from utils.EventLoop import EventLoop
from utils.EventLoopItem import EventLoopItem
from utils.running_on_pico import running_on_pico
from utils.safe_publish import safe_publish
from utils.get_wlan import get_wlan


EVENT_LOOP_TICK_DURATION_MS = 1000
PUBLISH_TICK_INTERVAL = 30

if not running_on_pico:
    from typing import List

print("Connecting to Wi-Fi...")
wlan = get_wlan(SSID, NETWORK_PASS)

print("Initializing MQTT client...")
client = MQTTClient(
    client_id="pico",
    server=MQTT_BROKER,
    port=MQTT_PORT,
    user=AIO_USER,
    password=AIO_KEY,
    keepalive=60,
)
client.connect()

print("Assigning sensors...")
humidity_sensor = HumiditySensor(
    pin_num=16,
    topic_suffix="feeds/iot.humidity",
    samples_for_average=PUBLISH_TICK_INTERVAL,
)
light_sensor = LightSensor(
    pin_num=28,
    topic_suffix="feeds/iot.brightness",
    samples_for_average=PUBLISH_TICK_INTERVAL,
)
soil_moist_sensor = SoilMoistureSensor(
    pin_num=27,
    topic_suffix="feeds/iot.soil-moisture",
    dry_val=65535,
    wet_val=25000,
    samples_for_average=PUBLISH_TICK_INTERVAL,
)
temp_sensor = TemperatureSensor(
    pin_num=26,
    topic_suffix="feeds/iot.temperature",
    samples_for_average=PUBLISH_TICK_INTERVAL,
)
led = Pin(1, Pin.OUT)

sensors = [
    humidity_sensor,
    light_sensor,
    soil_moist_sensor,
    temp_sensor,
]  # type: List[Sensor]


def measure():
    print("taking measurements...")
    for sensor in sensors:
        sensor.measure()
        print(
            f"  {sensor.__class__.__name__:<20} : "
            f"latest reading = {sensor.get_raw():<12.4f} | "
            f"average (last {sensor.maxlen:2d}) = {sensor.get_average():.4f}"
        )


def publish():
    print("publishing readings...")
    for sensor in sensors:
        topic = f"{AIO_USER}/{sensor.get_topic_suffix()}"
        val = sensor.get_average()
        safe_publish(client, topic, str(val))


print("starting event loop...")
event_loop = EventLoop([], EVENT_LOOP_TICK_DURATION_MS)
event_loop.add_item(EventLoopItem(led.toggle, interval_ticks=1))
event_loop.add_item(EventLoopItem(measure, interval_ticks=1))
event_loop.add_item(EventLoopItem(publish, interval_ticks=PUBLISH_TICK_INTERVAL))
event_loop.start()
