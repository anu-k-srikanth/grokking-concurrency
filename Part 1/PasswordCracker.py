
from queue import Queue
import time
import threading

class PasswordCracker: 
    def __init__(self, length): 
        self.length = length
        self.password = ((10 ** (self.length+1)) - 1) // 2
        self.queue = Queue()

    def io_bound_serially(self, waits):
        before = time.time()

        for i in range(waits):
            time.sleep(i)

        print(f"io_bound_serially takes {time.time() - before} seconds")


    def io_bound_parallely(self, waits):
        before = time.time()

        threads = []
        for i in range(waits):
            t = threading.Thread(target=time.sleep, args=(i, )) 
            t.start()
            threads.append(t)
        
        for t in threads: 
            t.join()

        print(f"io_bound_parallely takes {time.time() - before} seconds")

    def get_chunks(self, min_number, max_number, num_chunks):
        chunks = []
        chunk_size = (max_number - min_number) // num_chunks
        start, end = 0, chunk_size
        while end <= max_number:
            chunks.append((start, end))
            start, end = end, end + chunk_size
        if start < max_number: 
            chunks.append((start, max_number))
        return chunks
            

    def generate_passwords_serially(self):
        before = time.time()
        min_number = 10 ** self.length
        max_number = (10 ** (self.length+1)) - 1

        chunks = self.get_chunks(min_number, max_number, 4)
        print(chunks)

        result = self._check_passwords_in_range(min_number, max_number)

        print(f"generate_passwords_serially found password in {time.time() - before} seconds")
        return result

    def generate_passwords_parallel(self):
        min_number = 10 ** self.length
        max_number = (10 ** (self.length+1)) - 1

        chunks = self.get_chunks(min_number, max_number, 4)
        print(chunks)

        threads = []
        for chunk in chunks: 
            t = threading.Thread(target=self._check_passwords_in_range, args=(chunk[0], chunk[1]))
            t.start()
            threads.append(t)
        
        for t in threads: 
            t.join()

        while self.queue.empty: 
            result = self.queue.get()
            if result == True: return True
        return False


    def _check_passwords_in_range(self, min, max):
        for password in range(min, max):
            if self.check_password(password):
                self.queue.put(True)
                return 
        return self.queue.put(False)
    
    def has_found_password(self):
        before = time.time()
        found = self.generate_passwords_parallel()
        
        print(f"generate_passwords_parallel found password in {time.time() - before} seconds")
        return found
        

    def check_password(self, password):
        return self.password == password


pc = PasswordCracker(length=6)
# print(pc.has_found_password())
# print(pc.generate_passwords_serially())


print(pc.io_bound_parallely(5))
print(pc.io_bound_serially(5))