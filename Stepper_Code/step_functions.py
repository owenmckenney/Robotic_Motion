from time import sleep
import RPi.GPIO as GPIO

direction = 20
step = 21
cw = 1
ccw = 0
spr = 200
sleep = 16


class Stepper:

    def __init__(self, dir_pin, step_pin, slp_pin, spr, mode_pins, step_type):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.slp_pin = slp_pin
        self.spr = spr
        self.mode_pins = mode_pins
        self.step_type = step_type
        self.delay = 1 / 2000
        self.cw = 1
        self.ccw = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.slp_pin, 1)
        GPIO.output(direction, cw)

        GPIO.setup(self.mode_pins, GPIO.OUT)
        resolution = {"Full": (0,0,0),
                      "Half": (1,0,0),
                      "1/4": (0,1,0),
                      "1/8": (1,1,0),
                      "1/16": (0,0,1),
                      "1/32": (1,0,1)}
        GPIO.output(self.mode_pins, self.step_type) 

    def Rotate(self, rotations, d):
        GPIO.output(self.direction, d)
        
        for x in range(self.spr):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(delay)

s = Stepper(20, 21, 16, 1600, (1,7,8), "Full")
s.Rotate(1, 1)

