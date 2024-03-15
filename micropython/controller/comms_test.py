import board
import busio
import digitalio

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.IO41)
led.direction = digitalio.Direction.OUTPUT

re = digitalio.DigitalInOut(board.IO47)
re.direction = digitalio.Direction.OUTPUT

re.value = False

uart = busio.UART(tx=board.IO13, rx=board.IO48,rs485_dir= board.IO14,rs485_invert=False,baudrate=9600)

while True:
    data = uart.read(32)  # read up to 32 bytes
    #print(data)  # this is a bytearray type

    if data is not None:
        led.value = True

        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")

        led.value = False