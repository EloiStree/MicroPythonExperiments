import microcontroller
import board
import time
import digitalio
import analogio


#i2c = board.I2C(board.GP17, board.GP16)

#print("TX "+ board.TX.value)
#print("RX "+ board.RX.value)
#uart = busio.UART(board.TX,board.RX, baudrate=9600)

uart = busio.UART(board.D24, board.D25)

#uart = busio.UART(17, 16, baudrate=9600)

pins_to_set_as_output = [
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7
    
]

allowRelay=False

pin_objects = []

def setAllPinOut():
    for pin in pins_to_set_as_output:
        try:
            pin_io = digitalio.DigitalInOut(pin)
            pin_io.direction = digitalio.Direction.OUTPUT
            pin_io.value = False
            pin_objects.append(pin_io)
        except AttributeError:
            continue


def set_all_pins_output_state(state):
    if allowRelay:
        for pin in pin_objects:
            try:
                pin.value = state

            except AttributeError:
                continue




print("Hello World")

setAllPinOut()

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True
time.sleep(0.5)
led.value = False
time.sleep(0.5)
led.value = True
time.sleep(0.5)
led.value = False
time.sleep(0.5)


board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append("board.{}".format(alias))
        if len(pins) > 0:
            board_pins.append(" ".join(pins))
for pins in sorted(board_pins):
    print(pins)

    
while True:
    data = uart.read(32)  # read up to 32 bytes
    # print(data)  # this is a bytearray type
    if data is not None:
        # convert bytearray to string
        set_all_pins_output_state(True)
        data_string = ''.join([chr(b) for b in data])
        print(data_string, end="")
        time.sleep(0.2)
        set_all_pins_output_state(False)


