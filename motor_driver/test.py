from motor import Motor
import math

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 2, 115200)

for bags in range(5):
    m1.set_position(math.pi / 2 + math.pi / 2 * bags)
    while m1.motor_command_done not True:
        pass
    m1.set_position(math.pi / 2 - math.pi / 2 * bags)
