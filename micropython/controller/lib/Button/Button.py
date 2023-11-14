from machine import Pin
import uasyncio

class Button(object):
    
    rest_state = False
    # pin = None
    # pin_number = 0
    RELEASED = 'released'
    PRESSED = 'pressed'
    def __init__(self, pin, rest_state = False, callback = None, internal_pullup = False, internal_pulldown = False):
        self.pin_number = pin
        self.rest_state = rest_state
        if internal_pulldown:
            self.internal_pull = Pin.PULL_DOWN
            self.rest_state = False
        elif internal_pullup:
            self.internal_pull = Pin.PULL_UP
            self.rest_state = True
        else:
            self.internal_pull = None
        
        self.pin = Pin(pin, mode = Pin.IN, pull = self.internal_pull)
        
        self.callback = callback
        self.active = False
    
    def update(self):
        # print(self.pin.value())
        if self.pin.value() == (not self.rest_state) and (not self.active):
            self.active = True
            if self.callback != None:
                self.callback(self.pin_number, Button.PRESSED)
            return
        if self.pin.value() == self.rest_state and self.active:
            self.active = False
            if self.callback != None:
                self.callback(self.pin_number, Button.RELEASED)
            return
        
class button_manager:
    def __init__(self, buttons, debounce_time):
        self.buttons = buttons
        self.debounce_time = debounce_time
        if len(debounce_time) != 1:
            yield TypeError("ingresar el tiempo de debounce deseado")
        uasyncio.create_task(self.updater())
    async def updater(self):
        while True:
            for button in self.buttons:
                if button.pin.value() == (not button.rest_state) and (not button.active):
                    button.active = True
                    if button.callback != None:
                        button.callback(button.pin_number, Button.PRESSED)
                    return
                if button.pin.value() == button.rest_state and button.active:
                    button.active = False
                    if button.callback != None:
                        button.callback(button.pin_number, Button.RELEASED)
                    return
            await uasyncio.sleep_ms(self.debounce_time)
    