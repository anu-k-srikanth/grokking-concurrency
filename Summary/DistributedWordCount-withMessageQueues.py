from collections import defaultdict, deque
from queue import Queue
import re
from threading import Thread, Lock

SENTINEL = None

class Count_Dictionary:
    def __init__(self):
        self.dict = defaultdict(int)
        self._lock = Lock()

    def increment_count(self, word, count):
        with self._lock:
            self.dict[word] += count

class WordCounter:
    def __init__(self):
        self.map_queue = Queue()
        self.reduce_queue = Queue()
        self.total_count = Count_Dictionary()
        
        self.MAX_MAP_THREADS = 5
        self.MAX_REDUCE_THREADS = 3

    def _parse_words(self, text):
        words = []
        text_lines = text.split("\n")
        for line in text_lines: 
            words.extend(w for w in re.split(r"\W+", line) if w)
        return words 

    def count_words(self, text):
        words = self._parse_words(text)
        chunk_size = max(1, len(words) // self.MAX_MAP_THREADS)

        for i in range(0, len(words), chunk_size):
            word_chunk = words[i:min(i+chunk_size, len(words))]
            self.map_queue.put(word_chunk)

        map_threads = []
        for i in range(self.MAX_MAP_THREADS):
            t = MapWorker(self.map_queue, self.reduce_queue)
            t.start()
            map_threads.append(t)
    
        reduce_threads = []
        for i in range(self.MAX_REDUCE_THREADS):
            t = ReduceWorker(self.reduce_queue, self.total_count)
            t.start()
            reduce_threads.append(t)

        for t in map_threads:
            self.map_queue.put(SENTINEL)
        self.map_queue.join()

        for r in reduce_threads:
            self.reduce_queue.put(SENTINEL)
        self.reduce_queue.join()

        return self.total_count.dict
        
class MapWorker(Thread):
    def __init__(self, map_queue: Queue, reduce_queue: Queue):
        super().__init__()
        self.map_queue = map_queue
        self.reduce_queue = reduce_queue

    def run(self):
        while True: 
            words = self.map_queue.get()
            if words is SENTINEL: 
                self.map_queue.task_done()
                break

            word_count = defaultdict(int)
            for word in words: 
                word_count[word] += 1
                
            self.reduce_queue.put(word_count)
            self.map_queue.task_done()
                

class ReduceWorker(Thread):
    def __init__(self, reduce_queue: Queue, count_dict: Count_Dictionary):
        super().__init__()
        self.reduce_queue = reduce_queue
        self.count_dict = count_dict

    def run(self):
        while True: 
            word_counts = self.reduce_queue.get()
            if word_counts is SENTINEL: 
                self.reduce_queue.task_done()
                break

            for word,count in word_counts.items():
                self.count_dict.increment_count(word, count)
            self.reduce_queue.task_done()


if __name__ == "__main__":
    text = '''99 little bugs in the code
    take one down, patch it around
    127 little bugs in the code'''

    wc = WordCounter()
    print(wc.count_words(text))






