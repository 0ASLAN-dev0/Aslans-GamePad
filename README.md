# **WASD Keypad with RGB Feedback (CircuitPython)**

A 4-button mechanical keypad that sends USB HID keys (`W`, `A`, `S`, `D`) and provides RGB feedback. Idle LEDs run a rainbow animation.

---

## **Features**

* USB HID keyboard output (`W`, `A`, `S`, `D`)
* 4 buttons with RGB LEDs:

  * **W** → Blue
  * **A** → Green
  * **S** → Magenta
  * **D** → Red
* Rainbow animation when no key is pressed

---

## **Hardware**

* CircuitPython-compatible board
* 4 momentary buttons (D26–D29)
* 2 NeoPixels on D2
* USB connection

---

## **Setup**

1. Flash CircuitPython and copy `code.py`
2. Install `adafruit_hid` and `neopixel` libraries
3. Wire buttons to GND with pull-ups enabled

---

## **Customization**

* Change `button_map` for key assignments
* Modify `COLOR_W`, `COLOR_A`, etc., for LED colors
* Adjust `NUM_LEDS` and rainbow speed
