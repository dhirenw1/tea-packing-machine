#!/usr/bin/env python
import math

class configuration:

    SERIAL_PERIPHERAL = '/dev/serial0'

    NUM_BAGS_PER_COL = 33
    NUM_BAGS_IN_BUFFER = 10
    NUM_COLS = 3

    START_POS = 6           # start position for pusher
    PUSHED_POS = 10         # pushed position
    STAGE_POS = 10*math.pi  # position to move pusher when staging
    BAG_WIDTH = 0.4         # Width of teabag
