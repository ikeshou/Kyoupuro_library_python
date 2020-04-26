#!/usr/bin/env python3
"""
Circular doubly linked list implemented in Python3 for programming competition

連結リストは組み込みで用意されていないので自前で用意する必要がある。
先頭のセルのポインタを head ポインタとして持つ実装。rotate, reverse_rotate は楽だが、要素の追加削除の際に要素数のチェックと分岐が必要で大変。


<メソッド早見表>
巡回、出力系
    __str__(), __len__(), __iter()__
基本的な定数時間操作
    is_empty(), front(), back(), rotate(), reverse_rotate()
基本的な探索
    nth(), find(), count()
挿入
    push_back(), push_front(), pop_back(), pop_front(), insert_previous(), insert_next(), 
    insert_previous_by_index()
削除
    delete()
"""

class Cell:
    def __init__(self, data, prev_cell=None, next_cell=None):
        """第一引数としてデータを渡す。第二、第三引数ではリンクさせたい Cell オブジェクトを渡す。"""
        self.data = data
        self.previous = prev_cell
        self.next = next_cell
        
        

class LinkedList:
    def __init__(self, *args):
        self.head = None
        self.size = 0
        for x in args:
            self.push_back(x)


    def is_empty(self):
        return self.head is None
    
    def front(self):
        """あくまでも Cell が返ることに注意。空の場合は None が返る。"""
        return self.head

    def back(self):
        """あくまでも Cell が返ることに注意。空の場合は None が返る。"""
        return self.head.previous if self.head else None
        
    def rotate(self):
        if self.head:
            self.head = self.head.next
    
    def reverse_rotate(self):
        if self.head:
            self.head = self.head.previous
            
    def __str__(self):
        return '[' + ",".join([str(x.data) for x in self]) + ']'
    
    def __len__(self):
        return self.size


    def __iter__(self):
        """
        イテレータは特殊メソッド __iter__(self), __next__(self) をクラス内で定義することで作成可能。
        イテレータを使用する構文 (forなど) では内部で iter()、次いで next() が呼び出されているのでそれを再定義してしまう。
        next() は self.index を取得し、その Cell を返す。そして self.index を次のインスタンスに更新。
        あくまでも data ではなく Cell が返ることに注意。
        """
        self.index = self.head
        # 適切に next で StopIteration するためのフラグ。本当なら self.head に回ってきているかで周回判定を行いたいが、初回は見逃したい
        # このフラグは 本当の第一回目の iteration で self.head を指しているのではないことを示す
        self.uroboros = False
        return self

    def __next__(self):
        # 空のとき or 要素数 1 以上で head を現在指しており uroboros フラグがすでに立っているとき
        if self.index is None or (self.uroboros and self.index == self.head):
            raise StopIteration
        tmp = self.index
        self.index = self.index.next
        self.uroboros = True    # 1 回でも iteration したら uroboros フラグを立ててあげる
        return tmp


    def _push_common_procedure(self, x):
        """
        循環リストであることにより push_front, push_back は本質的に同じ操作が大半なはずである。(どちらも head, tail の間に挿入しようとしている)
        その共通処理を担う内部関数。なお push_front では要素数 1 以上の場合についてもヘッダセルの付け替えが必要になる。呼び出しもとで行う必要があることに注意。
        """
        self.size += 1
        # 要素数 0 の時
        if self.is_empty():
            pushed = Cell(x)
            pushed.previous = pushed
            pushed.next = pushed
            self.head = pushed
        # すでに要素が存在する時
        else:
            # 挿入セルの設定
            pushed = Cell(x, prev_cell=self.head.previous, next_cell=self.head)
            # 挿入セルの前のセルの調整。こちらを次の処理より先にやらないと (正しく辿るためには) 無駄に複雑になるので注意
            self.head.previous.next = pushed
            # 挿入セルの次のセルの調整
            self.head.previous = pushed
        return pushed


    def push_front(self, x):
        """
        O(1) で先頭に x というデータを持つセルを追加する。
        """
        # _push_common_procedure で size を増やしているのでここで増やしてはならない
        pushed_cell = self._push_common_procedure(x)
        # 現在の head ポインタを挿入セルに向ける
        self.head = pushed_cell
    

    def push_back(self, x):
        """O(1) で末尾に x というデータを持つセルを追加する。"""
        # _push_common_procedure で size を増やしているのでここで増やしてはならない
        self._push_common_procedure(x)
        # 現在の head ポインタは変わらぬ

    
    def pop_front(self):
        """O(1) で先頭からデータを pop する。"""
        # 要素数 0 の時
        if self.is_empty():
            raise IndexError("LinkedList.pop_front(): popped from empty LinkedList")
        popped = self.head
        self.size -= 1        
        # 要素数 1 の時
        if self.head == self.head.next:
            self.head = None
        # 要素数 2 以上の時
        else:
            # 削除セルの次のセルの調整
            self.head.next.previous = self.head.previous
            # 削除セルの前のセルの調整
            self.head.previous.next = self.head.next
            # 現在の head ポインタを削除セルの次のセルに向ける
            self.head = self.head.next
        return popped

    
    def pop_back(self):
        """O(1) で末尾からデータを pop する。"""
        # 要素数 0 の時
        if self.is_empty():
            raise IndexError("LinkedList.pop_back(): popped from empty LinkedList")
        popped = self.head.previous
        self.size -= 1        
        # 要素数 1 の時
        if self.head == self.head.next:
            self.head = None
        # 要素数 2 以上の時
        else:
            # 削除セルの前のセルの調整。こちらを次の処理より先にやらないと (正しく辿るためには) 無駄に複雑になるので注意
            self.head.previous.previous.next = self.head
            # 削除セルの次のセルの調整
            self.head.previous = self.head.previous.previous
            # 現在の head ポインタは変わらぬ
        return popped               
            
    
    def insert_previous(self, target_cell, x):
        """
        O(1) でtarget_cell の前に x をデータとしてもつようなセルを挿入する。
        なお、target_cell は必ず Linked List 内に存在するものとする。
        """
        assert target_cell is not None
        inserted = Cell(x, prev_cell=target_cell.previous, next_cell=target_cell)
        self.size += 1
        # 挿入セルの前のセルの調整
        target_cell.previous.next = inserted
        # 挿入セルの次のセルの調整
        target_cell.previous = inserted
        # head ポインタを変える必要があることもある
        if target_cell == self.head:
            self.head = inserted
        return inserted
    

    def insert_next(self, target_cell, x):
        """
        O(1) でtarget_cell の後ろに x をデータとしてもつようなセルを挿入する。
        なお、target_cell は必ず Linked List 内に存在するものとする。
        """        
        assert target_cell is not None
        inserted = Cell(x, prev_cell=target_cell, next_cell=target_cell.next)
        self.size += 1
        # 挿入セルの次のセルの調整
        target_cell.next.previous = inserted
        # 挿入セルの前のセルの調整
        target_cell.next = inserted
        # head ポインタを変える必要はない
        return inserted


    def nth(self, ind):
        """O(ind) で (0-index 表記で書くところの) [ind] 番目のセルのインスタンスを求めて返す。"""
        current_cell = self.head
        if not 0 <= ind+1 <= self.size:
            raise IndexError(f"LinkedList.nth(): invalid index. got {ind} (size={self.size})")
        for _ in range(ind):
            current_cell = current_cell.next
        return current_cell
    

    def insert_previous_by_index(self, ind, x):
        # insert_previous() で size を増やしているのでここで増やしてはならない
        target_cell = self.nth(ind)
        self.insert_previous(target_cell, x)


    def delete(self, target_cell):
        """
        O(1) で target_cell を削除する。
        なお、target_cell は必ず Linked List 内に存在するものとする。        
        """
        assert target_cell is not None
        self.size -= 1
        # 要素数 1 の時
        if self.head == self.head.next:
            self.head = None
        # 要素数 2 以上の時
        else:
            # 削除セルの前のセルの調整
            target_cell.previous.next = target_cell.next
            # 削除セルの次のセルの調整
            target_cell.next.previous = target_cell.previous
            # head ポインタを変える必要があることもある
            if self.head == target_cell:
                self.head = target_cell.next
    

    def count(self, val):
        """O(n) でデータが val と一致するようなセルの数を数え上げる。"""
        ans = 0
        for cell in self:
            if cell.data == val:
                ans += 1
        return ans
    

    def find(self, val):
        """O(n) でデータが val と一致するようなセルのインスタンスを返す。存在しないなら None を返す。"""
        for cell in self:
            if cell.data == val:
                return cell
        else:
            return None



