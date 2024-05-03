from machine import Pin, I2C
from ads1x15 import ADS1115
import uasyncio
import time

i2c = I2C(scl=Pin(22), sda=Pin(21))
adc = ADS1115(i2c, 72, 5)

volts2weight = 229000

class LoadCell():
    def __init__(self, i2c = I2C(scl=Pin(22), sda=Pin(21))):
        self.i2c = i2c
        self.adc = ADS1115(i2c, 72, 5)
        self.volts2weight = -229000
        self.tare = 0
        self.make_tare()
        self.last_weight = 0
        self.weights = []

    def make_tare(self, prom_cycles = 25):
        self.tare = self.measure_weight(prom_cycles)

    def measure_weight(self, prom_cycles):
        prom_value = 0
        for i in range(prom_cycles):
            current_measurement = adc.raw_to_v(adc.read(4, 0, 1))
            actual_value = current_measurement*self.volts2weight
            prom_value += float(actual_value)/prom_cycles
        return prom_value

    def get_weight(self, prom_cycles):
        self.last_weight = self.measure_weight(prom_cycles) - self.tare

    def save_last_weight(self):
        self.weights.append((self.last_weight,time.time()))

    async def run(self, wait_time = 500, prom_cycles = 1, times = 10):
        i = 0
        while i < times:
            self.get_weight(prom_cycles)
            self.weights.append((self.last_weight,time.time()))
            await uasyncio.sleep_ms(wait_time)
            i += 1

async def main():
    mycell = LoadCell()
    await mycell.run()
    with open('data.txt','w') as f:
        f.write(str(mycell.weights))

if __name__ == "__main__":
    uasyncio.run(main())
