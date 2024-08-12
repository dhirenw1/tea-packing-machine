from motor import Motor
import math

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 2, 115200)
m1.set_position(3.4*math.pi)