
import uasyncio
from sdcard import SDCard
from espcam import EspCam
from machine import Pin

rx = Pin(33,Pin.IN,Pin.PULL_DOWN)

wait_time = 3000

debug = True

async def main():
    
    espcam = EspCam()
    sdcard = SDCard()
    sdcard.mount_sd()
    sdcard.empty_sd()
    
    count = 0
    done = False    
    time_counter = 0
    Timelapse_Running = True

    while Timelapse_Running:
        if rx.value():
            if done == False:
                img = espcam.take_picture()
                sdcard.save_file("Foto_{0}".format(str(count)), img)
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
        

uasyncio.run(main())