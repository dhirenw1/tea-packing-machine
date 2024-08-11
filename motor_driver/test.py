from motor import Motor

# raspi serial peripheral used by Modbus RTU
peripheral = '/dev/serial0'

m1 = Motor(peripheral, 2, 115200)
m1.set_position(2000)