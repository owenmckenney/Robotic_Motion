import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

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
        GPIO.setup(self.slp_pin, 0)
        GPIO.output(self.dir_pin, self.cw)

        GPIO.setup(self.mode_pins, GPIO.OUT)
        resolution = {"Full": (0,0,0),
                      "Half": (1,0,0),
                      "1/4": (0,1,0),
                      "1/8": (1,1,0),
                      "1/16": (0,0,1),
                      "1/32": (1,0,1)}
        GPIO.output(self.mode_pins, resolution[self.step_type]) 

    def Rotate(self, rotations, d):
        GPIO.output(self.dir_pin, d)
        
        for x in range(self.spr * rotations):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.delay)
        
        GPIO.cleanup()

    def Rotate_Ramp_Up_Down(self, rotations, d):
        GPIO.output(self.dir_pin, d)
        #accel_point = (self.spr / 4) * rotations
        accel_point = 50
        #accel_delay = self.delay * accel_point
        accel_delay = 0.025
        delay_increment = accel_delay / 50

        #.025

        print(accel_point, accel_delay)
        
        
        for x in range(self.spr * rotations):

            if x < accel_point or x > (self.spr * rotations) - accel_point:
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(accel_delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(accel_delay)
                
                if x < accel_point - 1:
                    accel_delay = accel_delay - (delay_increment)
                    print("Accelerated " + str(accel_delay))
                else:
                    accel_delay = accel_delay + delay_increment
                    print("De-accelerated " + str(accel_delay))
            
            else:
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(self.delay)
                GPIO.output(self.step_pin, GPIO.LOW)
                time.sleep(self.delay)
                print("Regular " + str(self.delay))



stepper1 = Stepper(20, 21, 16, 3200, (1,7,8), "Full")
#stepper1.Rotate(1, 1)
stepper1.Rotate_Ramp_Up_Down(1, 1)


