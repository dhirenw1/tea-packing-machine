import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import multiprocessing

from pusher_state_machine import main as pusher_sm

pusher_proc = multiprocessing.Process(target=pusher_sm)

def execute_app():
    pusher_proc.start()

def handle_cleanup():
    pusher_proc.join()

def main():
    try:
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
