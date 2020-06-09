#!/usr/bin/env python3
"""
Min / max priority queue implemented in Python3 for programming competition

- 削除もできるやつ
"""


import itertools
from heapq import heappush, heappop

# built-in min heap を利用して実装した min priority queue
class RemovablePQueue:
    def __init__(self, max_pqueue=False):
        """
        self.pq is a heap that is comprised of 'entry' list ([priority, count, task])
        priority (number): int or float that represents priority
        count (int)      : unique id. the later it is added, the greater the count number becomes
        task (obj)       : any object
        """
        self.op = (lambda x: -x) if max_pqueue else (lambda x: x)
        self.pq = []    # heap
        self.entry_finder = dict()
        self.pq_remove_buf = []    # heap that memorizing the contents that should be removed
        self.counter = itertools.count()    # unique sequence id

    def is_empty(self):
        return len(self.pq) - len(self.pq_remove_buf) == 0

    def add_task(self, task, priority):
        """Add a new task in O(lgn). If the priorities are the same, the one that is added later is placed at close to leaf."""
        count = next(self.counter)
        entry = [self.op(priority), count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
    
    def pop_task(self):
        """Pop and return the task that is placed at the top of heap in O(lgn). Raise KeyError if PQueue is empty."""
        if self.is_empty():
            raise KeyError(f"RemovablePQueue.pop_task(): pqueue is empty.")
        while self.pq_remove_buf and self.pq[0] == self.pq_remove_buf[0]:
            # すでに削除要請が来ていたエントリー
            heappop(self.pq)
            heappop(self.pq_remove_buf)
        # 削除要請が来ていないヒープトップのエントリー
        _, _, task = heappop(self.pq)
        return task
    
    def remove_task(self, task):
        """Remove a task in O(1). Raise ValueError if the task does not exist in self.pq."""
        if task not in self.entry_finder:
            raise ValueError(f"RemovablePQueue.remove_task(): the task does not exist. got {task}")
        entry = self.entry_finder[task]
        heappush(self.pq_remove_buf, entry)    # とりあえずこっちに突っ込んでおく
        del self.entry_finder[task]





if __name__ == "__main__":
    print("MinPQueue test.")
    P = RemovablePQueue(max_pqueue=False)
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for i in range(len(L)):
        P.add_task(L[i], len(L)-i)
    
    assert not P.is_empty()
    P.remove_task('moo')
    P.remove_task('bow')
    P.remove_task('wow')
    P.remove_task('cow')
    P.remove_task('baaaa')
    try:
        P.remove_task('moo')
    except ValueError:
        pass
    try:
        P.remove_task('non-existent-key')
    except ValueError:
        pass
    buf = []
    while not P.is_empty():
        buf.append(P.pop_task())
    assert buf == ['roar', 'cheep', 'caw', 'oink', 'tweet', 'meow']

    print("MaxPQueue test.")
    Q = RemovablePQueue(max_pqueue=True)
    for i in range(len(L)):
        Q.add_task(L[i], i)
    
    assert not Q.is_empty()
    Q.remove_task('moo')
    Q.remove_task('bow')
    Q.remove_task('wow')
    Q.remove_task('cow')
    Q.remove_task('baaaa')
    try:
        Q.remove_task('moo')
    except ValueError:
        pass
    try:
        Q.remove_task('non-existent-key')
    except ValueError:
        pass
    buf = []
    while not Q.is_empty():
        buf.append(Q.pop_task())
    assert buf == ['roar', 'cheep', 'caw', 'oink', 'tweet', 'meow']

    print(" * assertion test ok * ")
