from machine import Pin, I2C
from ads1x15 import ADS1115
import uasyncio
import time

i2c = I2C(scl=Pin(22), sda=Pin(21))
adc = ADS1115(i2c, 72, 5)

#adc.set_conv(4, 0, 1) # start the first conversion

start = time.ticks_us() # get millisecond counter
#adc.read_rev()
delta = time.ticks_diff(time.ticks_us(), start)

volts2weight = 229000

async def main():
    last_value = 0
    actual_value = 0
    filtered_value = 0
    last_measurement = adc.raw_to_v(adc.read(4, 0, 1))
    while True:
        actual_value = (last_measurement - adc.raw_to_v(adc.read(4, 0, 1)))*volts2weight
        filtered_value = round(0.7*last_value + 0.3*actual_value,2)
        last_value = filtered_value
        print(filtered_value)
        delta = time.ticks_diff(time.ticks_us(), start) 
#         print(delta)
        await uasyncio.sleep_ms(100)
        
uasyncio.run(main())