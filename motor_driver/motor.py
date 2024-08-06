#!/usr/bin/python3.11

import minimalmodbus

class Motor:
    def __init__(self, peripheral, nodeID, baud):
        self.nodeID = nodeID
        self.interface = minimalmodbus.Instrument(peripheral, nodeID)
        self.baud = baud
        self.interface.serial.baudrate = baud

    def __str__(self):
        return f"{self.interface}"