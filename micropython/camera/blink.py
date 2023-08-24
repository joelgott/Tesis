from machine import Pin
import time

def ledblink(led, period):
    while True:
        led.on()
        time.sleep_ms(50)
        led.off()
        time.sleep_ms(period)

ledblink(Pin(4,Pin.OUT),1000)