import uasyncio
from lcd_i2c import LCD
from machine import I2C, Pin
import time
from ads1x15 import ADS1015
from Button import Button

def button_action(pin, event):
    print(f'Button connected to Pin {pin} has been {event}')
    if event == Button.PRESSED:
        print('Button pressed')
    if event == Button.RELEASED:
        print('Button released')

my_button = Button(17, callback = button_action, internal_pullup = True)


    

# PCF8574 on 0x27
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = LCD(addr=I2C_ADDR, cols=I2C_NUM_COLS, rows=I2C_NUM_ROWS, i2c=i2c)
adc = ADS1015(i2c, 72, 2)

adc.set_conv(0, 0, 1) # start the first conversion

start = time.ticks_us() # get millisecond counter
adc.read_rev()
delta = time.ticks_diff(time.ticks_us(), start) 

lcd.begin()

led = Pin(2, Pin.OUT)

b1 = Pin(13, Pin.IN, Pin.PULL_UP)

async def main():
    count = 0
    led_value = False
    while True:
        #lcd.print("{0}".format(adc.raw_to_v(adc.read_rev())))
        my_button.update()
        lcd.clear()    
        delta = time.ticks_diff(time.ticks_us(), start) 
        count += 1
        led_value = not led_value
        lcd.print("{0}".format(count))
        led.value(led_value)
        await uasyncio.sleep_ms(1000)
        
        
uasyncio.run(main())

