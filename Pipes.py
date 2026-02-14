from threading import Thread, current_thread
from multiprocessing import Pipe

# In this example, we use Pipe for message-based communication between multiple threads.
# This provides bidirectional communication between the two threads. 
# However, the program will hang if one of the threads calls self.conn.recv() and the other did not send anything

class Writer(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.name = "Writer"
    
    def run(self):
        for i in range(3): 
            print(f"{i} - Current writer thread name {current_thread().name}")
            print("Sending rubber duck")
            self.conn.send("Rubber duck")


class Reader(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.name = "Reader"
    
    def run(self):
        for i in range(3): 
            print(f"{i} - Current reader thread name {current_thread().name}")
            print("Receiving rubber duck")
            msg = self.conn.recv()
            print(f"Reading rubber duck: {msg}")


def main():
    writer_conn, reader_conn = Pipe()
    w = Writer(writer_conn)
    r = Reader(reader_conn)

    threads = [w, r]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

main()