if __name__ == "__main__":
    ll = LinkedList(1, 10, 100, 1000, 10000)
    assert str(ll) == '[1,10,100,1000,10000]'
    assert ll.is_empty() == False
    assert ll.front().data == 1
    assert ll.back().data == 10000
    ll.rotate()
    assert str(ll) == '[10,100,1000,10000,1]'
    ll.reverse_rotate()
    assert str(ll) == '[1,10,100,1000,10000]'
    assert len(ll) == 5

    for i in range(3):
        ll.push_back(2*i)
        ll.push_front(-2*i)
    
    assert str(ll) == '[-4,-2,0,1,10,100,1000,10000,0,2,4]'
    assert ll.pop_front().data == -4
    assert ll.pop_back().data == 4
    assert str(ll) == '[-2,0,1,10,100,1000,10000,0,2]'

    assert ll.count(10) == 1
    assert ll.find(8686) is None
    assert isinstance(ll.find(10), Cell)    # <__main__.Cell object at 0x10fa772d0>

    ll.insert_previous(ll.find(10), 5)
    assert str(ll) == '[-2,0,1,5,10,100,1000,10000,0,2]'
    ll.insert_next(ll.find(10), 20)
    assert str(ll) == '[-2,0,1,5,10,20,100,1000,10000,0,2]'
    ll.delete(ll.find(-2))
    ll.delete(ll.find(0))
    ll.delete(ll.find(0))
    ll.delete(ll.find(2))
    assert str(ll) == '[1,5,10,20,100,1000,10000]'

    assert ll.nth(4).data == 100
    ll.insert_previous_by_index(4, 40)
    assert str(ll) == '[1,5,10,20,40,100,1000,10000]'

    while not ll.is_empty():
        ll.pop_back()
    
    assert ll.size == 0
    assert str(ll) == '[]'
    
    print("* assertion test ok *")





