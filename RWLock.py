class RWLock:
    def __init__(self):
        self.read_lock = Lock()
        self.write_lock = Lock()
        self.readers = 0

    def acquire_read_lock(self):
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1: 
            self.write_lock.acquire()
        self.read_lock.release()

    def acquire_write_lock(self):
        self.write_lock.acquire()

    def release_read_lock(self):
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0: 
            self.write_lock.release()
        self.read_lock.release()

    def release_write_lock(self):
        self.write_lock.release() 
