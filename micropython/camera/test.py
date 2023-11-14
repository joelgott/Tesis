import camera
import uos
import machine

uos.mount(machine.SDCard(), "/sd")

camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
img = camera.capture()
imgFile = open("sd/photo.jpg", "wb")
imgFile.write(img)
imgFile.close()
camera.deinit()




    #uart = machine.UART(0) 

    #uart.init(baudrate=115200, bits=8, parity=None, stop=1)

    #uasyncio.create_task(handler(uart))