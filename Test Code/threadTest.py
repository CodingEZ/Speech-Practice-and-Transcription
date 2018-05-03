from _thread import start_new_thread
import time

def printer():
    time.sleep(2)
    print(1)

print(2)
start_new_thread(printer, ())
print(3)
time.sleep(4)
