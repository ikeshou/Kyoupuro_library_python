"""
一番ベーシックな min priority queue, max priority queue の実装

- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。



<メソッド早見表>
is_empty():
    O(1)
    PQueue が空か判定
add_task(task, priority):
    O(lgn)
    task を priority の優先度で PQueue に追加
pop_task():
    O(lgn)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを取り出す
"""



import itertools
from heapq import heappush, heappop
from typing import Any, Union

Num = Union[int, float]



class PQueueMin:
    """
    min priority queue
    Attributes:
        self.pq (list): (priority, count, task) というタプルのエントリからなるヒープ。
        self.counter (iter): ユニークな番号。上記エントリを比較する際、task までに必ず順序関係が決定するようにするためのもの。(task に順序関係がないことがある)
    """    
    def __init__(self):
        self.pq = []
        self.counter = itertools.count()

    def is_empty(self) -> bool:
        return len(self.pq) == 0

    def add_task(self, task: Any, priority: Num) -> None:
        count = next(self.counter)
        entry = (priority, count, task)
        heappush(self.pq, entry)
    
    def pop_task(self) -> Any:
        if self.is_empty():
            raise KeyError(f"PQueueMin.pop_task(): pqueue is empty.")
        _, _, task = heappop(self.pq)
        return task



class PQueueMax:
    """
    max priority queue
    Attributes:
        self.pq (list): (-priority, count, task) というタプルのエントリからなるヒープ。
        self.counter (iter): ユニークな番号。上記エントリを比較する際、task までに必ず順序関係が決定するようにするためのもの。(task に順序関係がないことがある)
    """
    def __init__(self):   
        self.pq = []
        self.counter = itertools.count()

    def is_empty(self) -> bool:
        return len(self.pq) == 0
    
    def add_task(self, task: Any, priority: Num) -> None:
        count = next(self.counter)
        entry = (-priority, count, task)    # counter は正負反転しない。後に追加される方が値が大きくなり min heap に挿入する上で不利になっている。
        heappush(self.pq, entry)

    def pop_task(self) -> Any:
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
