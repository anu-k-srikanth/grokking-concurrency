from collections import defaultdict
from multiprocessing import Lock, Pool
from multiprocessing.pool import ThreadPool
import re
from threading import Thread


def parse_words(text):
    words = []
    text_lines = text.split("\n")
    for line in text_lines: 
        words.extend(re.split(r"\W+", line))
    return words 

def count_words(words):
    word_count = defaultdict(int)
    for word in words: 
        word_count[word] += 1
    return word_count

def combine_counts(counts: list[dict]):
    total_count = defaultdict(int)
    for d in counts:
        for word,count in d.items():
            total_count[word] += count
    return total_count

def count_words_concurrent(words):
    NUM_CORES = 8
    pool = Pool(processes=NUM_CORES)
    chunk_size = len(words) // NUM_CORES 

    counts = pool.map(count_words, 
                      (words[i:min(i+chunk_size, len(words))] for i in range(0, len(words), chunk_size)))
    
    return combine_counts(counts)


def count_words_threads(text):
    words_per_line = []
    text_lines = text.split("\n")
    for line in text_lines: 
        words_per_line.append(re.split(r"\W+", line))

    shared_word_count = defaultdict(int)
    lock = Lock()

    def add_word_count(word):
        with lock:
            shared_word_count[word] += 1
    
    def count_words(word_arr):
        for word in word_arr: 
            add_word_count(word)
        return word_count

    threads = []
    for wil in words_per_line:
        t = Thread(target=count_words, args=(wil, ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    return shared_word_count


if __name__ == "__main__":
    text = '''99 little bugs in the code
    take one down, patch it around
    127 little bugs in the code'''

    words = parse_words(text)

    word_count = count_words(words)

    concurrent_word_count = count_words_concurrent(words)

    concurrent_word_count_with_threads = count_words_threads(text)

    print(f"word count: {word_count}")
    print(f"concurrent_word_count: {concurrent_word_count}")
    print(f"concurrent_word_count_with_threads: {concurrent_word_count_with_threads}")

