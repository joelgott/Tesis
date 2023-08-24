import uos
import machine

# SOLO HAY QUE MONTAR UNA VEZ

# Open file in SD
try:
    print(uos.stat("/sd"))
except:
    uos.mount(machine.SDCard(), "/sd")
print(uos.listdir("/sd"))
print(uos.listdir("/sd/Images"))