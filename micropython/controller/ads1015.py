from machine import Pin, I2C
from ads1x15 import ADS1015
import uasyncio
import time

i2c = I2C(0)
adc = ADS1015(i2c, 72, 2)

adc.set_conv(0, 0, 1) # start the first conversion

start = time.ticks_us() # get millisecond counter
adc.read_rev()
delta = time.ticks_diff(time.ticks_us(), start) 

async def main():
    while True:
        print(adc.raw_to_v(adc.read_rev()))
        delta = time.ticks_diff(time.ticks_us(), start) 
#         print(delta)
        await uasyncio.sleep_ms(50)
        
uasyncio.run(main())