import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import colorsys  # for HSV to RGB

# ------------------
# Setup
# ------------------
kbd = Keyboard(usb_hid.devices)
pixels = neopixel.NeoPixel(board.D2, 2, brightness=0.4, auto_write=True)

button_map = [
    (board.D26, Keycode.W),
    (board.D27, Keycode.A),
    (board.D28, Keycode.S),
    (board.D29, Keycode.D),
]

buttons = []
for pin, key in button_map:
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append({"obj": btn, "key": key, "pressed": False})

# ------------------
# Rainbow Function
# ------------------
def rainbow_cycle_hsv(step):
    # step: 0–255
    hue = step / 255.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # full saturation & brightness
    pixels.fill((int(r*255), int(g*255), int(b*255)))

rainbow_step = 0

# ------------------
# Main Loop
# ------------------
while True:
    any_pressed = False

    for b in buttons:
        if not b["obj"].value:  # key pressed
            any_pressed = True
            if not b["pressed"]:
                kbd.press(b["key"])
                b["pressed"] = True

            # LED color based on key
            if b["key"] == Keycode.W:
                pixels.fill((0, 0, 255))
            elif b["key"] == Keycode.A:
                pixels.fill((255, 0, 0))
            elif b["key"] == Keycode.S:
                pixels.fill((0, 255, 0))
            elif b["key"] == Keycode.D:
                pixels.fill((0, 255, 255))

        else:  # key released
            if b["pressed"]:
                kbd.release(b["key"])
            b["pressed"] = False

    # Rainbow if no keys pressed
    if not any_pressed:
        rainbow_cycle_hsv(rainbow_step)
        rainbow_step = (rainbow_step + 1) % 256
        time.sleep(0.02)
    else:
        time.sleep(0.01)
