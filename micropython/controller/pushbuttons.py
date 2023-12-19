from machine import Pin
import uasyncio
from primitives import Pushbutton
from lcd_i2c import LCD
from machine import I2C, Pin

# PCF8574 on 0x27
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = LCD(addr=I2C_ADDR, cols=I2C_NUM_COLS, rows=I2C_NUM_ROWS, i2c=i2c)

def toggle(led):
    led.value(not led.value())

def lcd_display(text):
    lcd.clear()
    lcd.print(text)

async def my_app():
    lcd.begin()
    b1 = Pin(13, Pin.IN, Pin.PULL_UP)
    led = Pin(2, Pin.OUT)
    pb = Pushbutton(b1, suppress = True)
    pb.release_func(toggle, (led,))  # Note how function and args are passed
    pb.double_func(lcd_display, ("doble click",))  # Note how function and args are passed
    pb.long_func(lcd_display, ("click largo",))  # Note how function and args are passed
    await uasyncio.sleep(60)  # Dummy

uasyncio.run(my_app())  # Run main application code