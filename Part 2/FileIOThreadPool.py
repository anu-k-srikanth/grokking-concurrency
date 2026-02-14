import glob
from multiprocessing.pool import ThreadPool
import os
import time

def search_files(file_location, search_string):
    with open(file_location, "r", encoding="utf8") as file: 
        time.sleep(0.1)
        return search_string in file.read()
    
def search_files_serially(file_locations, search_string):
    for file_location in file_locations:
        if search_files(file_location, search_string): 
            print(f"Found result: {search_string} at {file_location}") 

def search_files_concurrently(file_locations, search_string):
    with ThreadPool() as pool: 
        results = pool.starmap(search_files, ((file_location, search_string) for file_location in file_locations))
        for (result, file_name) in zip(results, file_locations):
            if result: 
                print(f"Found result: {result} at {file_name}")

if __name__ == "__main__":
    file_locations = list(
    glob.glob(f"{os.path.abspath(os.getcwd())}/*.py"))
    search_string = input("What word are you trying to find?: ")

    start_time = time.perf_counter()
    search_files_concurrently(file_locations, search_string)
    process_time = time.perf_counter() - start_time
    print(f"CONCURRENT PROCESS TIME: {process_time}")

    start_time_serial = time.perf_counter()
    search_files_serially(file_locations, search_string)
    serial_process_time = time.perf_counter() - start_time_serial
    print(f"SERIAL PROCESS TIME: {serial_process_time}")