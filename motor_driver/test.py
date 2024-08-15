from motor import Motor
import math
import time

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 1, 115200)

def execute_app():
    # for bags in range(30): 
    while True:
        
        m1.set_position(10)
        # m1.set_position(4*math.pi + math.pi / 16 * bags)
        while m1.motor_command_done() is not True:
            pass
        # m1.set_position(4*math.pi / 2 - math.pi / 16 * bags)
        m1.set_position(-10)
        while m1.motor_command_done() is not True:
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
