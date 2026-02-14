from threading import Thread
from queue import Queue
import time
import random


class WasherWorker(Thread):
    def __init__(self, washer_queue: Queue, dryer_queue: Queue):
        super().__init__()
        self.washer_queue = washer_queue
        self.dryer_queue = dryer_queue

    def run(self):
        while True:
            load = self.washer_queue.get()
            if load is None: 
                self.washer_queue.task_done()
                break
            print(f"Running washer laundry load {load}")
            time.sleep(2)
            print(f"Laundry {load} completed. Time to dry")
            self.dryer_queue.put(load)
            self.washer_queue.task_done()


class DryerWorker(Thread):
    def __init__(self, dryer_queue: Queue, folding_queue: Queue):
        super().__init__()
        self.dryer_queue = dryer_queue
        self.folding_queue = folding_queue

    def run(self):
        while True:
            load = self.dryer_queue.get()
            if load is None: 
                self.dryer_queue.task_done()
                break
            print(f"Running dryer laundry load {load}")
            time.sleep(2)
            print(f"Laundry {load} completed. Time to fold")
            self.folding_queue.put(load)
            self.dryer_queue.task_done()

def main():
    washer_queue = Queue()
    for load in range(7):
        washer_queue.put(load)
    
    max_washer_threads = random.randrange(1, 5)
    dryer_queue = Queue()
    washer_threads = []

    for _ in range(max_washer_threads):
        t = WasherWorker(washer_queue, dryer_queue)
        t.start()
        washer_threads.append(t)
    
    # This will check whether all of the items are processed from the washer queue
    # This will block until that is true
    washer_queue.join()

    # Add sentinel values for each thread that was created so that they can each shut down 
    for _ in washer_threads:
        washer_queue.put(None)
    # Block until all washer_threads are complete (this happens when theyre all shut down)
    for t in washer_threads:
        t.join()

    dryer_threads = []
    folding_queue = Queue()
    max_dryer_threads = random.randrange(1, 5)

    for _ in range(max_dryer_threads):
        t = DryerWorker(dryer_queue, folding_queue)
        t.start()
        dryer_threads.append(t)

    dryer_queue.join()

    for _ in dryer_threads: 
        dryer_queue.put(None)
    for t in dryer_threads: 
        t.join()

    print("\nAll laundry completed successfully!\n")

main()