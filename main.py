import math
import time
from RPi import GPIO           # Allows us to call our GPIO pins and names it just GPIO
import threading

from pusher_state_machine import main as pusher_sm

slider_homed = threading.Event()
push_slider = threading.Event()

def test(slider_homed, push_slider):
    slider_homed_var = True
    while True:
        if push_slider.is_set():
                print("Pushing slider...")
                push_slider.clear()
                time.sleep(2)
                slider_homed_var = False
                slider_homed.clear()
                print("HOMING SLIDER...")
                time.sleep(5)
                slider_homed.set()
                slider_homed_var = True



pusher_thread = threading.Thread(target=pusher_sm, args=(slider_homed,push_slider))
test_thread = threading.Thread(target=test, args=(slider_homed,push_slider))

def execute_app():
    slider_homed.set()
    push_slider.clear()
    pusher_thread.start()
    test_thread.start()


def handle_cleanup():
    # pusher_process.join()
    pusher_thread.join()
    test_thread.join()
    print("done")

def main():
    try:
        slider_homed.set()
        execute_app()
    finally:
        handle_cleanup()

if __name__=='__main__':
    main()
