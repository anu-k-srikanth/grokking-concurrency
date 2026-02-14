
import time 
import threading
from workers.SleepyWorker import SleepyWorker
from workers.SumOfSquares import SumOfSquares


def main():
    start = time.time()
    threads1 = []
    thread = threading.Thread()
    for i in range(9):
        # t = threading.Thread(target=calculate_sum_of_squares, args=(i*1000000, ))
        # t.start()
        t = SumOfSquares(i*1234569)
        threads1.append(t)
        # calculate_sum_of_squares(i * 1000000)

    for thread in threads1: 
        thread.join()

    print(f"Sum of squares calculation took {round(time.time() - start)} seconds to run")

    threads2 = []
    for i in range(3):
        t = SleepyWorker(seconds=i*i)
        # t = threading.Thread(target=time.sleep, args=(i, ))
        # time.sleep(i) 
        # t.start()
        threads2.append(t)
    
    for thread in threads2: 
        thread.join()

    print(f"Sleep took {round(time.time() - start)} seconds to run")
    
main()