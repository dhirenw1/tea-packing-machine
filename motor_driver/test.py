from motor import Motor
import math
import time

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 1, 115200)

while True:
    for bags in range(10):
        m1.set_position(10 - 0.4*bags)
        while m1.motor_command_done() is not True:
            pass
        m1.set_position(-10 + 0.4*bags)
        while m1.motor_command_done() is not True:
            pass

# m1.stop()
