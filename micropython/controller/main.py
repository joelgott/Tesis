import uasyncio
from uasyncio import Event
from machine import I2C, Pin
import time
from ui import UserInterface
from ads1015 import LoadCell
from motor_driver import Motor
from camera_driver import Camera

i2c = I2C(scl=Pin(22), sda=Pin(21))

async def main():
    userinterface = UserInterface(i2c)
    await userinterface.config()
    loadcell = LoadCell(i2c)
    cam = Camera()
    led = Camera(2)
    motor = Motor(200)
    exp_finished = Event()
    avalancha = Event()
    last_avalanch = 0
    uasyncio.create_task(motor.move_with_stop(avalancha))
    while loadcell.last_weight < userinterface.config_vars[3]:
        if loadcell.last_weight > last_avalanch + userinterface.config_vars[2]:
            avalancha.set()
            for i in range(userinterface.config_vars[1]*10):
                userinterface.update_display("avalancha", "faltan {} s".format(userinterface.config_vars[1]*60 - i))
                await uasyncio.sleep_ms(userinterface.config_vars[1]*1000)
            last_avalanch = loadcell.last_weight
            avalancha.clear()
            uasyncio.create_task(motor.move_with_stop(avalancha))  
        if not avalancha.is_set():
            loadcell.get_weight(3)
            userinterface.update_display("peso="+str(round(loadcell.last_weight,3)))
            uasyncio.create_task(led.take_photo(min(100,int(userinterface.config_vars[0]*0.5))))
        await uasyncio.sleep_ms(userinterface.config_vars[0])
    led.shutoff_cam()
    exp_finished.set()
    userinterface.update_display("Regresando", "{} mm".format(motor.distance_moved))
    await motor.return_back()
    userinterface.update_display("Experiencia", "Terminada")

if __name__ == "__main__":
    uasyncio.run(main())