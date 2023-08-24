import uos
import machine
import camera
import uasyncio
import time

def take_picture(name):
    
    img = camera.capture()
    imgFile = open("sd/Images/{0}.jpg".format(name), "wb")
    imgFile.write(img)
    imgFile.close()

async def main():
    try:
        uos.stat("/sd")
    except:
        uos.mount(machine.SDCard(), "/sd")
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
    camera.speffect(camera.EFFECT_NONE)
    camera.framesize(camera.FRAME_VGA)
    start = time.ticks_us() # get millisecond counter
    take_picture("test2")
    delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
    camera.deinit()
    print(delta)
    
    #while True:
    #   await uasyncio.sleep_ms(1000)

uasyncio.run(main())