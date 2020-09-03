"""
一番ベーシックな min priority queue, max priority queue の実装

- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。



<メソッド早見表>
empty():
    O(1)
    PQueue が空か判定
add_task(task, priority):
    O(lgn)
    task を priority の優先度で PQueue に追加
pop_task():
    O(lgn)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを取り出し、(task, priority) を返す
"""



import itertools
from heapq import heappush, heappop
from heapq import _heappop_max, _siftdown_max
def _heappush_max(h, item): h.append(item); _siftdown_max(h, 0, len(h)-1)
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

    def empty(self) -> bool:
        return len(self.pq) == 0

    def add_task(self, task: Any, priority: Num) -> None:
        count = next(self.counter)
        entry = (priority, count, task)
        heappush(self.pq, entry)
    
    def pop_task(self) -> Any:
        if self.empty():
            raise KeyError(f"PQueueMin.pop_task(): pqueue is empty.")
        priority, _, task = heappop(self.pq)
        return (task, priority)



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

    def empty(self) -> bool:
        return len(self.pq) == 0
    
    def add_task(self, task: Any, priority: Num) -> None:
        count = next(self.counter)
        entry = (priority, count, task)
        _heappush_max(self.pq, entry)

    def pop_task(self) -> Any:
        if self.empty():
            raise KeyError(f"PQueueMax.pop_task(): pqueue is empty.")
        priority, _, task = _heappop_max(self.pq)
        return (task, priority)


