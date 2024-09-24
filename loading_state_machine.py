from motor_driver.motor import Motor
import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import threading
import yaml

# Pull configs from config file
with open('/home/tpm/tea-packing-machine/cfg/configuration.yaml') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

# GPIO pin for gripper
GRIPPER_PIN = cfg['GRIPPER1_SOL_PIN']
GPIO.setup(GRIPPER_PIN, GPIO.OUT)

motor_x = Motor(cfg['SERIAL_PERIPHERAL'], 2, 115200, setVel=2000, setAcc=15, setDec=15)
motor_y = Motor(cfg['SERIAL_PERIPHERAL'], 3, 115200, setVel=2000, setAcc=15, setDec=15)
motor_z = Motor(cfg['SERIAL_PERIPHERAL'], 4, 115200, setVel=2000, setAcc=15, setDec=15)

motor_x.set_abs_position(0)
motor_y.set_abs_position(0)
motor_z.set_abs_position(0)

def close_gripper():
    GPIO.output(GRIPPER_PIN, GPIO.HIGH)

def open_gripper():
    GPIO.output(GRIPPER_PIN, GPIO.LOW)

def loader(load_bags_event):
    if(load_bags_event.is_set()):
        # pseudocode: move gantry over bags
        # lower gantry over bags
        close_gripper()
        # lift gantry
        # move gantry above box
        # lower gantry into box
        open_gripper()
        # lift gantry

def execute_app(load_bags_event):
    loader(load_bags_event=load_bags_event)

def handle_cleanup():
    GPIO.cleanup()

def main(load_bags_event):
    try:
        execute_app(load_bags_event)
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()