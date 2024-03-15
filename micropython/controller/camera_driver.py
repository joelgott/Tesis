from machine import Pin, I2C
import uasyncio
import time

class Camera():
    def __init__(self, pin = 18):
        self.cam = Pin(pin, Pin.OUT, value = False)
        self.cam.value(False)

    async def take_photo(self, waittime):
        self.cam.value(True)
        await uasyncio.sleep_ms(waittime)
        self.cam.value(False)

    def shutoff_cam(self):
        self.cam.value(True)

async def main():
    cam = Camera(18)
    led = Camera(2)
    for i in range(5):
        uasyncio.create_task(cam.take_photo(500))
        uasyncio.create_task(led.take_photo(500))
        await uasyncio.sleep_ms(3000)
    cam.shutoff_cam()
    led.shutoff_cam()

if __name__ == "__main__":
    uasyncio.run(main())

