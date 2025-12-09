import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import colorsys

# ----------------------------
# Setup
# ----------------------------
kbd = Keyboard(usb_hid.devices)

NUM_LEDS = 7
LED_PIN = board.GP6
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.4, auto_write=True)

button_map = [
    (board.GP1, Keycode.ONE),
    (board.GP2, Keycode.TWO),
    (board.GP4, Keycode.THREE),
    (board.GP3, Keycode.FOUR),
    (board.GP26, Keycode.FIVE),
    (board.GP27, Keycode.SIX),
    (board.GP28, Keycode.SEVEN),
    (board.GP29, Keycode.EIGHT),
]

# Neon colors for each button
button_colors = [
    (50, 50, 255),   # SW1
    (50, 255, 50),   # SW2
    (255, 50, 255),  # SW3
    (255, 50, 50),   # SW4
    (50, 255, 255),  # SW5
    (255, 255, 50),  # SW6
    (255, 100, 255), # SW7
    (255, 150, 50),  # SW8
]

buttons = []
for i, (pin, key) in enumerate(button_map):
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append({
        "obj": btn,
        "key": key,
        "pressed": False,
        "color": button_colors[i]
    })

# ----------------------------
# Rainbow animation
# ----------------------------
def rainbow_cycle(step):
    for i in range(NUM_LEDS):
        hue = ((i * 20) + step) % 255 / 255
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        pixels[i] = (int(r*255), int(g*255), int(b*255))

rainbow_step = 0

# ----------------------------
# Main Loop
# ----------------------------
while True:
    any_pressed = False

    for b in buttons:
        if not b["obj"].value:            # Button pressed
            any_pressed = True
            if not b["pressed"]:
                kbd.press(b["key"])       # send HID key
                b["pressed"] = True

            # Set LED color
            pixels.fill(b["color"])

        else:
            if b["pressed"]:
                kbd.release(b["key"])
            b["pressed"] = False

    # No buttons pressed → rainbow
    if not any_pressed:
        rainbow_cycle(rainbow_step)
        rainbow_step = (rainbow_step + 1) % 255
        time.sleep(0.02)
    else:
        time.sleep(0.01)
