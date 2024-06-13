import uos
from machine import SDCard
import uasyncio

class SD_Card:
    def __init__(self):
        pass

    def mount_sd(self):
        if 'sd' not in uos.listdir(""):
            uos.mount(SDCard(), "/sd")
            return True
        else:
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
    
async def main():
    sdcard = SD_Card()
    sdcard.mount_sd()

if __name__ == "__main__":
    uasyncio.run(main())
