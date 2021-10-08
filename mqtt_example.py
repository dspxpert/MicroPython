from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import os, time, network

SERVER = '121.129.42.234' # MQTT Server Address
CLIENT_ID = 'ESP8266_Sensor'
PUB_TOPIC = b'led1'
SUB_TOPIC = b'led2'

LED_PIN = 2
BUTTON_PIN = 12

# WeMos D1-mini Pin map
# RST        1 TX
# A0         3 RX
# 16 D0      5 D1 SCL
# 14 D5      4 D2 SDA
# 12 D6      0 D3
# 13 D7      2 D4 (Built-in LED Active Low)
# 15 D8        GND

# WeMos D1-mini Built-in LED(GPIO2) active low
state = 1
led = Pin(LED_PIN, Pin.OUT, value=state)

def wifi_setup(ssid='JD-iPhoneSE2', password='7075443332'):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to Network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Network Config:', sta_if.ifconfig())

def sub_cb(topic, msg):
    global state, led

    print((topic, msg))
    if msg == b"on":
        state = 0
        led.value(state)
    elif msg == b"off":
        state = 1
        led.value(state)
    elif msg == b"toggle":
        state = 1 - state
        led.value(state)

def main(server=SERVER):
    global state, led
    
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
    prev_button = 1
    client = MQTTClient(CLIENT_ID, SERVER)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(SUB_TOPIC)
    
    state = 0
    led.value(state)
    
    try:
        while True:
            client.check_msg()
            if button.value() != prev_button:
                prev_button = button.value()
                if prev_button == 0:
                    client.publish(PUB_TOPIC, b"toggle")
                    print("Button press - led1 toggle sent.")
                    time.sleep(0.05)
                #else:
                #    client.publish(PUB_TOPIC, b"off")
                #    print("pin12 off")
    finally:
        client.disconnect()

wifi_setup()
#wifi_setup('cellion2G', 'cellion2g')
main()
