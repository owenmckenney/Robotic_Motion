import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

step_pin = 21
dir_pin = 20
slp_pin = 16
spr = 3200
mode_pins = (1,7,8)
step_type = "Full")
delay = 1 / 2000
cw = 1
ccw = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(slp_pin, 0)
GPIO.output(dir_pin, cw)

GPIO.setup(mode_pins, GPIO.OUT)
resolution = {"Full": (0,0,0),
                "Half": (1,0,0),
                "1/4": (0,1,0),
                "1/8": (1,1,0),
                "1/16": (0,0,1),
                "1/32": (1,0,1)}
GPIO.output(mode_pins, resolution[step_type])

pins = {
        21 : {'name' : 'Step Pin', 'state' : GPIO.LOW}
        }

def step(delay):
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(delay)

def Rotate(d, spr, delay):
    GPIO.output(dir_pin, d)

    for x in range(spr / 4):
        step(delay)

    GPIO.cleanup();

@app.route("/")
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    template_data = {
            'pins' : pins
            }
    return render_template('stepper.html', **template_data)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

