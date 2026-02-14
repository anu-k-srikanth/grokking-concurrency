import socket
import os 
from threading import Thread, current_thread
import time

SOCK_FILE = "./mailbox"
BUFFER_SIZE = 1028

class Sender(Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        self.name = "Sender"
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCK_FILE)

        messages = ["Hello", " ", "World"]
        for msg in messages: 
            print(f"{current_thread().name}: Send message {msg}")
            client.sendall(str.encode(msg))
        
        client.close() 
    

class Receiver(Thread):
    def run(self):
        self.name = "Receiver"

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(SOCK_FILE)
        server.listen()

        print(f"{current_thread().name}: Listening for incoming messages")
        conn, addr = server.accept()

        while True: 
            msg = conn.recv(BUFFER_SIZE)
            if not msg: 
                break 
            message = msg.decode()
            print(f"{current_thread().name}: {message} received by server from {addr}")
        
        server.close()

def main():
    if os.path.exists(SOCK_FILE):
        os.remove(SOCK_FILE)
    
    receiver = Receiver() 
    receiver.start() 

    time.sleep(1)

    sender = Sender()
    sender.start()

    for t in [receiver, sender]:
        t.join()

main()




