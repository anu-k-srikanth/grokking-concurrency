import random
from threading import Lock, Semaphore, Thread, current_thread
import time


class Garage: 
    def __init__(self, capacity):
        self._semaphore = Semaphore(capacity)
        self._cars_lock = Lock()
        self.parked_cars = set()
        
    def enter(self, car_name):
        self._semaphore.acquire()
        self._cars_lock.acquire()
        self.parked_cars.add(car_name)
        print(f"Car {car_name} parked")
        self._cars_lock.release()
    
    def leave(self, car_name):
        self._cars_lock.acquire()
        self.parked_cars.remove(car_name)
        print(f"Car {car_name} left")
        self._semaphore.release()
        self._cars_lock.release()

def park_car(garage: Garage, car_name):
    garage.enter(car_name)
    time.sleep(random.randrange(1, 5) * 0.1)
    garage.leave(car_name)

if __name__ == "__main__":
    garage = Garage(3)

    threads = []
    for i in range(15):
        t = Thread(target=park_car, args=(garage, "car_name_" + str(i)))
        print(f"{t.name} is parking")
        t.start()
        threads.append(t)
    
    for t in threads: 
        t.join()





