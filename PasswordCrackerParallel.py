
from queue import Queue
import time
import threading
from multiprocessing import Pool
import multiprocessing

def get_chunks(min_number, max_number, num_chunks):
    chunks = []
    chunk_size = (max_number - min_number) // num_chunks
    start, end = min_number, chunk_size
    while end <= max_number:
        chunks.append((start, end))
        start, end = end, end + chunk_size
    if start < max_number: 
        chunks.append((start, max_number))
    return chunks
        
def main():
    length = 7
    min_number = 10 ** length
    max_number = (10 ** (length+1)) - 1
    # chunks = get_chunks(min_number, max_number, 4)
    # print(chunks)

    start = time.time()
    with Pool() as pool: 
        arguments = ((min, max) for min, max in get_chunks(min_number, max_number, 4))
        results = pool.starmap(_check_passwords_in_range_parallel, arguments)

        print(f"Waiting for pool tasks to finish")
        pool.close() # No more new tasks to submit
        pool.join() # Close the pool

    result = [res for res in results]
    print(f"Results {result}")
    print(f"Time to completion with multiple process is {time.time() - start}")
    # Time to completion with multiple process is 15.406512022018433

    start_serial = time.time()
    chunks = get_chunks(min_number, max_number, 4)

    resultsSerial = []
    for chunk in chunks: 
        resultsSerial.append(_check_passwords_in_range_parallel(chunk[0], chunk[1]))
    print(f"Results {resultsSerial}")
    print(f"Time to completion with multiple process is {time.time() - start_serial}")
    # Time to completion with multiple process is 51.54315400123596
    

def _check_passwords_in_range_parallel(min, max):
    print(f"{multiprocessing.current_process().name}: Processing {min} to {max}")
    for password in range(min, max):
        # print(f"{threading.current_thread().name} thread here")
        if check_password(password):
            return True
    return False

def check_password(password):
    return password == 0

if __name__ == "__main__":
    main()