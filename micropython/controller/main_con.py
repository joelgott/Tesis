import machine
import uasyncio


        
async def handler(uart):
    while True:
        if uart.any():
            msg = str(uart.readline(),'utf-8')
            print(msg)

async def main():
    
    uart = machine.UART(2) 

    uart.init(baudrate=115200, bits=8, parity=None, stop=1)

    uasyncio.create_task(handler(uart))
    
    while True:
        await uasyncio.sleep_ms(500)


uasyncio.run(main())

