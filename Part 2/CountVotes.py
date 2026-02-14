
from collections import defaultdict
from multiprocessing.pool import ThreadPool
import random
import time
from typing import List, Tuple

def count_votes_split(votes, num_threads):
    chunk_size = len(votes) // num_threads
    ranges = []
    for start in range(0, len(votes), chunk_size):
        ranges.append((start, min(start+chunk_size, len(votes))))

    with ThreadPool() as pool:
        results = pool.starmap(count_votes, ((votes, start, end) for start, end in ranges))
        summary = merge_results(results)
    
    return summary

def merge_results(results: List[dict[int, int]]):
    overall_summary = defaultdict(int)
    for result in results: 
        for candidate, count in result.items():
            overall_summary[candidate] += count
    return overall_summary

def count_votes(votes: List[int], start, end):
    summary = defaultdict(int)
    for vote in votes[start:end]: 
        summary[vote] += 1
        time.sleep(0.01)
    return summary

def get_winning_candidate(summary: dict):
    highest_votes, winning_candidate = -1, None
    for candidate, vote_count in summary.items():
        if vote_count > highest_votes:
            highest_votes = vote_count
            winning_candidate = candidate
    return winning_candidate, highest_votes

if __name__ == "__main__":
    num_candidates = 4
    votes = []
    for _ in range(10000):
        votes.append(random.randrange(1, num_candidates+1))
    
    start = time.perf_counter()
    summary = count_votes(votes, 0, len(votes))
    winning_candidate, highest_votes = get_winning_candidate(summary)
    end = time.perf_counter()


    print(f"The winning candidate is {winning_candidate} with {highest_votes} votes")
    print(f"Serial operation took {end-start} seconds")

    start = time.perf_counter()
    thread_summary = count_votes_split(votes, num_threads=5)
    winning_candidate_threading, highest_votes_threading = get_winning_candidate(thread_summary)
    end = time.perf_counter()

    print(f"The winning candidate is {winning_candidate_threading} with {highest_votes_threading} votes")
    print(f"Parallel operation took {end-start} seconds")

    # The winning candidate is 4 with 2569 votes
    # Serial operation took 121.252013375 seconds
    # The winning candidate is 4 with 2569 votes
    # Parallel operation took 24.49838324999999 seconds