from machine import Pin
import uasyncio

Pull = Pin(18,Pin.OPEN_DRAIN)
Dir = Pin(19,Pin.OPEN_DRAIN)

async def main(duty):
    Dir.value(1)
    while True:
        Pull.value(0)
        await uasyncio.sleep_ms(duty)
        Pull.value(1)
        await uasyncio.sleep_ms(duty)


uasyncio.run(main(100))