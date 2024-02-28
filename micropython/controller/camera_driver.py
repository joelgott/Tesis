from machine import Pin, I2C
import uasyncio
import time

class Camera():
    def __init__(self, pin = 18):
        self.cam = Pin(pin, Pin.OUT, value = False)

    async def take_photo(self, waittime):
        self.cam.value(True)
        await uasyncio.sleep_ms(waittime)
        self.cam.value(False)

    def shutoff_cam(self):
        self.cam.value(True)


