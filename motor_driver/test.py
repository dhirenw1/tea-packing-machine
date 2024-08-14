from motor import Motor
import math
import time

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 1, 115200)

for bags in range(30): 
    m1.set_position(4*math.pi + math.pi / 16 * bags)
    while m1.motor_command_done() is not True:
        pass
    m1.set_position(4*math.pi / 2 - math.pi / 16 * bags)

# m1.stop()
