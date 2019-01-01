from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython

SERVER = '172.30.1.28' # MQTT Server Address
CLIENT_ID = 'ESP32_Sensor'
PUB_TOPIC = b'button'
SUB_TOPIC = b'led'

led = Pin(12, Pin.OUT, value=0)
state = 0

button = Pin(2, Pin.IN, Pin.PULL_UP)
prev_button = 1

def sub_cb(topic, msg):
    global state, led
    print((topic, msg))
    if msg == b"on":
        led.value(1)
        state = 0
    elif msg == b"off":
        led.value(0)
        state = 1
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state

def main(server=SERVER):
    global button, prev_button
    client = MQTTClient(CLIENT_ID, SERVER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(SUB_TOPIC)

    try:
        while True:
            client.check_msg()
            if button.value() != prev_button:
                prev_button = button.value()
                if prev_button == 0:
                    client.publish(PUB_TOPIC, b"on")
                else:
                    client.publish(PUB_TOPIC, b"off")
    finally:
        client.disconnect()
