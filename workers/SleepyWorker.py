
import threading 
import time

# Extends the thread class
class SleepyWorker(threading.Thread):
    def __init__(self, seconds, **kwargs):
        self.seconds = seconds
        super(SleepyWorker, self).__init__()
        self.start()

    def _sleep_for_a_while(self):
        time.sleep(self.seconds)

        print(f"Slept for {self.seconds} seconds")
    
    def run(self):
        self._sleep_for_a_while()

