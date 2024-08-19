#!/usr/bin/env python

from motor_driver.motor import Motor
import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import threading
import argparse

GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

NUM_BAGS_PER_COL = 20
NUM_BAGS_IN_BUFFER = 10

START_POS = 6
PUSHED_POS = 10
STAGE_POS = 10*math.pi

m1 = Motor(peripheral, 1, 115200, setVel=1400, setAcc=25, setDec=25)
m1.set_abs_position(0)

def execute_app(slider_homed, push_slider):
    bag = 0
    # GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, bouncetime=1)
    while True:
        # if GPIO.event_detected(INPUT_PIN):
        # print(m1.get_read_digital_inputs())
        if m1.get_read_digital_inputs() & 0x4 == 0x0:
            print(bag)
            if bag < NUM_BAGS_PER_COL:
                if bag < NUM_BAGS_IN_BUFFER and slider_homed.is_set() is False:
                    print("Not homed")
                    m1.set_rel_position(PUSHED_POS - 0.4*bag)
                    while m1.motor_command_done() is not True:
                        pass
                    m1.set_abs_position(START_POS)
                    while m1.motor_command_done() is not True:
                        pass
                else:
                    print("homed")
                    m1.set_rel_position(PUSHED_POS)
                    while m1.motor_command_done() is not True:
                        pass
                    m1.set_abs_position(START_POS)
                    while m1.motor_command_done() is not True:
                        pass
                bag += 1
            else:
                bag = 0

                # Push slider to move column into stager
                m1.set_abs_position(STAGE_POS)
                while m1.motor_command_done() is not True:
                    pass
                print("UNSTAGING")
                m1.set_abs_position(START_POS)
                while m1.motor_command_done() is not True:
                    pass
                push_slider.set()

            while m1.get_read_digital_inputs() & 0x4 == 0:
                pass



def handle_cleanup():
    m1.stop()

def main(slider_homed, push_slider):
    try:
        execute_app(slider_homed, push_slider)
    finally:
        handle_cleanup()

# if __name__=='__main__':
    # execute_app()

#     parser = argparse.ArgumentParser(description='pusher state machine')
#     parser.add_argument('--event', metavar='event', required=True,
#                         help='slider event')
#     args = parser.parse_args()

#     main(args.event)
