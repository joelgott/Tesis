import uos
import machine
import camera
import uasyncio

def take_picture(name):
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
    img = camera.capture()
    imgFile = open("sd/Images/{0}.jpg".format(name), "wb")
    imgFile.write(img)
    imgFile.close()
    camera.deinit()

async def timelapse(photo_time, max_amount = 1):
    print("empieza el timelapse")
    count = 0
    while count < max_amount:
        take_picture("Foto_{0}".format(str(count)))
        print("saque una foto")
        count += 1
        await uasyncio.sleep_ms(photo_time)

async def main():
    print("Arrancando")
    try:
        uos.stat("/sd")
    except:
        uos.mount(machine.SDCard(), "/sd")
    uasyncio.create_task(timelapse(1000,3))
    print("listo")
    while True:
        await uasyncio.sleep_ms(1000)

uasyncio.run(main())
