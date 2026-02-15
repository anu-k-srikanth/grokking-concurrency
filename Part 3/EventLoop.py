from __future__ import annotations
from collections import deque
import time
import typing as T

class Event:
    def __init__(self, name: str, action: T.Callable[..., None], next_event: T.Optional[Event] = None):
        self.name = name
        self._action = action 
        self._next_event = next_event
    
    def execute_action(self) -> None:
        self._action(self)
        if self._next_event:
            event_loop.register_event(self._next_event)

class EventLoop:
    def __init__(self):
        self.queue = deque()

    def register_event(self, event: Event):
        self.queue.append(event)

    def run_forever(self):
        while True:
            if len(self.queue) > 0: 
                event = self.queue.popleft()
                event.execute_action()


def knock(event: Event):
    print("Someone knocked")
    print(event.name)
    time.sleep(1)

def who(event: Event):
    print("Someone heard")
    print(event.name)
    time.sleep(1)

if __name__ == "__main__":
    event_loop = EventLoop()

    reply_event = Event("Who's there?", who)
    knock_event = Event("Knock Knock!", knock, reply_event)
    
    for _ in range(5):
        event_loop.register_event(knock_event)

    event_loop.run_forever()

