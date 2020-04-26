#!/usr/bin/env python3
"""
Min / max priority queue implemented in Python3 for programming competition

リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。
max priority queue, min priority queue の両方とも頻繁に使うため用意しておく。
自作クラスのオブジェクトを突っ込みたい場合は __lt__, __gt__ をオーバーロードしよう。


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
task_decrease / increase_key(task, new_priority):
    O(n) (うまく実装すると O(lgn) になるけど未実装。使わないようにする)
    PQueue 内の task オブジェクトの優先度を new_priority へ減らす / 増やす
"""

import itertools
from heapq import heappush, heappop


# min heap を利用して実装した min priority queue
class PQueueMin:
    def __init__(self):
        """
        self.pq は [priority, count, task] からなる entry が収納された heap。
        リストの比較は前から順に比較していくので、priority が同点だった場合 count が小さい方が木構造の上におかれることになる。
        self.entry_finder の辞書を用いて task から O(1) で self.pq 内の entry にアクセス可能。

        priority: 優先度を表す実数値
        count: ユニークな ID 。後に追加されるほど大きくなる。
        task: 任意のオブジェクト
        """
        self.pq = []    # heap
        self.entry_finder = dict()    # mapping of tasks to entries
        self.counter = itertools.count()    # unique sequence id


    def is_empty(self):
        return len(self.pq) == 0
    
    def _left(self, ind):
        return (ind//2)+1
    
    def _right(self, ind):
        return (ind//2)+2
    
    def _parent(self, ind):
        return (ind-1)//2
    

    def add_task(self, task, priority):
        """Add a new task in O(lgn). Raise KeyError if the task is in PQueue."""
        if task in self.entry_finder:
            raise KeyError(f"PQueueMin.add_task(): task already exists. task:{task}")
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
    

    def pop_task(self):
        """Pop and return the lowest priority task in O(lgn). Raise KeyError if PQueue is empty."""
        if self.is_empty():
            raise KeyError(f"PQueueMin.pop_task(): pqueue is empty.")
        _, _, task = heappop(self.pq)
        return task

    
    def task_decrease_key(self, task, new_priority):
        """Decrease the priority of specific task. Raise ValueError if new_priority is greater than the old one."""
        entry = self.entry_finder[task]
        if entry[0] < new_priority:
            raise ValueError(f"PQueueMin.task_decrease_key(): decrease only. current priority: {entry[0]}, but got {new_priority}")
        entry[0] = new_priority
        # 見つかってからは O(lgn) だが、この線形探索で O(n) かかる...
        i = self.pq.index(entry)
        while i >= 1 and self.pq[i] < self.pq[self._parent(i)]:
            self.pq[i], self.pq[self._parent(i)] = self.pq[self._parent(i)], self.pq[i]
            i = self._parent(i)


# min heap を利用して実装した max priority queue
# 内部で正負を反転させるのみ
class PQueueMax:
    def __init__(self):
        self.pq = []    # heap
        self.entry_finder = dict()    # mapping of tasks to entries
        self.counter = itertools.count()    # unique sequence id

    def is_empty(self):
        return len(self.pq) == 0
    
    def _left(self, ind):
        return (ind//2)+1
    
    def _right(self, ind):
        return (ind//2)+2
    
    def _parent(self, ind):
        return (ind-1)//2
    
    def add_task(self, task, priority):
        if task in self.entry_finder:
            raise KeyError(f"PQueueMax.add_task(): task already exists. task:{task}")
        count = next(self.counter)
        # counter は正負反転しちゃだめ。この時点で後に追加される方が値が大きくなり min heap に挿入する上で不利になっている。
        entry = [-priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def pop_task(self):
        if self.is_empty():
            raise KeyError(f"PQueueMax.pop_task(): pqueue is empty.")
        _, _, task = heappop(self.pq)
        return task
    
    def task_increase_key(self, task, new_priority):
        entry = self.entry_finder[task]
        # 負数から変換するのを忘れずに。
        if - entry[0] > new_priority:
            raise ValueError(f"PQueueMax.task_increase_key(): increase only. current priority: {- entry[0]}, but got {new_priority}")
        # 負数へ変換するのを忘れずに。
        entry[0] = - new_priority
        # 見つかってからは O(lgn) だが、この線形探索で O(n) かかる...
        i = self.pq.index(entry)
        while i >= 1 and self.pq[i] < self.pq[self._parent(i)]:
            self.pq[i], self.pq[self._parent(i)] = self.pq[self._parent(i)], self.pq[i]
            i = self._parent(i)




if __name__ == "__main__":
    import random
    P = PQueueMin()
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for elm in L:
        P.add_task(elm, random.randint(1, 100))
    
    assert not P.is_empty()
    print(P.pq)
    P.task_decrease_key('moo', 0)
    print(P.pq)
    assert P.pop_task() == 'moo'
    print("")

    tmp = sorted(P.pq)
    for elm in tmp:
        print(elm)
    print("")
    
    while not P.is_empty():
        print(P.pop_task())
