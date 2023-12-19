from machine import Pin
import uasyncio

Pull = Pin(25,Pin.OPEN_DRAIN)
Dir = Pin(26,Pin.OPEN_DRAIN)

async def main(duty):
    Dir.value(1)
    while True:
        Pull.value(0)
        await uasyncio.sleep_ms(duty)
        Pull.value(1)
        await uasyncio.sleep_ms(duty)


uasyncio.run(main(10000))