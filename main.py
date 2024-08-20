import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import multiprocessing

from staging_state_machine import main as stager

load_bags_event = multiprocessing.Event()


def print_msg(event):
    while True:
        event.wait()
        print("P2")
        time.sleep(1/60)
        event.clear()

stager_process = multiprocessing.Process(target=stager, args=(load_bags_event,))
test_proc = multiprocessing.Process(target=print_msg, args=(load_bags_event,))

def execute_app():
#     slider_homed.set()
#     push_slider.clear()
#     pusher_thread.start()
#     test_thread.start()
    stager_process.start()
    test_proc.start()
    while True:
        pass


def handle_cleanup():
#     # pusher_process.join()
#     pusher_thread.join()
#     test_thread.join()
#     print("done")
    stager_process.join()
    test_proc.join()

def main():
    execute_app()



if __name__=='__main__':
    main()
