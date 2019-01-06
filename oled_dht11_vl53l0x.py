import os, machine, time, dht, ssd1306, vl53l0x

# for normal scl = 5/sda = 4, for d-duino scl=4/sda=5
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
vl53 = vl53l0x.VL53L0X(i2c)

oled.fill(0) # (0 - clear buffer / 1)
oled.text('test', 0, 0) # posion in (x, y)
oled.show()

for i in range(0,6):
  #oled.text(str(i),0,8*i)
  oled.text(str(i),8*i, 8)
  oled.show()
  time.sleep_ms(100)

#oled.fill(0)
#oled.show()

d = dht.DHT11(machine.Pin(15))
pin2 = machine.Pin(2, machine.Pin.OUT)
pin12 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
prev_tick = time.ticks_ms()

while True:
  vl_read = vl53.read()
  #print(vl_read)
  
  if vl_read <= 150:
    pin2.value(1)
  else:
    pin2.value(0)
    
  if pin12.value() == 0:
    oled.text("Button Pressed.",0,32)
    oled.show()
    break
  
  current_tick = time.ticks_ms()
  if current_tick - prev_tick >= 2500:
    prev_tick =  current_tick
    d.measure()
    print(str(d.temperature())+' '+str(d.humidity()))
    
  oled.fill(0)
  oled.text("Temp: "+str(d.temperature())+"'C",0,0)
  oled.text("Humi: "+str(d.humidity())+"%",0,8)
  oled.text("Dist: "+str(vl_read)+"mm",0,16)
  oled.show()

