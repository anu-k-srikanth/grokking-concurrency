from threading import Lock, Thread
import time


dumplings = 9

class Philosopher(Thread):
    def __init__(self, name, protect_dumplings, left_chopstick: Lock, right_chopstick: Lock):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.protect_dumplings = protect_dumplings

    def eat_dumplings(self):
        global dumplings
        while dumplings > 0:
            self.left_chopstick.acquire()
            print(f"Philosopher {self.name} acquired left chopstick")
            if self.right_chopstick.locked:
                print(f"Philosopher {self.name} politely concedes")
            else:
                self.right_chopstick.acquire()
                print(f"Philosopher {self.name} acquired right chopstick")
                with self.protect_dumplings: 
                    if dumplings > 0: 
                        dumplings -= 1
                print(f"Philosopher {self.name} ate dumpling. There are {dumplings} dumplings left")
                self.right_chopstick.release()
                print(f"Philosopher {self.name} released right chopstick")
            self.left_chopstick.release()
            print(f"Philosopher {self.name} released left chopstick")
            time.sleep(0.1)

    def run(self):
        self.eat_dumplings()

if __name__ == "__main__":
    protect_dumplings = Lock()
    left_chopstick = Lock()
    right_chopstick = Lock()

    philosophers = []
    for i in range(2):
        t = Philosopher("Philosopher-" + str(i), protect_dumplings, left_chopstick, right_chopstick)
        t.start()
        philosophers.append(t)

    for t in philosophers:
        t.join()
    