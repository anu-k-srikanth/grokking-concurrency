import sys
from threading import Lock, Thread
import time


class SynchronizedBankAccount:
    def __init__(self):
        self.money = 0
        self.mutex = Lock()

    def deposit(self, amount):
        self.mutex.acquire()
        if amount > 0:
            self.money += amount
            self.mutex.release()
        else: 
            raise ValueError("Error depositing")

    def withdraw(self, amount):
        self.mutex.acquire()
        if amount > 0: 
            self.money -= amount
            self.mutex.release()
        else: 
            raise ValueError("Error withdrawing")


class UnsynchronizedBankAccount:
    def __init__(self):
        self.money = 0

    def deposit(self, amount):
        if amount > 0:
            self.money += amount
        else: 
            raise ValueError("Error depositing")

    def withdraw(self, amount):
        if amount > 0: 
            self.money -= amount
        else: 
            raise ValueError("Error withdrawing")

class ATM(Thread):
    def __init__(self, account):
        super().__init__()
        self.account = account

    def run(self):
        self.account.deposit(10)
        time.sleep(0.001)
        self.account.withdraw(10)


if __name__ == "__main__":
    THREAD_DELAY = 1e-16
    # THREAD_DELAY = 0.0000000000000000000000005
    unsynchronized_account = UnsynchronizedBankAccount()
    sys.setswitchinterval(THREAD_DELAY)

    start = time.perf_counter()
    threads = []
    for _ in range(1000):
        t = ATM(unsynchronized_account)
        t.start()
        threads.append(t)

    for t in threads: 
        t.join()

    print(f"unsynchronized bank account balance is {unsynchronized_account.money}. It should be 0. ")
    print(f"Unsynchronized logic with race condition took {time.perf_counter() - start}")

    synchronized_account = SynchronizedBankAccount()

    start = time.perf_counter()
    threads = []
    for _ in range(1000):
        t = ATM(synchronized_account)
        t.start()
        threads.append(t)

    for t in threads: 
        t.join()
    
    print(f"synchronized bank account balance is {synchronized_account.money}. It should be 0. ")
    print(f"Synchronized logic with mutex took {time.perf_counter() - start}")


    # unsynchronized bank account balance is 30. It should be 0. 
    # Unsynchronized logic with race condition took 0.8386835420000001
    # synchronized bank account balance is 0. It should be 0. 
    # Synchronized logic with mutex took 0.752394708