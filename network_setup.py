import network, webrepl
# import webrepl_setup 

def network_setup():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to Network...')
        sta_if.connect('freecafe_02', 'freecafe00')
        while not sta_if.isconnected():
            pass
    print('Network Config:', sta_if.ifconfig())
    webrepl.start()

network_setup()
