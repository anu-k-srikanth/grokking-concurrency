from collections import deque
import random
import typing as T

# Before async/await, coroutines were implemented using the Generator type
# Here the values are 
#   (1) yield type - what values this yields when pausing
#   (2) send type - what type of values can be sent into the function
#   (3) return type - what type of values this function returns 
Coroutine = T.Generator[None, None, int]

class EventLoop:
    def __init__(self):
        self.tasks: T.Deque[Coroutine] = deque()

    def add_coroutine(self, task: Coroutine):
        self.tasks.append(task)

    def run_coroutine(self, task: Coroutine):
        try:
            # Task is started and run until the yield statement with task.send(None)
            # Once it gets to yield, it gives up control and we execute the `self.add_coroutine(task)`
            # This adds the corouting to the event loop queue again to be checked at a later time so that we can schedule more
            # If the coroutine is already done and has returned, StopIteration exception is thrown and we do not add it to the queeu again.
            task.send(None)
            self.add_coroutine(task)
        except StopIteration as e:
            # Generators don't return normally. They yield 0 or more times and then they return the result as part of the StopIteration exception
            # We have to extract the return value from this exception.
            print(f"Task completed. {e.value}")

    def run_forever(self):
        while self.tasks: 
            print("Event loop cycle")
            task = self.tasks.popleft()
            self.run_coroutine(task)

def fibonnacci(n: int) -> Coroutine:
    i, j = 0, 1
    for num in range(n):
        print(f"Fibonacci {num}: {i}")
        i, j = j, i+j
        yield
    return i


def print_random_number(n: int) -> Coroutine:
    sum_of_rand = 0
    for num in range(n):
        rand = random.randint(1, 100)
        print(f"Random number {num}: {rand}")
        sum_of_rand += rand
        yield
    return sum_of_rand

    
if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonnacci(5))
    event_loop.add_coroutine(print_random_number(3))
    event_loop.run_forever()