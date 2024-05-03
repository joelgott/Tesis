import uasyncio
from uasyncio import Event
from machine import I2C, Pin
import time
from ui import UserInterface
from motor_driver import Motor

i2c = I2C(scl=Pin(22), sda=Pin(21))

async def main():
    userinterface = UserInterface(i2c)
    motor = Motor(1000)
    while True:
        if userinterface.b1.value() and not userinterface.b2.value():
            motor.dir.value(True)
            motor.start()
            userinterface.update_display("Derecha", display = "BOTH")
        elif not userinterface.b1.value() and userinterface.b2.value():
            motor.dir.value(False)
            motor.start()
            userinterface.update_display("Izquierda", display = "BOTH")
        else:
            motor.stop()
            userinterface.update_display("         ", "", display = "BOTH")
        #print("buttons: {}, {}".format(userinterface.b1.value(),userinterface.b2.value()))        
        await uasyncio.sleep_ms(100)

if __name__ == "__main__":
    uasyncio.run(main())