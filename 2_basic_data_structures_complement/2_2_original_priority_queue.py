#!/usr/bin/env python3
"""
*Original* min / max priority queue implemented in Python3 for programming competition

- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。

- max priority queue, min priority queue の両方とも頻繁に使うため用意しておく。

- pqueue において increase_key, decrease_key などのタスクを指定してその priority を増減させるメソッド (O(lgn)) を利用するには、
  タスクからエントリーオブジェクトを O(1) で発見し、binary heap の中でのインデックスを O(1) で特定できるようにする必要がある。
  heapq の heapify を使ってしまうとインデックス情報をトラッキングできなくなるため「自作の heap 実装」を行うことにする。

- 自作クラスのオブジェクトを突っ込みたい場合は比較演算のための __lt__, __gt__ をオーバーロードしよう。


<メソッド早見表>
is_empty():
    O(1)
    PQueue が空か判定
is_registered_task():
    O(1)
    task が PQueue に登録されているか判定
peek():
    O(1)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを確認する (ヒープからは取り出さない)
add_task(task, priority):
    O(lgn)
    任意の task オブジェクトを priority なる優先度の値で PQueue に追加する
    なお、priority が同じ場合、後に挿入された方が (葉に: min-pqueue / 根に: max-pqueue) 近くなるように実装している
pop_task():
    O(lgn)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを取り出す
task_change_key(task, new_priority):
    O(lgn)
    PQueue 内の task オブジェクトの優先度を new_priority へ変更する
"""

import operator as op
import itertools

class OriginalPQueue:
    def __init__(self, max_pqueue=False):
        """
        self.pq is a heap that is comprised of 'entry' list ([priority, count, ind, task])
        priority (number): int or float that represents priority
        count (int)      : unique id. the later it is added, the greater the count number becomes
        ind (int)        : index of self.pq (heap). it is appropriately updated whenever the swap beteween elements occurrs
        task (obj)       : any object
        """
        self.max_pqueue = max_pqueue
        self.comp = op.gt if max_pqueue else op.lt    # comparing function
        self.pq = []    # heap
        self.size = 0    # heap size
        self.entry_finder = dict()    # mapping of tasks to entries
        self.counter = itertools.count()    # unique sequence id

    def is_empty(self):
        return self.size == 0
    
    def is_registered_task(self, task):
        return task in self.entry_finder
    
    def _left(self, ind):
        return (ind << 1) + 1
    
    def _right(self, ind):
        return (ind << 1) + 2
    
    def _parent(self, ind):
        return (ind - 1) >> 1
    
    def _swap_pq_element(self, i, j):
        """swap self.pq[i] and self.pq[j] in O(1). self.pq[i][2], self.pq[j][2] (index slot) is updated appropriately."""
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.pq[i][2], self.pq[j][2] = i, j

    def _heapify(self, ind):
        """
        (assume that both _left(ind) subtree and _right(ind) subtree satisfy heap condition)
        make the ind subtree satisfy heap condition in O(lgn)
        """
        l = self._left(ind)
        r = self._right(ind)
        # max-heap なら自身、左子、右子のうち最大のものを、min-heap なら最小のものを pivot にメモる
        if l < self.size and self.comp(self.pq[l], self.pq[ind]):
            pivot = l
        else:
            pivot = ind
        if r < self.size and self.comp(self.pq[r], self.pq[pivot]):
            pivot = r
        if pivot != ind:
            # ind を中心とする subtree はヒープ条件を満足していなかった
            self._swap_pq_element(ind, pivot)
            self._heapify(pivot)
    
    def _change_key(self, ind, new_priority):
        """change self.pq[ind][0] to new_priority and make it satisfies heap condition in O(lgn)"""
        old_priority = self.pq[ind][0]
        self.pq[ind][0] = new_priority
        if old_priority == new_priority:
            pass
        elif self.comp(new_priority, old_priority):
            # 上へ滑らせる
            while ind > 0 and self.comp(self.pq[ind], self.pq[self._parent(ind)]):    # 親と比較して適切な大小関係でないなら
                p = self._parent(ind)
                self._swap_pq_element(ind, p)
                ind = self._parent(ind)
        else:
            # 下へ移動していく
            self._heapify(ind)

    def _heappush(self, entry):
        priority = entry[0]
        entry[0] = - float('inf') if self.max_pqueue else float('inf')
        self.pq.append(entry)
        self.size += 1
        # この時点でヒープ条件は満たされている。ここからヒープ末尾の要素の優先度を (-inf or inf から) priority へ変更する
        self._change_key(self.size - 1, priority)

    def _heappop(self):
        self._swap_pq_element(0, self.size - 1)
        heap_root = self.pq.pop()
        self.size -= 1        
        self._heapify(0)
        return heap_root

    
    def peek(self):
        """
        Not pop but peek a task in O(1) that is currently placed at the root of the binary heap. 
        min-pqueue: minimum priority task, max-queue: maximum priority task
        """
        if self.is_empty():
            raise IndexError(f"peek(): pqueue is empty.")
        _, _, _, task = self.pq[0]
        return task


    def add_task(self, task, priority):
        """Add a new task in O(lgn). Raise KeyError if the task is in OriginalPQueue."""
        if self.is_registered_task(task):
            raise KeyError(f"OriginalPQueue.add_task(): task already exists. task:{task}")
        count = next(self.counter)
        ind = self.size
        entry = [priority, count, ind, task]
        self.entry_finder[task] = entry
        self._heappush(entry)


    def pop_task(self):
        """Pop and return the lowest (min-pqueue) / highest (max-pqueue) priority task in O(lgn). Raise KeyError if OriginalPQueue is empty."""
        if self.is_empty():
            raise KeyError(f"OriginalPQueue.pop_task(): pqueue is empty.")
        _, _, _, task = self._heappop()    # ind has already changed from 0 to size-1 in _heappop()
        return task

    
    def task_change_key(self, task, new_priority):
        """Change the priority of specific task in O(lgn)."""
        entry = self.entry_finder[task]
        i = entry[2]
        self._change_key(i, new_priority)




if __name__ == "__main__":
    import random

    print("MinPQueue test.")
    P = OriginalPQueue(max_pqueue=False)
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for elm in L:
        P.add_task(elm, random.randint(1, 100))
    
    assert not P.is_empty()
    assert P.size == len(L)
    P.task_change_key('moo', 0)
    assert P.pop_task() == 'moo'

    tmp = list(map(lambda x: x[3], sorted(P.pq)))
    buf = []
    while not P.is_empty():
        buf.append(P.pop_task())
    assert tmp == buf

    print("MaxPQueue test.")
    Q = OriginalPQueue(max_pqueue=True)
    for elm in L:
        Q.add_task(elm, random.randint(1, 100))
    
    assert not Q.is_empty()
    assert Q.size == len(L)
    Q.task_change_key('moo', 101)
    assert Q.pop_task() == 'moo'

    tmp = list(map(lambda x: x[3], sorted(Q.pq, reverse=True)))
    buf = []
    while not Q.is_empty():
        buf.append(Q.pop_task())
    assert tmp == buf

    print(" * assertion test ok * ")