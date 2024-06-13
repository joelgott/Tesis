import uos
import machine
import camera
import uasyncio
import time

framesizes = [camera.FRAME_96X96, camera.FRAME_QQVGA, camera.FRAME_QCIF, camera.FRAME_HQVGA, camera.FRAME_240X240, camera.FRAME_QVGA, camera.FRAME_CIF, camera.FRAME_HVGA, camera.FRAME_VGA, camera.FRAME_SVGA, camera.FRAME_XGA, camera.FRAME_HD, camera.FRAME_SXGA, camera.FRAME_UXGA, camera.FRAME_FHD, camera.FRAME_P_HD, camera.FRAME_P_3MP, camera.FRAME_QXGA, camera.FRAME_QHD, camera.FRAME_WQXGA, camera.FRAME_P_FHD, camera.FRAME_QSXGA]
framesize_names = ["96X96", "QQVGA", "QCIF", "HQVGA", "240X240", "QVGA", "CIF", "HVGA", "VGA", "SVGA", "XGA", "HD", "SXGA", "UXGA", "FHD", "P_HD", "P_3MP", "QXGA", "QHD", "WQXGA", "P_FHD", "QSXGA"]
# el 13, 14 da problemas

def take_picture(name):
    
    img = camera.capture()
    imgFile = open("sd/{0}.jpg".format(name), "wb")
    imgFile.write(img)
    imgFile.close()

async def main():
    try:
        uos.stat("/sd")
    except:
        uos.mount(machine.SDCard(), "/sd")
    try:
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
    except:
        pass
    camera.speffect(camera.EFFECT_NONE)
    camera.quality(5)
    time_taken = []
    first_size = 0
    size_len = 10
    if (size_len + first_size) > len(framesizes):
        raise ValueError("Out of index")
    for i in range(size_len):     # Hay que tener cuidado con que le alcanze el tiempo para guardar la foto
        camera.framesize(framesizes[i+first_size])
        start = time.ticks_us() # get millisecond counter
        take_picture(framesize_names[i+first_size])
        delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
        time_taken.append([framesize_names[i+first_size],delta])
        await uasyncio.sleep_ms(12000)
    camera.deinit()

    print(time_taken)
    #while True:
    #   await uasyncio.sleep_ms(1000)

uasyncio.run(main())