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




