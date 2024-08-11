#!/usr/bin/python3.11

import minimalmodbus

# REGISTERS
PR_0_MODE_R =         0x6200
PR_0_POS_H_R =        0x6201
PR_0_POS_L_R =        0x6202
PR_0_VEL_R =          0x6203
PR_0_ACC_R =          0x6204
PR_0_DECEL_R =        0x6205
PR_0_PAUSE_TIME_R =   0x6206
PR_0_SPEC_PARAM_R =   0x6207

# Operation modes
NO_MODE     = 0 
POS_MODE    = 1
VEL_MODE    = 2
HOMING_MODE = 3

SET_VEL = 600
SET_ACC = 50
SET_DEC = 50
SET_PAUSE_TIME = 0
TRIGGER = 0x10
STOP = 0x40

class Motor:
    def __init__(self, peripheral, nodeID, baud):
        self.nodeID = nodeID
        self.interface = minimalmodbus.Instrument(peripheral, nodeID)
        self.baud = baud
        self.interface.serial.baudrate = baud
        self.interface.write_register(PR_0_MODE_R, POS_MODE, 0)         # Set operation mode
        # self.interface.write_register()

    def __str__(self):
        return f"{self.interface}"

    def set_operation_mode(self, mode):
        self.interface.write_register(PR_0_MODE_R, mode, 0)

    def set_position(self, position):
        # Convert decimal position into two high and low hex values, convert the high and low back to ints, then write
        hex_pos = hex(position).split('x')[-1]
        pos_h = int('0x' + hex_pos[:len(hex_pos)//2], 16)
        pos_l = int('0x' + hex_pos[len(hex_pos)//2:], 16)
        self.interface.write_registers(PR_0_MODE_R, [POS_MODE, pos_h, pos_l, SET_VEL, SET_ACC, SET_DEC, SET_PAUSE_TIME, TRIGGER])

    def stop(self):
        self.interface.write_register(PR_0_MODE_R, STOP)