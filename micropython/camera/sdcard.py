import uos
from machine import SDCard
import uasyncio

class SD_Card:
    def __init__(self):
        pass

    def mount_sd(self):
        try:
            uos.stat("/sd")
            return True
        except:
            uos.mount(SDCard(), "/sd")
            return False 

    def empty_sd(self):
        try:
            files = uos.listdir("sd/Images")
            for file in files:
                uos.remove("sd/Images/{}".format(file))
            print("SD card contents erased succesfully")
        except:
            print("Error erasing contents from SD card")

    def unmount_sd(self):
        try:
            uos.umount("/sd")
        except:
            pass

    def save_file(self, name, file, path = "sd/Images/"):
        imgFile = open("{0}{1}.jpg".format(path,name), "wb")
        imgFile.write(file)
        imgFile.close()
    
