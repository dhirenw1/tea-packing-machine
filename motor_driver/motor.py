#!/usr/bin/python3.11

import minimalmodbus
import math
import time
import sys

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
DIG_IN_STATE_R =      0x0179

# Operation modes
NO_MODE     = 0 
ABS_POS_MODE    = 0x01 
REL_POS_MODE    = 0x41
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

int32_max = (2**31) - 1
int32_min = (-2**31)


DIRECTION_DICT = {'CW' : 0, 'CCW' : 1}

class Motor:
    def __init__(self, peripheral, nodeID, baud, pulsesPerRev=PULSES_PER_REV, setVel=SET_VEL, setAcc=SET_ACC, setDec=SET_DEC, setPauseTime=SET_PAUSE_TIME):
        self.nodeID = nodeID
        self.interface = minimalmodbus.Instrument(peripheral, nodeID, debug=False)
        self.baud = baud
        self.setVel = setVel
        self.setAcc = setAcc
        self.setDec = setDec
        self.setPauseTime = setPauseTime
        
        self.interface.serial.baudrate = baud
        self.pulses_per_rev = pulsesPerRev
        self.interface.mode = minimalmodbus.MODE_RTU
        self.interface.handle_local_echo=True
        try:
            self.interface.write_register(PULSES_PER_REV_R, self.pulses_per_rev)  # Set pulses per rev
            self.interface.write_register(PR_0_MODE_R, ABS_POS_MODE)         # Set operation mode
        except TypeError as error:
            print(error, "Incorrect datatype used while writing to register")
        except ValueError as error:
            print(error, "Value too out of bounds for write to register")
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def __str__(self):
        return f"{self.interface}, Pulses/Rev: {self.pulses_per_rev}"

    def radians_to_pulses(self, inputRadians):
        pulses = int((inputRadians) / (2 * math.pi) * self.pulses_per_rev)
        # Protect from pulse values outside of bounds
        if pulses > int32_max:
            pulses = int32_max
        if pulses < int32_min:
            pulses = int32_min
        return pulses

    def set_operation_mode(self, mode):
        self.interface.write_register(PR_0_MODE_R, mode, 0)

    # position in radians
    def set_rel_position(self, position, vel=None, acc=None, dec=None):
        if vel is None:
            vel=self.setVel
        if acc is None:
            acc=self.setAcc
        if dec is None:            
            dec=self.setDec
            
        # Convert radians to pulses
        pulses = self.radians_to_pulses(position)

        hex_pos = hex(pulses & 0xffffffff).split('x')[-1]

        # Split out position into 2 parts if bigger than 2 bytes, or 4 hex values
        if(len(hex_pos) > 4):
            pos_h = int('0x' + hex_pos[:len(hex_pos)//2], 16)
            pos_l = int('0x' + hex_pos[len(hex_pos)//2:], 16)
        else:
            pos_h = 0
            pos_l = int('0x' + hex_pos, 16)
        
        try:
            self.interface.write_registers(PR_0_MODE_R, [REL_POS_MODE, pos_h, pos_l, vel, acc, dec, SET_PAUSE_TIME, TRIGGER])
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def set_abs_position(self, position, vel=None, acc=None, dec=None):
        if vel is None:
            vel=self.setVel
        if acc is None:
            acc=self.setAcc
        if dec is None:            
            dec=self.setDec
            
        # Convert radians to pulses
        pulses = self.radians_to_pulses(position)

        hex_pos = hex(pulses & 0xffffffff).split('x')[-1]

        # Split out position into 2 parts if bigger than 2 bytes, or 4 hex values
        if(len(hex_pos) > 4):
            pos_h = int('0x' + hex_pos[:len(hex_pos)//2], 16)
            pos_l = int('0x' + hex_pos[len(hex_pos)//2:], 16)
        else:
            pos_h = 0
            pos_l = int('0x' + hex_pos, 16)
        
        try:
            self.interface.write_registers(PR_0_MODE_R, [ABS_POS_MODE, pos_h, pos_l, vel, acc, dec, SET_PAUSE_TIME, TRIGGER])
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def stop(self):
        self.interface.write_register(PR_0_MODE_R, STOP)

    def get_status(self):
        try:
            return self.interface.read_register(MOTION_STATUS_R)
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID) 
            sys.exit(0)
    
    def motor_command_done(self):
        if self.get_status() & 0x10 > 0:
            return True
        else:
            return False

    def reset_current_alarm(self):
        try:
            self.interface.write_register(CONTROL_WORD_R, 0x1111)
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def reset_history_alarm(self):
        try:
            self.interface.write_register(CONTROL_WORD_R, 0x1122)
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def get_current_alarm(self):
        try:
            return self.interface.read_register(CURRENT_ALARM_R)
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)

    def get_read_digital_inputs(self):
        try:
            return self.interface.read_register(DIG_IN_STATE_R)
        except (minimalmodbus.NoResponseError,  minimalmodbus.InvalidResponseError) as error:
            print(error, "Node:", self.nodeID)
            sys.exit(0)