"""
(参考) <Algorithm Introduction vol.1 p.124-139>
優先度の変更が可能な min / max priority queue

- リスト上で min heap を構築するためのモジュール heapq は存在するが priority queue はサポートされていないので自前で用意する必要がある。
  min / max priority queue をクラス初期化時の引数で指定できるような実装


<algorithm>
pqueue において O(lgn) であるタスクの priority を増減させるには
タスクからエントリーオブジェクトを O(lgn) で発見し、binary heap 配列の中でのインデックスを O(lgn) で特定できるようにする必要がある。
エントリ自身が binary heap 内での配列インデックスを記憶するような自作の heap 実装により、上記をそれぞれ O(1) で行えるようになる。
（heapq を使用するとインデックスの特定に O(n) かかる）



<メソッド早見表>
is_empty():
    O(1)
    PQueue が空か判定
peek():
    O(1)
    優先度が (最小: min-pqueue / 最大: max-pqueue) の task オブジェクトを確認する (ヒープからは取り出さない)
add_task(task, priority):
    O(lgn)
    task を priority の優先度で PQueue に追加
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
from typing import Any, List, Union

Num = Union[int, float]



class OriginalPQueue:
    """
    優先度を変更可能な min / max priority queue
    Attributes:
        self.max_pqueue (bool): max_pqueue かどうか。デフォルトは False
        self.comp (function): 比較関数。min pqueue なら <, max pqueue なら >
        self.pq (list): [priority, ind, task] というリストのエントリからなるヒープ。ind がユニークであるため task までにエントリの順序関係が決定することに留意。
        self.size (int): ヒープサイズ
        self.entry_finder (dict): task からエントリを発見するための辞書
    """
    def __init__(self, max_pqueue: bool=False):
        self.max_pqueue = max_pqueue
        self.comp = op.gt if max_pqueue else op.lt
        self.pq = []
        self.size = 0
        self.entry_finder = dict()

    def is_empty(self) -> bool:
        return self.size == 0
    
    def _left(self, ind: int) -> int:
        return (ind << 1) + 1
    
    def _right(self, ind: int) -> int:
        return (ind << 1) + 2
    
    def _parent(self, ind: int) -> int:
        return (ind - 1) >> 1
    
    def _swap_pq_element(self, i: int, j: int) -> None:
        """O(1) で pq の [i], [j] 要素を交換する。各エントリのヒープ内インデックスのスロットは適切に更新される。"""
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.pq[i][1], self.pq[j][1] = i, j

    def _heapify(self, ind: int) -> None:
        """
        （[ind] の左右の子を根とする部分木はヒープ条件を満たしているとする）
        O(lgn) で ind を根とする部分木がヒープ条件を満たすように変更する
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
    
    def _change_key(self, ind: int, new_priority: Num) -> None:
        """O(lgn) で [ind] の優先度を new_priority に変更し、ヒープ条件を回復させる"""
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

    def _heappush(self, task: Any, priority: Num) -> None:
        """O(lgn) で task, priority からエントリを作成しヒープに追加する"""
        tmp_priority = -float('inf') if self.max_pqueue else float('inf')    # 末尾にふさわしい priority に
        entry = [tmp_priority, self.size, task]
        self.entry_finder[task] = entry
        self.pq.append(entry)
        self.size += 1
        # この時点でヒープ条件は満たされている。ここからヒープ末尾の要素の優先度を (-inf or inf から) priority へ変更する
        self._change_key(self.size - 1, priority)

    def _heappop(self) -> List[List[Union[int, Any]]]:
        """O(lgn) でヒープトップのエントリをポップして返す"""
        self._swap_pq_element(0, self.size - 1)
        heap_root = self.pq.pop()
        self.size -= 1        
        self._heapify(0)
        return heap_root

    
    def peek(self) -> Any:
        """O(1) でヒープトップのエントリを盗み見て、そのタスクを返す"""
        if self.is_empty():
            raise IndexError(f"peek(): pqueue is empty.")
        _, _, task = self.pq[0]
        return task


    def add_task(self, task: Any, priority: Num) -> None:
        """O(lgn) で priority なる優先度で task をヒープに追加する"""
        if task in self.entry_finder:
            raise KeyError(f"OriginalPQueue.add_task(): task already exists. task:{task}")
        self._heappush(task, priority)


    def pop_task(self) -> Any:
        """O(lgn) でヒープトップのエントリをポップし、そのタスクを返す"""
        if self.is_empty():
            raise KeyError(f"OriginalPQueue.pop_task(): pqueue is empty.")
        _, _, task = self._heappop()
        return task

    
    def task_change_key(self, task: Any, new_priority: Num) -> None:
        """O(lgn) で task の優先度を new_priority へ変更する"""
        entry = self.entry_finder[task]
        i = entry[1]
        self._change_key(i, new_priority)




if __name__ == "__main__":
    import random

    print("MinPQueue test.")
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    pr = list(range(1, len(L) + 1))
    
    for _ in range(100):
        random.shuffle(pr)

        P = OriginalPQueue(max_pqueue=False)

        for i in range(len(L)):
            P.add_task(L[i], pr[i])
        
        assert not P.is_empty()
        assert P.size == len(L)
        P.task_change_key('moo', 0)
        assert P.pop_task() == 'moo'

        tmp = list(map(lambda x: x[2], sorted(P.pq)))
        buf = []
        while not P.is_empty():
            buf.append(P.pop_task())
        assert tmp == buf


    print("MaxPQueue test.")

    for _ in range(100):
        Q = OriginalPQueue(max_pqueue=True)

        for i in range(len(L)):
            Q.add_task(L[i], pr[i])
        
        assert not Q.is_empty()
        assert Q.size == len(L)
        Q.task_change_key('moo', 1000)
        assert Q.pop_task() == 'moo'

        tmp = list(map(lambda x: x[2], sorted(Q.pq, reverse=True)))
        buf = []
        while not Q.is_empty():
            buf.append(Q.pop_task())
        assert tmp == buf

    print(" * assertion test ok * ")