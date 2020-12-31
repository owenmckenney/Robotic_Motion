import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)

pins = {
        2 : {'name' : 'GPIO 2', 'state' : GPIO.LOW}
        }

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)



@app.route("/")
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    template_data = {
            'pins' : pins
            }
    
    return render_template('main.html', **template_data)

@app.route("/<change_pin>/<action>")
def action(change_pin, action):
    change_pin = int(change_pin)
    device_name = pins[change_pin]['name']

    if action == "on":
        GPIO.output(change_pin, GPIO.HIGH)
        message = "Turned " + device_name + " on"
    if action == "off":
        GPIO.output(change_pin, GPIO.LOW)
        message = "Turned " + device_name + " off"

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    template_data = {
            'pins' : pins
            }

    return render_template('main.html', **template_data)


'''

def index():
    return render_template('index.html')
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

