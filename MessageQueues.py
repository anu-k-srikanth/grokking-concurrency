from threading import Thread, current_thread
from queue import Queue
import time

class Worker(Thread):
    def __init__(self, queue: Queue, id):
        super().__init__(name=str(id))
        self.queue = queue
        self.start()

    def run(self):
        while not self.queue.empty(): 
            print(f"Recieved item: {self.queue.get()} in thread {current_thread().name}")
            time.sleep(1)

def main():
    queue = Queue()
    for i in range(10):
        queue.put(i)

    threads = []
    for i in range(4):
        t = Worker(queue, i+1)
        threads.append(t)

    for t in threads: 
        t.join()
    
main()