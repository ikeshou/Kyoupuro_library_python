"""
エントリの削除が可能な min / max priority queue


- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。
  min / max priority queue をクラス初期化時の引数で指定できるような実装


<algorithm>
pqueue を二本持つことにより削除クエリに対し処理を遅延して捌くことができる


<メソッド早見表>
is_empty():
    O(1)
    PQueue が空か判定
add_task(task, priority):
    O(lgn)
    task を priority の優先度で PQueue に追加
peek():
    O(1)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを確認する (ヒープからは取り出さない)
pop_task():
    O(lgn)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを取り出す
remove_task(task):
    O(lgn)
    task を PQueue から削除



verified @ABC170D
"""


import itertools
from heapq import heappush, heappop
from typing import Any, Union

Num = Union[int, float]



class RemovablePQueue:
    """
    removable min / max priority queue
    Attributes:
        self.pq (list): (priority, ind, task) というタプルで表されるエントリからなるヒープ。
        self.op (function): 内部で実際にもつ priority に変換する関数。max_pqueue の場合は -1 をかける。
        self.counter (iter): ユニークな番号。上記エントリを比較する際、task までに必ず順序関係が決定するようにするためのもの。(task に順序関係がないことがある)
        self.entry_finder (dict): task からエントリをひくための辞書
        self.pq_remove_buf (list): [priority, ind, task] というリストのエントリからなるヒープ。削除要請のあったものが一時的に保存される。
    """    
    def __init__(self, max_pqueue: bool=False):
        self.pq = []
        self.op = (lambda x: -x) if max_pqueue else (lambda x: x)
        self.counter = itertools.count()
        self.entry_finder = dict()
        self.pq_remove_buf = []


    def is_empty(self) -> bool:
        return len(self.pq) - len(self.pq_remove_buf) == 0  

    def add_task(self, task: Any, priority: Num) -> None:
        """O(lgn) でタスクを追加する"""
        count = next(self.counter)
        entry = (self.op(priority), count, task)
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def peek(self) -> Any:
        """O(lgn) でヒープトップのエントリを盗み見て、そのタスクを返す"""
        if self.is_empty():
            raise KeyError(f"RemovablePQueue.peek(): pqueue is empty.")
        while self.pq_remove_buf and self.pq[0] == self.pq_remove_buf[0]:
            # すでに削除要請が来ていたエントリー
            heappop(self.pq)
            heappop(self.pq_remove_buf)
        # 削除要請が来ていないヒープトップのエントリー            
        _, _, task = self.pq[0]
        return task
    
    def pop_task(self) -> Any:
        """O(lgn) でヒープトップのエントリをポップし、そのタスクを返す"""
        if self.is_empty():
            raise KeyError(f"RemovablePQueue.pop_task(): pqueue is empty.")
        while self.pq_remove_buf and self.pq[0] == self.pq_remove_buf[0]:
            # すでに削除要請が来ていたエントリー
            heappop(self.pq)
            heappop(self.pq_remove_buf)
        # 削除要請が来ていないヒープトップのエントリー
        _, _, task = heappop(self.pq)
        return task
    
    def remove_task(self, task: Any) -> None:
        """O(lgn) でタスクを削除する"""
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
