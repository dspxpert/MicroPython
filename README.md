# MicroPython
MicroPython Projects

>1. Firmware Flashing<br><br>
>esptool -p COMxx erase_flash<br>
>
>esptool -p COMxx write_flash 0 firmware.bin (for ESP8266)<br>
>esptool -p COMxx write_flash -z 0x1000 firmware.bin (for ESP32)<br>
>
>2. Network Connection<br><br>
>main.py<br>
>import os, time, network<br>
>def network_setup():<br>
>    sta_if = network.WLAN(network.STA_IF)<br>
>    sta_if.active(True)<br>
>    if not sta_if.isconnected():<br>
>        print('Connecting to Network...')<br>
>        sta_if.connect('freecafe_02', 'freecafe00')<br>
>        while not sta_if.isconnected():<br>
>            pass<br>
>    print('Network Config:', sta_if.ifconfig())<br>
>
>3. Setup WebREPL<br>
>import webrepl_setup<br>
>
>4. MQTT example<br>
>
