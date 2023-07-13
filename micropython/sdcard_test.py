import uos
import machine

uos.mount(machine.SDCard(), "/sd")

# Open file in SD

print(uos.listdir("/sd"))