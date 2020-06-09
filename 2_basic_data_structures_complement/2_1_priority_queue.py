#!/usr/bin/env python3
"""
Min / max priority queue implemented in Python3 for programming competition

- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。

- max priority queue, min priority queue の両方とも頻繁に使うため用意しておく。

- task_decrease_key, task_increase_key は実装されていない。辞書などを用いて task から entry の参照を得ることはできるが、それが heap においてどのようなインデックス位置なのかを
  特定するのに (built-in heap のみを使う場合) O(n) かかってしまう。自前のヒープ内で swap 時にインデックスを保持するようなデータを用意してやると O(1) でインデックス位置が定まるため
  あとは O(lgn) で更新処理を行えるのだが... 
  -> 2_2_original_priority_queue.py

- 自作クラスのオブジェクトを突っ込みたい場合は比較演算のための __lt__, __gt__ をオーバーロードしよう。


<メソッド早見表>
is_empty():
    O(1)
    PQueue が空か判定
add_task(task, priority):
    O(lgn)
    任意の task オブジェクトを priority なる優先度の値で PQueue に追加する
pop_task():
    O(lgn)
    優先度が最小 / 最大の task オブジェクトを取り出す
"""



import itertools
from heapq import heappush, heappop

# built-in min heap を利用して実装した min priority queue
class PQueueMin:
    def __init__(self):
        """
        self.pq is a heap that is comprised of 'entry' list ([priority, count, task])
        priority (number): int or float that represents priority
        count (int)      : unique id. the later it is added, the greater the count number becomes
        task (obj)       : any object
        """
        self.pq = []    # heap
        self.counter = itertools.count()    # unique sequence id

    def is_empty(self):
        return len(self.pq) == 0

    def add_task(self, task, priority):
        """Add a new task in O(lgn). If the priorities are the same, the one that is added later is placed at close to leaf."""
        count = next(self.counter)
        entry = [priority, count, task]
        heappush(self.pq, entry)
    
    def pop_task(self):
        """Pop and return the lowest priority task in O(lgn). Raise KeyError if PQueue is empty."""
        if self.is_empty():
            raise KeyError(f"PQueueMin.pop_task(): pqueue is empty.")
        _, _, task = heappop(self.pq)
        return task



# built-in min heap を利用して実装した max priority queue (内部で正負を反転させるのみ)
class PQueueMax:
    def __init__(self):
        """
        self.pq is a heap that is comprised of 'entry' list ([priority, count, task])
        priority (number): int or float that represents priority
        count (int)      : unique id. the later it is added, the greater the count number becomes
        task (obj)       : any object
        """        
        self.pq = []    # heap
        self.counter = itertools.count()    # unique sequence id

    def is_empty(self):
        return len(self.pq) == 0
    
    def add_task(self, task, priority):
        """Add a new task in O(lgn). If the priorities are the same, the one that is added later is placed at close to leaf."""
        count = next(self.counter)
        entry = [-priority, count, task]    # counter は正負反転しない。後に追加される方が値が大きくなり min heap に挿入する上で不利になっている。
        heappush(self.pq, entry)

    def pop_task(self):
        """Pop and return the lowest priority task in O(lgn). Raise KeyError if PQueue is empty."""        
        if self.is_empty():
            raise KeyError(f"PQueueMax.pop_task(): pqueue is empty.")
        _, _, task = heappop(self.pq)
        return task




if __name__ == "__main__":
    import random
    P = PQueueMin()
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for elm in L:
        P.add_task(elm, random.randint(1, 100))
    
    assert not P.is_empty()
    tmp = list(map(lambda x: x[2], sorted(P.pq)))
    buf = []
    while not P.is_empty():
        buf.append(P.pop_task())
    assert tmp == buf


    Q = PQueueMax()
    for elm in L:
        Q.add_task(elm, random.randint(1, 100))
    
    assert not Q.is_empty()
    tmp = list(map(lambda x: x[2], sorted(Q.pq)))    # すでに priority は負になっている
    buf = []
    while not Q.is_empty():
        buf.append(Q.pop_task())
    assert tmp == buf

    print(" * assertion test ok * ")
