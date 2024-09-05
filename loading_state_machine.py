from motor_driver.motor import Motor
import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import threading



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