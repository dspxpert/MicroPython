from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import os, time, network

def network_setup():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to Network...')
        sta_if.connect('freecafe_02', 'freecafe00')
        while not sta_if.isconnected():
            pass
    print('Network Config:', sta_if.ifconfig())

SERVER = '172.30.1.28' # MQTT Server Address
CLIENT_ID = 'ESP32_Sensor'
PUB_TOPIC = b'button'
SUB_TOPIC = b'led'

# WeMos D1-mini Built-in LED(GPIO2) active low
# default off == 1 (initial state)

led = Pin(22, Pin.OUT, value=1)
state = 0

def sub_cb(topic, msg):
    global state, led
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
    elif msg == b"off":
        led.value(1)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state

def main(server=SERVER):

    button = Pin(12, Pin.IN, Pin.PULL_UP)
    prev_button = 1
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
                    print("pin12 on")
                else:
                    client.publish(PUB_TOPIC, b"off")
		    print("pin12 off")
    finally:
        client.disconnect()

network_setup()
main()
