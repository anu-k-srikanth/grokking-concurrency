import os
from multiprocessing import Process
import time
import threading

def create_child_process():
    print(f"I am child process {os.getpid()}")
    print(f"My parent is {os.getppid()}")
    time.sleep(5)

def create_process(children):
    start = time.time()
    print(f"I am a parent process {os.getpid()}")
    for i in range(children): 
        print(f"Create child process {i}")
        Process(target=create_child_process).start()
    print(f"This method took {time.time() - start} seconds")


def create_threads(number):
    print(f"The active thread count is: {threading.active_count()}")

    for i in range(number):
        t = threading.Thread(target=time.sleep, args=(3, )).start()
        print(f"The thread native id is: {threading.get_native_id()}")
    
    print(f"The active thread count is: {threading.active_count()}")
    print("done creating threads")

if __name__ == "__main__":
    num_children = 3
#  create_process(num_children)
    create_threads(4)