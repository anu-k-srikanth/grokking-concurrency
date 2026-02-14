

from collections import deque
from threading import Lock, Thread
import time

class Buffer:
    def __init__(self, capacity):
        self.queue = deque()
        self.capacity = capacity
        self.mutex = Lock()
    
    def produce(self, string):  
        with self.mutex:
            while len(self.queue) == self.capacity:
                print(self.queue)
                time.sleep(1)
            self.queue.append(string)

    
    def consume(self):
        while len(self.queue) > 0:
            with self.mutex:
                while len(self.queue) == 0: 
                    print(self.queue)
                    time.sleep(1)
                self.queue.popleft()


class Producer(Thread):
    def __init__(self, buffer: Buffer, string: str):
        super().__init__()
        self.buffer = buffer
        self.string = string

    def run(self):
        print(f"{self.name} Trying to produce")
        self.buffer.produce(self.string)


class Consumer(Thread):
    def __init__(self, buffer: Buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        print(f"{self.name} Trying to consume")
        self.buffer.consume()


if __name__ == "__main__":
    common_buffer = Buffer(1)

    threads = []
    for i in range(10): 
        t1 = Producer(buffer=common_buffer, string=str(i))
        t1.start()
        threads.append(t1)

        t2 = Consumer(buffer=common_buffer)
        t2.start()
        threads.append(t2)

    for t in threads: 
        t.join()
