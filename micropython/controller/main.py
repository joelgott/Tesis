import uasyncio
from uasyncio import Event
from lcd_i2c import LCD
from machine import I2C, Pin
import time
from ads1x15 import ADS1115
from primitives import Pushbutton

app_state = 0
default_t1 = 2000
default_t2 = 1
default_threshold_weight = 5
default_final_weight = 200
user_input = default_t1

default_sps = 50

state_texts = ["t1 (ms):" , "t2 (min):" , "umbral peso (g):", "Peso final (g):"]
default_values = [default_t1, default_t2, default_threshold_weight, default_final_weight]
cfg_vars = default_values.copy()

config_finished = True # saltea la configuracion

# PCF8574 on 0x27
I2C_ADDR = 0x27     # DEC 39, HEX 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

volts2weight = 229000
max_steps = 300000 # 600 * 200 / 2 #  600[mm] / 2 [mm/rev] * 1000  [step/rev]
steps_taken = 0

i2c = I2C(scl=Pin(22), sda=Pin(21))
lcd = LCD(addr=I2C_ADDR, cols=I2C_NUM_COLS, rows=I2C_NUM_ROWS, i2c=i2c)
Pull = Pin(26,Pin.OUT)
Dir = Pin(25,Pin.OUT)

adc = ADS1115(i2c, 72, 5)

def next_state():
    global app_state
    global user_input
    global config_finished
    if app_state < 4:
        cfg_vars[app_state] = user_input
        if app_state < (len(cfg_vars) - 1) :
            app_state += 1
            user_input = default_values[app_state]
            print("state: ",str(app_state))
            update()
        else:
            user_input = default_values[-1]
            print("config finished")
            config_finished = True
            
def prev_state():
    global app_state
    global user_input
    if app_state > 0:
        app_state -= 1
        print(cfg_vars)
        user_input = cfg_vars[app_state]
        print("state: ",str(app_state), "var value:",cfg_vars[app_state])
        update()
        
def up():
    global user_input
    user_input += 1
    print("up")
    update()

def down():
    global user_input
    user_input -= 1
    print("down")
    update()
    
def upx10():
    global user_input
    user_input += 10
    update()

def downx10():
    global user_input
    user_input -= 10
    update()
      
def config_buttons(b1,b2 = None,b3 = None,b4 = None):
    next_state_button = Pushbutton(b1, suppress = False)
    next_state_button.press_func(next_state)
    if b2 != None:
        up_button = Pushbutton(b2, suppress = True)
        up_button.press_func(up)
        up_button.long_func(upx10)
    if b3 != None:
        down_button = Pushbutton(b3, suppress = True)
        down_button.press_func(down)
        down_button.long_func(downx10)
    if b4 != None:
        down_button = Pushbutton(b4, suppress = True)
        down_button.press_func(prev_state)

def update():
    global app_state
    global user_input
    lcd.clear()
    lcd.set_cursor(0,0)
    lcd.print(state_texts[app_state])
    lcd.set_cursor(0,1)
    lcd.print(str(user_input))

async def make_step(wait_time):
    Pull.value(0)
    await uasyncio.sleep_ms(wait_time)
    Pull.value(1)

async def run_motor(stepspersecond,exp_terminada,avalancha):
    global steps_taken
    steps = 0
    Dir.value(0)
    period = int(1000/(2*stepspersecond))
    while steps < max_steps:
        if exp_terminada.is_set():
            break
        if (not avalancha.is_set()):
            uasyncio.create_task(make_step(1))
            steps += 1
            steps_taken = steps
            lcd.home()
            lcd.print("paso " + str(steps) + " de " + str(max_steps))
        await uasyncio.sleep_ms(period)
    if (not exp_terminada.is_set()):
        exp_terminada.set()
    print("motor finished")
    
async def motor_return(steps_amount,stepspersecond):
    Dir.value(1)
    period = int(1000/(2*stepspersecond))
    steps = 0
    while steps < steps_amount:
        uasyncio.create_task(make_step(10))
        steps += 1
        await uasyncio.sleep_ms(period)

async def take_photo(cam, waittime):
    cam.value(True)
    await uasyncio.sleep_ms(waittime)
    cam.value(False)

async def shutoff_cam(cam):
    cam.value(True)
    print("cam_finished")

async def cam_weight(cams, t1, t2, delta_weight, max_weight, exp_terminada, avalancha):
    last_measurement = adc.raw_to_v(adc.read(4, 0, 1))
    weight_acum = 0
    global steps_taken
    while True:
        if (exp_terminada.is_set()):
            for cam in cams:
                uasyncio.create_task(shutoff_cam(cam))
            lcd.clear()
            lcd.home()
            lcd.print("exp terminada")
            lcd.set_cursor(0,1)
            lcd.print("<- " + str(steps_taken) + " pasos")
            uasyncio.create_task(motor_return(steps_taken,default_sps))
            break
        for cam in cams:
            uasyncio.create_task(take_photo(cam,100))
        current_measurement = adc.raw_to_v(adc.read(4, 0, 1))
        weight = (last_measurement - current_measurement)*volts2weight
        if weight > delta_weight:
            avalancha.set()
            lcd.set_cursor(0,1)
            lcd.print("avalancha!")
            await uasyncio.sleep(t2*60)
            avalancha.clear()
            last_measurement = current_measurement
            weight_acum += weight
            lcd.set_cursor(0,1)
            lcd.print("p acum: " + str(weight_acum))
        else:
            if weight_acum < max_weight:
                await uasyncio.sleep_ms(t1)
            else:
                if (not exp_terminada.is_set()):
                    exp_terminada.set()
        
async def main():
    led = Pin(2, Pin.OUT, value = False)
    cam1 = Pin(18, Pin.OUT, value = False)
    cams = [cam1, led]
    b1 = Pin(13, Pin.IN, Pin.PULL_UP)
    b2 = Pin(12, Pin.IN, Pin.PULL_UP)
    b3 = Pin(14, Pin.IN, Pin.PULL_UP)
    b4 = Pin(27, Pin.IN, Pin.PULL_UP)
    lcd.begin()
    if not config_finished:
        print("configurando botones")
        config_buttons(b1,b2,b3,b4)
        print("listo")
    update()
    first_time = True
    exp_finished = Event()
    avalancha = Event()
    while True:        
        if config_finished and first_time:
            lcd.clear()
            first_time = False
            uasyncio.create_task(run_motor(default_sps,exp_finished,avalancha))
            uasyncio.create_task(cam_weight(cams,cfg_vars[0],cfg_vars[1],cfg_vars[2],cfg_vars[3],exp_finished,avalancha))
        else:
            await uasyncio.sleep_ms(1000)
    
uasyncio.run(main())