from motor import Motor
import math
import time
import keyboard

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

NUM_BAGS_PER_COL = 30
NUM_BAGS_IN_BUFFER = 10

START_POS = 6
PUSHED_POS = 10

m1 = Motor(peripheral, 1, 115200, setVel=900, setAcc=25, setDec=25)
m1.set_position(START_POS)
def execute_app():
    # for bags in range(30): 
    bag = 0
    while True:

        keyboard.wait('space')

        if bag < NUM_BAGS_PER_COL:
            if bag < NUM_BAGS_IN_BUFFER:
                m1.set_position(PUSHED_POS - 0.4*bag)
                while m1.motor_command_done() is not True:
                    pass
                m1.set_position(START_POS)
                while m1.motor_command_done() is not True:
                    pass
            else:
                m1.set_position(PUSHED_POS)
                while m1.motor_command_done() is not True:
                    pass
                m1.set_position(START_POS)
                while m1.motor_command_done() is not True:
                    pass
            bag += 1
        else:
            bag = 0

def handle_cleanup():
    m1.stop()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
