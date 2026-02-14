
import random
from threading import Lock, Thread
import time

class RWLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()

    def acquire_read(self):
        # The read lock here making sure that the update to increase the number of readers is atomic. 
        # It does not need to block out other readers so we free it at the end. 
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1: 
            # This will acquire the lock to block out any writers while reading is going on.
            # If a write has acquired this lock, then this operation will stall here until the write releases the lock
            self.write_lock.acquire()
        self.read_lock.release()

    def release_read(self):
        assert(self.readers > 0)
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.write_lock.release()
        self.read_lock.release()

    def acquire_write(self):
        self.write_lock.acquire()

    def release_write(self):
        self.write_lock.release()


rwlock = RWLock()
counter = 0

class User(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.start()

    def run(self):
        while True:
            rwlock.acquire_read()
            print(f"User {self.name} is reading value {counter}")
            rwlock.release_read()
            time.sleep(random.randrange(1,5))

class Librarian(Thread):
    def __init__(self):
        super().__init__()
        self.start()

    def run(self):
        global counter
        while True:
            rwlock.acquire_write()
            counter += 1
            print(f"Librarian is writing value {counter}")
            rwlock.release_write()
            time.sleep(random.randrange(1,5))

users = []
for i in range(3):
    u = User(str(i))
    users.append(u)

Librarian()