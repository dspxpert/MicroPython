# MicroPython
MicroPython Projects

>1. Firmware Flashing<br>
>esptool -p COMxx erase_flash<br>
>
>esptool -p COMxx write_flash 0 firmware.bin (for ESP8266)<br>
>esptool -p COMxx write_flash -z 0x1000 firmware.bin (for ESP32)<br>
>
>2. Network Connection
>main.py
>import os, time, network
>def network_setup():
>    sta_if = network.WLAN(network.STA_IF)
>    sta_if.active(True)
>    if not sta_if.isconnected():
>        print('Connecting to Network...')
>        sta_if.connect('freecafe_02', 'freecafe00')
>        while not sta_if.isconnected():
>            pass
>    print('Network Config:', sta_if.ifconfig())
>
>3. Setup WebREPL
>import webrepl_setup
>
>4. MQTT example
>
