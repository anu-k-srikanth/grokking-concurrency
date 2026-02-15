class Node:
    def __init__(self, val, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.val = val
    
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
        self.insert_at_head(node)

    def remove(self, node):
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.next = None
        node.prev = None
        return node

    def remove_tail(self):
        return self.remove(self.tail.next)

    def __str__(self) -> str:
        node = self.tail
        arr = []
        while node: 
            arr.append(node.val)
            node = node.next
        return str(arr)

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        # key -> Node(val)
        self.table = {}
        self.linked_list = LinkedList()

    # O(1)
    def put(self, key, value):
        if key in self.table: 
            current = self.table[key]
            current.val = (key,value)
            self.linked_list.move_to_head(current)
            return
        if len(self.table) == self.capacity: 
            tail_node = self.linked_list.remove_tail()
            del self.table[tail_node.val[0]]
        self.table[key] = self.linked_list.insert((key,value))

    # O(1)
    def get(self, key):
        if key in self.table: 
            self.linked_list.move_to_head(self.table[key])
            return self.table[key].val[1]
        raise ValueError(f"Record with key {key} not in cache")

    # O(1)
    def delete(self, key):
        if key in self.table: 
            self.linked_list.remove(self.table[key])
            del self.table[key]
            return 
        raise ValueError(f"Record with key {key} not in cache")

    def __str__(self) -> str:
        return str(self.table) + "||" + str(self.linked_list)


if __name__ == "__main__":
    cache = LRUCache(3)
    cache.put("anu", 1)
    print(cache)
    cache.put("jake", 2)
    print(cache)
    cache.put("pippin", 3)
    print(cache)
    cache.get("anu")
    print(cache)
    cache.delete("anu")
    print(cache)
    cache.put("upili", 4)
    print(cache)
    cache.put("madhu", 5)
    print(cache)