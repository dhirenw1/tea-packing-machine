#!/usr/bin/env python

from motor_driver.motor import Motor
import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import threading

slider_flag = threading.Event()
slider_homed = slider_flag.is_set()
# push_slider = threading.Event()

GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4           # Sets our input pin, in this example I'm connecting our button to pin 4. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)           # Set our input pin to be an input

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

NUM_BAGS_PER_COL = 33
NUM_BAGS_IN_BUFFER = 10
NUM_COLS = 3

START_POS = 6
PUSHED_POS = 10
STAGE_POS = 10*math.pi
BAG_WIDTH = 0.4

m1 = Motor(peripheral, 1, 115200, setVel=2000, setAcc=15, setDec=15)
m1.set_abs_position(0)

def stage_column():
    slider_flag.clear()
    # print("Pushing slider...")
    time.sleep(0.01)
    # print("HOMING SLIDER...")
    time.sleep(0.01)
    # print("Staged")
    slider_flag.set()

def load_columns(load_bags_event):
    slider_flag.clear()
    # print("Pushing slider...")
    # time.sleep(0.01)
    # print("HOMING SLIDER...")
    # time.sleep(0.01)
    # print("Staged")
    slider_flag.set()
    load_bags_event.set()

def pusher(load_bags_event):
    bag = 0
    col = 0
    # GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, bouncetime=1)
    last_in = current_in = 0
    while True:
        # if GPIO.event_detected(INPUT_PIN):
        current_in = m1.get_read_digital_inputs() & 0x4 == 0x0

        if current_in is True and current_in != last_in:
            # print(bag)
            if bag < NUM_BAGS_PER_COL - 1 and slider_homed is False:
                # Load bags in buffer zone if pusher not ready
                if bag < NUM_BAGS_IN_BUFFER:
                    m1.set_rel_position(PUSHED_POS - BAG_WIDTH*bag)
                    m1.wait()
                    m1.set_abs_position(START_POS)
                    m1.wait()
                # Otherwise just load bags into normal staging zone
                else:
                    m1.set_rel_position(PUSHED_POS)
                    m1.wait()
                    m1.set_abs_position(START_POS)
                    m1.wait()

                bag += 1
            else:
                bag = 0
                # Push slider to move column into stager
                m1.set_abs_position(STAGE_POS)
                m1.wait()
                m1.set_abs_position(START_POS)
                m1.wait()

                if col < NUM_COLS:
                    col += 1
                    stager_thread = threading.Thread(target=stage_column)
                    stager_thread.start()

                else:
                    col = 0
                    load_thread = threading.Thread(target=load_columns, args=(load_bags_event,))
                    load_thread.start()

                            # # Read digital input to see if laser untripped
            # while m1.get_read_digital_inputs() & 0x4 == 0:
            #     pass
        last_in = current_in

def execute_app(load_bags_event):
    slider_flag.set()
    pusher(load_bags_event)

def handle_cleanup():
    m1.stop()

def main(load_bags_event):
    try:
        execute_app(load_bags_event)
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
