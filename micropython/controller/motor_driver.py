from machine import Pin, PWM
import uasyncio

Pull = Pin(26,Pin.OUT)
Dir = Pin(25,Pin.OUT)

async def main(time, speed):
    Dir.value(0)
    led = Pin(2, Pin.OUT, value = False)
    pwm1 = PWM(Pull, freq=speed, duty_u16=32768)  # create a PWM object on a pin
    pwm2 = PWM(led, freq=speed, duty_u16=32768)  # create a PWM object on a pin
    #pwm.init(freq=20, duty_ns=5000)
    await uasyncio.sleep_ms(time)
    pwm1.deinit()
    pwm2.deinit()

uasyncio.run(main(10000,500))