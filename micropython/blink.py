from machine import Pin
import time

def blink(led, period):
    while True:
        led.on()
        time.sleep_ms(50)
        led.off()
        time.sleep_ms(period)

blink(Pin(33,Pin.OUT),1000)