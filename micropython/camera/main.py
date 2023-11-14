import uos
from machine import Pin, SDCard
import camera
import uasyncio

led = Pin(4,Pin.OUT)
rx = Pin(33,Pin.IN,Pin.PULL_DOWN)

wait_time = 3000

debug = True

def take_picture(name):
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
    img = camera.capture()
    imgFile = open("sd/Images/{0}.jpg".format(name), "wb")
    imgFile.write(img)
    imgFile.close()
    camera.deinit()

def start_sd():
    try:
        uos.stat("/sd")
        return True
    except:
        uos.mount(SDCard(), "/sd")
        return False    
        
def empty_sd():
    try:
        files = uos.listdir("sd/Images")
        for file in files:
            uos.remove("sd/Images/{}".format(file))
        print("SD card contents erased succesfully")
    except:
        print("Error erasing contents from SD card")

def unmount_sd():
    try:
        uos.umount("/sd")
    except:
        pass

async def main():
    
    # err = start_sd()
    # if err == True:
    #     led.value = True
    #     while 1:
    #         led.value = not led.value
    #         await uasyncio.sleep_ms(200)
    start_sd()
    empty_sd()
    
    count = 0
    done = False    
    time_counter = 0
    Timelapse_Running = True

    while Timelapse_Running:
        if rx.value():
            if done == False:
                take_picture("Foto_{0}".format(str(count)))
                count += 1
                done = True
            else:
                time_counter += 1 
                if time_counter > wait_time:
                    Timelapse_Running = False
        else :
            time_counter = 0
            done = False
        await uasyncio.sleep_ms(1)

    unmount_sd()

    while True:
        led.on()
        await uasyncio.sleep_ms(50)
        led.off()
        await uasyncio.sleep_ms(1000)

uasyncio.run(main())