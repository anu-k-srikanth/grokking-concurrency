from collections import deque
import random
from threading import Lock, Thread
import time


queue = deque() 
MAX_CAPACITY = 1
mutex = Lock()


class Producer(Thread):
    def __init__(self, string):
        super().__init__()
        self.string = string
    
    def run(self):
        done_flag = False
        while not done_flag:
            mutex.acquire()
            if len(queue) == MAX_CAPACITY:
                mutex.release() 
                time.sleep(2)
                print(f"Producer sleeps")
            else: 
                queue.append(self.string)
                print(f"Producer produced item {self.string}")
                done_flag = True
        mutex.release()
        time.sleep(random.randrange(1,5))


class Consumer(Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        done_flag = False
        while not done_flag:
            mutex.acquire()
            if len(queue) == 0:
                mutex.release() 
                time.sleep(2)
                print(f"Consumer sleeps")
            else: 
                item = queue.popleft()
                print(f"Consumer consumed item {item}")
                done_flag = True
        mutex.release()
        time.sleep(random.randrange(1, 5))
    

if __name__ == "__main__":
    threads = []
    for i in range(20):
        p = Producer(str(i))
        c = Consumer()
        p.start()
        c.start()
        threads.extend([p,c])
    
    for t in threads: 
        t.join()
    
