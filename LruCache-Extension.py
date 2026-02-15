from contextlib import contextmanager
import heapq
import sys
from threading import Condition, Lock, Thread
import threading
import time
import traceback


class Node:
    def __init__(self, val, next=None, prev=None, ttl=None):
        self.next = next
        self.prev = prev
        self.val = val
        self.ttl = ttl
    
    def __str__(self) -> str:  
        return self.val

class LinkedList:
    def __init__(self):
        self.head = Node(val="head")
        self.tail = Node(val="tail")
        self.head.prev = self.tail
        self.tail.next = self.head

    def insert(self, val) -> Node:
        new_node = Node(val)
        self.insert_at_head(new_node)
        return new_node
    
    def insert_at_head(self, node):
        prev_node = self.head.prev
        prev_node.next = node
        self.head.prev = node
        node.prev = prev_node
        node.next = self.head
        return node

    def move_to_head(self, node):
        self.remove(node)
        print(self.__str__())
        self.insert_at_head(node)
        print(self.__str__())

    def remove(self, node) -> Node:
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.next = None
        node.prev = None
        return node

    def remove_tail(self) -> Node:
        if self.tail.next == self.head:
            raise ValueError("No more items to remove")
        return self.remove(self.tail.next)

    def __str__(self) -> str:
        node = self.tail
        arr = []
        while node: 
            arr.append(node.val)
            node = node.next
        return str(arr)

class LRUCache:
    def __init__(self, capacity, max_bytes):
        self.capacity = capacity
        self.max_bytes = max_bytes
        self.current_bytes = 0
        self.table = {}
        self.linked_list = LinkedList()

        self.heap = []
        self.lock = Lock()
        self.expiry_check_condition = Condition(self.lock)

        self._start_cleaner()

    def _start_cleaner(self):
        t = Thread(target=self.clean_expired_items)
        t.start()
    
    def clean_expired_items(self):
        print("Starting cleaner...")
        while True: 
            print(self.linked_list)
            with self.expiry_check_condition:
                while len(self.heap) == 0:
                    # If heap is empty, wait to be notified of a new item added
                    self.expiry_check_condition.wait()

                counter = 0 
                time_now = time.time()
                while len(self.heap) > 0 and self.heap[0][0] < time_now:
                    expiry, key = heapq.heappop(self.heap)
                    if key in self.table: 
                        node = self.table[key]
                        if node.ttl == expiry:
                            self._internal_delete(key)
                            counter += 1
                print(f"Cleaned {counter} expired items")
                print(self.linked_list)

                if len(self.heap) > 0: 
                    next_expiry = max(0, self.heap[0][0] - time.time())
                    self.expiry_check_condition.wait(timeout=next_expiry)

    # O(1)
    def put(self, key, value, ttl=None):
        with self.lock:
            size = sys.getsizeof(value)
            if size > self.max_bytes:
                raise ValueError(f'''This object has size {size} is too large to be stored in this cache. 
                                Object size should be under {self.max_bytes}''')
        
            while self.current_bytes + size > self.max_bytes:
                node = self.linked_list.remove_tail()
                node_size = sys.getsizeof(node.val)
                self.current_bytes -= node_size
                del self.table[node.val[0]]

            if key in self.table: 
                current: Node = self.table[key]
                self.current_bytes -= sys.getsizeof(current.val)
                current.val = (key,value)
                if ttl: 
                    print(f"Adding to expiry heap and notifying cleaner thread")
                    current.ttl = ttl
                    heapq.heappush(self.heap, (ttl, key))
                    self.expiry_check_condition.notify()
                self.linked_list.move_to_head(current)
                self.current_bytes += sys.getsizeof((key,value))
                return
            if len(self.table) == self.capacity: 
                tail_node = self.linked_list.remove_tail()
                del self.table[tail_node.val[0]]
                self.current_bytes -= sys.getsizeof((tail_node.val[0],tail_node.val[1]))

            self.current_bytes += sys.getsizeof((key,value))
            self.table[key] = self.linked_list.insert((key,value))
            if ttl: 
                print(f"Adding to expiry heap and notifying cleaner thread")
                self.table[key].ttl = ttl
                heapq.heappush(self.heap, (ttl, key))
                self.expiry_check_condition.notify()

    # O(1)
    def get(self, key):
        with self.lock:
            if key in self.table: 
                self.linked_list.move_to_head(self.table[key])
                return self.table[key].val[1]
            raise ValueError(f"Record with key {key} not in cache")


    def _internal_delete(self, key):
        if key in self.table: 
            node = self.linked_list.remove(self.table[key])
            del self.table[key]
            self.current_bytes -= sys.getsizeof((node.val[0],node.val[1]))
            return node
        raise ValueError(f"Record with key {key} not in cache")
    
    # O(1)
    def delete(self, key):
        with self.lock:
            self._internal_delete(key)

    def __str__(self) -> str:
        return str(self.table) + "||" + str(self.linked_list)


def dump_threads():
    for thread in threading.enumerate():
        print(f"Thread {thread.name} (daemon={thread.daemon})")
        stack = sys._current_frames()[thread.ident]
        traceback.print_stack(stack)
        print("-" * 50)

if __name__ == "__main__":
    # time_plus_5 = time.time() + 5
    cache = LRUCache(3, 100)

    time.sleep(2)
    cache.put("anu", 1)
    print(cache)
    # dump_threads()
    cache.put("srikanth", 2)
    print(cache)
    # dump_threads()
    cache.put("kokila", 3)
    print(cache)
    # dump_threads()
    # cache.get("anu")
    # print(cache)
    # cache.delete("anu")
    # print(cache)
    cache.put("upili", 4, time.time())
    print(cache)
    cache.put("madhu", 5)
    print(cache)





