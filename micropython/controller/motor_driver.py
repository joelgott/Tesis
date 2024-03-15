from machine import Pin, PWM
import uasyncio

#max_steps = 300000 # 600 * 200 / 2 #  600[mm] * 0.5 [rev/mm] * 1000  [step/rev]
# Dir = 1 vuelve, dir = 0 avanza
class Motor:
    def __init__(self, freq = 500):
        self.pull = Pin(26,Pin.OUT)
        self.dir = Pin(25,Pin.OUT)
        self.freq = freq
        self.pwm = None
        self.steps_per_rev = 1000
        self.mm_per_rev = 7.7
        self.distance_moved = 0

    def start(self):
        self.pwm = PWM(self.pull, freq=self.freq, duty_u16=32768)  # create a PWM object on a pin

    def stop(self):
        try:
            self.pwm.deinit()
        except:
            pass
    
    async def move(self, distance, dir = 0):
        self.dir.value(dir)
        wait_time = int(distance * 1000.0 * self.steps_per_rev / (self.mm_per_rev * self.freq))
        self.start()
        await uasyncio.sleep_ms(wait_time)
        self.stop()

    async def move_with_stop(self, stop, dir = 0):
        self.dir.value(dir)
        self.start()
        while True:
            if stop.is_set():
                self.stop()                
                break
            self.distance_moved += 10 * self.freq * self.mm_per_rev / (1000 * self.steps_per_rev)
            await uasyncio.sleep_ms(10)
        self.stop()

    async def return_back(self, dir = 1):
        await self.move(self.distance_moved,dir)

async def main():
    my_motor = Motor(1000)
    await my_motor.move(500,1)

if __name__ == "__main__":
    uasyncio.run(main())