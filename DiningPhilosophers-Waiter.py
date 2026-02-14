from threading import Lock, Thread
import time


dumplings = 9
class Waiter():
    def __init__(self):
        self.mutex = Lock()

    def ask_for_chopsticks(self, name, left, right):
        left.acquire()
        print(f"Philosopher {name} acquired left chopstick")
        right.acquire()
        print(f"Philosopher {name} acquired right chopstick")

    def release_chopsticks(self, name, left, right):
        left.release()
        print(f"Philosopher {name} acquired left chopstick")
        right.release()
        print(f"Philosopher {name} acquired right chopstick")


class Philosopher(Thread):
    def __init__(self, name, protect_dumplings, left_chopstick, right_chopstick, waiter: Waiter):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.protect_dumplings = protect_dumplings
        self.waiter = waiter

    def eat_dumplings(self):
        global dumplings
        while dumplings > 0:
            self.waiter.ask_for_chopsticks(self.name, left_chopstick, right_chopstick)
            with self.protect_dumplings: 
                if dumplings > 0: 
                    dumplings -= 1
            print(f"Philosopher {self.name} ate dumpling. There are {dumplings} dumplings left")
            self.waiter.release_chopsticks(self.name, left_chopstick, right_chopstick)
            time.sleep(0.1)

    def run(self):
        self.eat_dumplings()

if __name__ == "__main__":
    protect_dumplings = Lock()
    left_chopstick = Lock()
    right_chopstick = Lock()
    waiter = Waiter()

    philosophers = []
    for i in range(2):
        t = Philosopher("Philosopher-" + str(i), protect_dumplings, left_chopstick, right_chopstick, waiter)
        t.start()
        philosophers.append(t)

    for t in philosophers:
        t.join()
    