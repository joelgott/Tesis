from lcd_i2c import LCD
from machine import I2C, Pin
import ssd1306
import uasyncio
from primitives import Pushbutton

default_t1 = 1000
default_t2 = 2
default_threshold_weight = 15
default_final_weight = 400

state_texts = ["t1 (ms):" , "t2 (min):" , "umbral peso (g):", "Peso final (g):"]
default_values = [default_t1, default_t2, default_threshold_weight, default_final_weight]
cfg_vars = default_values.copy()

class UserInterface:
    def __init__(self, i2c = I2C(scl=Pin(22), sda=Pin(21))):
        # PCF8574 on 0x27
        I2C_ADDR = 0x27     # DEC 39, HEX 0x27
        I2C_NUM_ROWS = 2
        I2C_NUM_COLS = 16
        self.i2c = i2c 
        self.lcd = LCD(addr=I2C_ADDR, cols=I2C_NUM_COLS, rows=I2C_NUM_ROWS, i2c=self.i2c) 
        self.lcd.begin()
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)        
        self.b1 = Pin(13, Pin.IN, Pin.PULL_UP)
        self.b2 = Pin(12, Pin.IN, Pin.PULL_UP)
        self.b3 = Pin(14, Pin.IN, Pin.PULL_UP)
        self.b4 = Pin(27, Pin.IN, Pin.PULL_UP)        
        self.config_vars = default_values.copy()
        self.state = 0
        self.config_finished = False
        try:
            self.lcd.clear()
            self.oled.fill(0)
        except:
            pass            

    def config_buttons(self, b1, b2 = None, b3 = None, b4 = None):
        self.next_state_button = Pushbutton(b1, suppress = False)
        self.next_state_button.press_func(self.next_state)                                     
        if b2 != None:
            self.up_button = Pushbutton(b2, suppress = True)
            self.up_button.press_func(self.up)
            self.up_button.long_func(self.upx10)
        if b3 != None:
            self.down_button = Pushbutton(b3, suppress = True)
            self.down_button.press_func(self.down)
            self.down_button.long_func(self.downx10)
        if b4 != None:
            self.prev_button = Pushbutton(b4, suppress = True)
            self.prev_button.press_func(self.prev_state)

    def up(self):
        self.config_vars[self.state] += 1
        self.update_display(state_texts[self.state],str(self.config_vars[self.state]))

    def down(self):
        if self.config_vars[self.state] - 1 > 0: 
            self.config_vars[self.state] -= 1
            self.update_display(state_texts[self.state],str(self.config_vars[self.state]))
        
    def upx10(self):
        self.config_vars[self.state] += 10
        self.update_display(state_texts[self.state],str(self.config_vars[self.state]))

    def downx10(self):
        if self.config_vars[self.state] - 10 > 0:
            self.config_vars[self.state] -= 10
            self.update_display(state_texts[self.state],str(self.config_vars[self.state]))

    def next_state(self):
        if self.state < (len(self.config_vars)) :
            if self.state < (len(self.config_vars) - 1):
                self.update_display(state_texts[self.state+1],str(self.config_vars[self.state+1]))
            self.state += 1
                
    def prev_state(self):
        if self.state > 0:
            self.state -= 1
            self.update_display(state_texts[self.state],str(self.config_vars[self.state]))

    async def config(self):
        self.config_buttons(self.b1,self.b2,self.b3,self.b4)
        self.update_display(state_texts[self.state],str(self.config_vars[self.state]))
        while True:
            if self.state == len(self.config_vars):
                break
            await uasyncio.sleep_ms(100)
        try:
            self.lcd.clear()        
        except:
            self.oled.fill(0)

    def update_display(self, first_column, second_column = "", display = "LCD"):  
        if display == "LCD":
            self.lcd.clear()
            self.lcd.set_cursor(0,0)
            self.lcd.print(first_column)
            self.lcd.set_cursor(0,1)
            self.lcd.print(second_column)
        elif display == "OLED":
            self.oled.fill(0)    
            self.oled.text(first_column, 0, 0, 1)
            self.oled.text(second_column, 0, 40, 1)
            self.oled.show()
        elif display == "BOTH":
            self.lcd.clear()
            self.lcd.set_cursor(0,0)
            self.lcd.print(first_column)
            self.lcd.set_cursor(0,1)
            self.lcd.print(second_column)
            self.oled.fill(0)    
            self.oled.text(first_column, 0, 0, 1)
            self.oled.text(second_column, 0, 40, 1)
            self.oled.show()
        else:
            print("No existe el display {}".format(display))
                
async def main():
    ui = UserInterface()
    await ui.config()
    print("termine")

if __name__ == "__main__":
    uasyncio.run(main())
      