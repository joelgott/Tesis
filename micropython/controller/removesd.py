import uasyncio
from machine import Pin

led = Pin(2, Pin.OUT, value = False)
cam1 = Pin(18, Pin.OUT, value = False)
cams = [cam1, led]

async def shutoff_cam(cam):
    cam.value(False)
    await uasyncio.sleep_ms(10000)
    cam.value(True)
    await uasyncio.sleep_ms(10000)
    print("cam_finished")
    
async def main():
    for cam in cams:
        uasyncio.create_task(shutoff_cam(cam))
    while True:
        await uasyncio.sleep_ms(10)
        

uasyncio.run(main())