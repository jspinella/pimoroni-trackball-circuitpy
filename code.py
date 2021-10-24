import usb_hid
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_hid.mouse import Mouse

I2C_ADDRESS = 0x0A

REG_LED_RED = 0x00
REG_LED_GRN = 0x01
REG_LED_BLU = 0x02
REG_LED_WHT = 0x03

REG_LEFT = 0x04
REG_RIGHT = 0x05
REG_UP = 0x06
REG_DOWN = 0x07

# i2c @ address 0xA
m = Mouse(usb_hid.devices)
i2c = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(i2c, I2C_ADDRESS)

# intensity of r,g,b,w LEDs from 0-100 e.g. set_leds(100,100,25,50)
def set_leds(r,g,b,w):
    device.write(bytes([REG_LED_RED, r & 0xff]))
    device.write(bytes([REG_LED_GRN, g & 0xff]))
    device.write(bytes([REG_LED_BLU, b & 0xff]))
    device.write(bytes([REG_LED_WHT, w & 0xff]))

def set_leds_purple(): set_leds(60,0,90,20)
def set_leds_orange(): set_leds(99,63,8,0)
def set_leds_yellow(): set_leds(100,85,6,0)
def set_leds_white(): set_leds(0,0,0,100)

def i2c_rdwr(data, length=0):
    """Write and optionally read I2C data."""
    device.write(bytes(data))

    if length > 0:
        msg_r = bytearray(length)
        device.readinto(msg_r)
        return list(msg_r)

    return []

def read():
    """Read up, down, left, right and switch data from trackball."""
    left, right, up, down, switch = i2c_rdwr([REG_LEFT], 5)

    switch = 129 == switch

    return up, down, left, right, switch

with device:
    #set_leds(0,0,5,100)
    set_leds_purple()

    multiplier = 9

    while True:
        up, down, left, right, switch = read()

        # Send movements and clicks to xte
        if switch:
            m.click(Mouse.LEFT_BUTTON)
        else:
            x = right - left
            y = down - up
            m.move(int(-x*multiplier), int(-y*multiplier), 0)
