import uos
from machine import Pin
import camera
import uasyncio

class EspCam():
    def __init__(self):
        self.led = Pin(4,Pin.OUT)

    def take_picture(name):
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        img = camera.capture()
        camera.deinit()
        return img

    async def flash(self, onTime = 50, downTime = 1000):
        self.led.on()
        await uasyncio.sleep_ms(onTime)
        self.led.off()
        await uasyncio.sleep_ms(downTime)

async def main():
    espcam = EspCam()
    while True:
        await espcam.flash()

if __name__ == "__main__":
    uasyncio.run(main())

