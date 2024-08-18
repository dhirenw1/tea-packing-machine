#!/usr/bin/env python

from motor import Motor
import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
 
GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

NUM_BAGS_PER_COL = 30
NUM_BAGS_IN_BUFFER = 10

START_POS = 6
PUSHED_POS = 10

m1 = Motor(peripheral, 1, 115200, setVel=1400, setAcc=25, setDec=25)
m1.set_abs_position(0)

def execute_app():
    bag = 0
    GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, bouncetime=1)
    while True:

        # if GPIO.event_detected(INPUT_PIN):
        # print(m1.get_read_digital_inputs())
        if m1.get_read_digital_inputs() & 0x4 == 0x0:
            print(bag)
            if bag < NUM_BAGS_PER_COL:
                if bag < NUM_BAGS_IN_BUFFER:
                    m1.set_rel_position(PUSHED_POS - 0.4*bag)
                    while m1.motor_command_done() is not True:
                        pass
                    m1.set_abs_position(START_POS)
                    while m1.motor_command_done() is not True:
                        pass
                else:
                    m1.set_rel_position(PUSHED_POS)
                    while m1.motor_command_done() is not True:
                        pass
                    m1.set_abs_position(START_POS)
                    while m1.motor_command_done() is not True:
                        pass
                bag += 1
            else:
                bag = 0
            while m1.get_read_digital_inputs() & 0x4 == 0:
                pass



def handle_cleanup():
    m1.stop()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
