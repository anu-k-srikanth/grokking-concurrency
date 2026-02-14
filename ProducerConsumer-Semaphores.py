

from collections import deque
import random
from threading import Lock, Semaphore, Thread
import time

MAX_CAPACITY = 5
can_add = Semaphore(MAX_CAPACITY)
can_remove = Semaphore()
mutex = Lock()
queue = deque()
SENTINEL = None

class Producer(Thread):
    def __init__(self, string):
        super().__init__()
        self.string = string
    
    def run(self):
        can_add.acquire()
        with mutex: 
            queue.append(self.string)
            print(f"{self.name} Producing {self.string}")
        can_remove.release()
        time.sleep(random.randrange(1,5)*0.1)

class Consumer(Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        while True:
            can_remove.acquire()
            with mutex:
                item = queue.popleft()
                print(f"{self.name} Consuming {item}")
            can_add.release()

            if item is SENTINEL:
                print(f"{self.name} Got sentinel. Exiting")
                break

            time.sleep(random.randrange(1,5)*0.1)
    
if __name__ == "__main__":
    producers = []
    consumers = []
    for i in range(6):
        p = Producer(str(i))
        p.start()
        producers.append(p)

    for i in range(3):
        c = Consumer()
        c.start()
        consumers.append(c)
    
    for t in producers: 
        t.join()

    for _ in range(len(consumers)):
        can_add.acquire()
        queue.append(SENTINEL)
        can_remove.release()

    for t in consumers:
        t.join()


