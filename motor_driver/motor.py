#!/usr/bin/python3.11

import minimalmodbus
import math
import time

# REGISTERS
PR_0_MODE_R =         0x6200
PR_0_POS_H_R =        0x6201
PR_0_POS_L_R =        0x6202
PR_0_VEL_R =          0x6203
PR_0_ACC_R =          0x6204
PR_0_DECEL_R =        0x6205
PR_0_PAUSE_TIME_R =   0x6206
PR_0_SPEC_PARAM_R =   0x6207

MOTION_STATUS_R =     0x1003
CONTROL_WORD_R =      0x1801
CURRENT_ALARM_R =     0x2203
PULSES_PER_REV_R =    0x0001
MOTOR_DIRECTON_R =    0x0007

# Operation modes
NO_MODE     = 0 
POS_MODE    = 0x41
VEL_MODE    = 2
HOMING_MODE = 3

# Pulse per rev
PULSES_PER_REV = 10000

# Initialization constants
SET_VEL = 400   # RPM
SET_ACC = 20    # ms/1000RPM
SET_DEC = 20    # ms/1000RPM
SET_PAUSE_TIME = 0
TRIGGER = 0x10
STOP = 0x40

int16_max = 2**16 - 1

DIRECTION_DICT = {'CW' : 0, 'CCW' : 1}

class Motor:
    def __init__(self, peripheral, nodeID, baud, pulsesPerRev=PULSES_PER_REV):
        self.nodeID = nodeID
        self.interface = minimalmodbus.Instrument(peripheral, nodeID, debug=False)
        self.baud = baud
        self.interface.serial.baudrate = baud
        self.pulses_per_rev = pulsesPerRev
        self.interface.mode = minimalmodbus.MODE_RTU
        self.interface.handle_local_echo=True
        self.interface.write_register(PULSES_PER_REV_R, self.pulses_per_rev)  # Set pulses per rev
        self.interface.write_register(PR_0_MODE_R, POS_MODE)         # Set operation mode

    def __str__(self):
        return f"{self.interface}, Pulses/Rev: {self.pulses_per_rev}"

    def radians_to_pulses(self, inputRadians):
        if inputRadians < 0:
            dir = DIRECTION_DICT['CCW']
        else:
            dir = DIRECTION_DICT['CW']
        return dir, int((inputRadians) / (2 * math.pi) * self.pulses_per_rev)

    def set_operation_mode(self, mode):
        self.interface.write_register(PR_0_MODE_R, mode, 0)

    # position in radians
    def set_position(self, position):
        # Convert radians to pulses
        dir, pulses = self.radians_to_pulses(position)
        hex_pos = hex(pulses & 0xffffffff).split('x')[-1]
        # Split out position into 2 parts if bigger than 2^16
        if(len(hex_pos) > 4):
            pos_h = int('0x' + hex_pos[:len(hex_pos)//2], 16)
            pos_l = int('0x' + hex_pos[len(hex_pos)//2:], 16)
        else:
            pos_h = 0
            pos_l = int('0x' + hex_pos, 16)
        print(hex_pos, pos_h, pos_l, pulses)
        # self.interface.write_register(MOTOR_DIRECTON_R, dir)
        self.interface.write_registers(PR_0_MODE_R, [POS_MODE, pos_h, pos_l, SET_VEL, SET_ACC, SET_DEC, SET_PAUSE_TIME, TRIGGER])

    def stop(self):
        self.interface.write_register(PR_0_MODE_R, STOP)

    def get_status(self):
        return self.interface.read_register(MOTION_STATUS_R)
    
    def motor_command_done(self):
        if self.get_status() & 0x10 > 0:
            return True
        else:
            return False

    def reset_current_alarm(self):
        self.interface.write_register(CONTROL_WORD_R, 0x1111)

    def reset_history_alarm(self):
        self.interface.write_register(CONTROL_WORD_R, 0x1122)

    def get_current_alarm(self):
        return self.interface.read_register(CURRENT_ALARM_R)