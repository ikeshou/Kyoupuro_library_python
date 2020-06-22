"""
(参考) <Algorithm Introduction vol.1 p.194-202>
循環双方向連結リスト

- 連結リストは組み込みで用意されていないので自前で用意する必要がある。


<メソッド早見表>
巡回、出力系
    __str__(), __len__(), __iter()__
基本的な定数時間操作
    is_empty(), front(), back(), rotate(), reverse_rotate()
基本的な探索
    nth(), find(), count()
挿入
    push_back(), push_front(), pop_back(), pop_front(), insert_previous_by_reference(), insert_next_by_reference(), 
    insert_by_index()
削除
    delete()


partially verified @AOJ ALDS1_3_C
http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_3_C&lang=ja
"""


from typing import Any, Callable, Optional


class Cell:
    def __init__(self, data: Any, prev_cell: Optional['Cell']=None, next_cell: Optional['Cell']=None):
        """
        Args:
            data (object)
            prev_cell (Cell)
            next_cell (Cell)
        """
        self.data = data
        self.previous = prev_cell
        self.next = next_cell
    
    def __str__(self) -> str:
        return 'Cell(' + str(self.data) + ')'
        

class LinkedList:
    def __init__(self, *args: Any):
        self.head = Cell(None)
        self.head.previous = self.head
        self.head.next = self.head
        self.size = 0
        for x in args:
            self.push_back(x)


    def is_empty(self) -> bool:
        """
        O(1) で空かどうか判定する
        >>> LinkedList().is_empty()
        True
        """
        return self.size == 0
    
    def front(self) -> Cell:
        """
        O(1) で先頭のセルの参照を返す
        >>> print(LinkedList(1, 3, 5).front())
        Cell(1)
        """
        if self.size == 0:
            raise IndexError
        return self.head.next

    def back(self) -> Cell:
        """
        O(1) で末尾のセルの参照を返す
        >>> print(LinkedList(1, 3, 5).back())
        Cell(5)
        """        
        if self.size == 0:
            raise IndexError
        return self.head.previous
            
    def __str__(self) -> str:
        """
        >>> print(LinkedList(1, 3, 5))
        [1, 3, 5]
        """
        return '[' + ", ".join([str(cons.data) for cons in self]) + ']'
    
    def __len__(self) -> int:
        """
        >>> len(LinkedList(1, 3, 5))
        3
        """
        return self.size

    def __iter__(self) -> Cell:
        self.ind = self.head
        return self

    def __next__(self) -> Cell:
        self.ind = self.ind.next
        if self.ind is self.head:
            raise StopIteration
        return self.ind


    def push_front(self, x: Any) -> None:
        """
        O(1) で先頭にデータが x であるセルを追加

        >>> ll = LinkedList(1, 3, 5)
        >>> ll.push_front(-1)
        >>> print(ll)
        [-1, 1, 3, 5]
        """
        pushed_cell = Cell(x)
        pushed_cell.next = self.head.next
        pushed_cell.previous = self.head
        self.head.next.previous = pushed_cell
        self.head.next = pushed_cell
        self.size += 1

    def push_back(self, x: Any) -> None:
        """
        O(1) で末尾にデータが x であるセルを追加
        
        >>> ll = LinkedList(1, 3, 5)
        >>> ll.push_back(7)
        >>> print(ll)
        [1, 3, 5, 7]
        """
        pushed_cell = Cell(x)
        pushed_cell.previous = self.head.previous
        pushed_cell.next = self.head
        self.head.previous.next = pushed_cell
        self.head.previous = pushed_cell
        self.size += 1
    
    def pop_front(self) -> Cell:
        """
        O(1) で先頭のセルを pop して返す

        >>> print(LinkedList(1, 3, 5).pop_front())
        Cell(1)
        """
        if self.size == 0:
            raise IndexError(f"LinkedList.pop_front(): cannot pop from an empty linked list.")
        popped_cell = self.head.next
        self.head.next.next.previous = self.head
        self.head.next = self.head.next.next
        self.size -= 1
        return popped_cell

    def pop_back(self) -> Cell:
        """
        O(1) で末尾のセルを pop して返す

        >>> print(LinkedList(1,3,5).pop_back())
        Cell(5)
        """
        if self.size == 0:
            raise IndexError(f"LinkedList.pop_back(): cannot pop from an empty linked list.")
        popped_cell = self.head.previous
        self.head.previous.previous.next = self.head
        self.head.previous = self.head.previous.previous
        self.size -= 1
        return popped_cell
    

    def insert_previous_by_reference(self, target_cell: Cell, x: Any) -> Cell:
        """
        Linked List の中のあるセルへの参照を受け取り、 O(1) でデータが x であるセルを作成しそのセルの前に挿入する

        Args:
            target_cell (Cell)
            x (object)

        Returns:
            Cell: 挿入されたセル
        
        Examples:
            >>> ll = LinkedList(1, 3, 5)
            >>> print(ll.insert_previous_by_reference(ll.nth(1), 2))
            Cell(2)
            >>> print(ll)
            [1, 2, 3, 5]        
        """
        inserted_cell = Cell(x, prev_cell=target_cell.previous, next_cell=target_cell)
        inserted_cell.previous.next = inserted_cell
        inserted_cell.next.previous = inserted_cell
        self.size += 1
        return inserted_cell

    def insert_next_by_reference(self, target_cell: Cell, x: Any) -> Cell:
        """
        Linked List の中のあるセルへの参照を受け取り、 O(1) でデータが x であるセルを作成しそのセルの後ろに挿入する
    
        Args:
            target_cell (Cell)
            x (object)

        Returns:
            Cell: 挿入されたセル

        Examples:
            >>> ll = LinkedList(1, 3, 5)
            >>> print(ll.insert_next_by_reference(ll.nth(1), 2))
            Cell(2)
            >>> print(ll)
            [1, 3, 2, 5]        
        """
        inserted_cell = Cell(x, prev_cell=target_cell, next_cell=target_cell.next)
        inserted_cell.previous.next = inserted_cell
        inserted_cell.next.previous = inserted_cell
        self.size += 1
        return inserted_cell


    def nth(self, ind: int) -> Cell:
        """
        Linked List の中で ind 番目 (0-index) であるセルを O(ind) で探索して参照を返す
        ind が負の場合は n + ind と同じ扱いをする

        Args:
            ind (int): 負数も可

        Returns:
            Cell

        Raises:
            IndexError: index out of range のとき

        Examples:
            >>> print(LinkedList(1, 3, 5).nth(-1))
            Cell(5)
            >>> print(LinkedList(1, 3, 5).nth(2))
            Cell(5)
        """
        if ind < -self.size or self.size-1 < ind:
            raise IndexError(f"LinkedList.nth(): index out of range. got f{ind} (size={self.size})")
        if ind < 0:
            ind += self.size
        tmp = self.head.next
        for _ in range(ind):
            tmp = tmp.next
        return tmp

    def insert_by_index(self, ind: int, x: Any) -> Cell:
        """
        O(ind) で ind (0-index) の位置にデータが x であるようなセルが新たに挿入される

        Args:
            ind (int)
            x (object)

        Returns:
            Cell: 挿入されたセル

        Examples:
            >>> ll = LinkedList(1000)
            >>> print(ll.insert_by_index(0, 100))
            Cell(100)
            >>> print(ll)
            [100, 1000]
        """
        return self.insert_previous_by_reference(self.nth(ind), x)


    def delete(self, target_cell: Cell) -> None:
        """
        O(1) で Linked List の中のあるセルへの参照を受け取り、そのセルを削除する
        
        Args:
            target_cell (Cell)

        Examples:
            >>> ll = LinkedList(1,3,5)
            >>> ll.delete(ll.nth(1))
            >>> print(ll)
            [1, 5]
        """
        target_cell.previous.next = target_cell.next
        target_cell.next.previous = target_cell.previous
        self.size -= 1
    

    def rotate(self, k: int=1) -> None:
        """
        O(k) で順方向、反時計回りに k 回転する
        
        >>> ll = LinkedList(1, 3, 5)
        >>> ll.rotate()
        >>> print(ll)
        [3, 5, 1]
        """
        if self.size > 0:
            for _ in range(k):
                next_cell = self.head.next
                self.delete(self.head)
                self.head = self.insert_next_by_reference(next_cell, None)
    
    def reverse_rotate(self, k: int=1) -> None:
        """
        O(k) で逆方向、時計回りに k 回転する

        >>> ll = LinkedList(1, 3, 5)
        >>> ll.reverse_rotate()
        >>> print(ll)
        [5, 1, 3]
        """
        if self.size > 0:
            for _ in range(k):
                prev_cell = self.head.previous
                self.delete(self.head)
                self.head = self.insert_previous_by_reference(prev_cell, None)
    

    def count(self, val: Any, key: Callable[[Any], Any]=lambda x: x):
        """
        O(n) で key(Cell.data) が val と一致するようなセルの数を数えて返す

        >>> LinkedList(1, 3, 5, 7, 9).count(True, key=lambda x: x>=5)
        3
        """
        cnt = 0
        for cons in self:
            if key(cons.data) == val:
                cnt += 1
        return cnt

    def find(self, val: Any, key: Callable[[Any], Any]=lambda x: x):
        """
        O(n) で key(Cell.data) が val と一致するようなセルを探索し、発見したらそのセルを返す。発見できなかったら -1 を返す。

        >>> print(LinkedList(1, 2, 3, 4, 5).find(2))
        Cell(2)
        """
        for cons in self:
            if key(cons.data) == val:
                return cons
        return -1 



if __name__ == "__main__":
    import doctest
    doctest.testmod()


    ll = LinkedList(1, 10, 100, 1000, 10000)
    assert str(ll) == '[1, 10, 100, 1000, 10000]'
    assert ll.is_empty() == False
    assert ll.front().data == 1
    assert ll.back().data == 10000
    ll.rotate()
    assert str(ll) == '[10, 100, 1000, 10000, 1]'
    ll.reverse_rotate()
    assert str(ll) == '[1, 10, 100, 1000, 10000]'
    assert len(ll) == 5

    for i in range(3):
        ll.push_back(2*i)
        ll.push_front(-2*i)
    
    assert str(ll) == '[-4, -2, 0, 1, 10, 100, 1000, 10000, 0, 2, 4]'
    assert ll.pop_front().data == -4
    assert ll.pop_back().data == 4
    assert str(ll) == '[-2, 0, 1, 10, 100, 1000, 10000, 0, 2]'

    assert ll.count(10) == 1
    assert ll.find(8686) == -1
    assert isinstance(ll.find(10), Cell)    # <__main__.Cell object at 0x10fa772d0>

    ll.insert_previous_by_reference(ll.find(10), 5)
    assert str(ll) == '[-2, 0, 1, 5, 10, 100, 1000, 10000, 0, 2]'
    ll.insert_next_by_reference(ll.find(10), 20)
    assert str(ll) == '[-2, 0, 1, 5, 10, 20, 100, 1000, 10000, 0, 2]'
    ll.delete(ll.find(-2))
    ll.delete(ll.find(0))
    ll.delete(ll.find(0))
    ll.delete(ll.find(2))
    assert str(ll) == '[1, 5, 10, 20, 100, 1000, 10000]'

    assert ll.nth(4).data == 100
    ll.insert_by_index(4, 40)
    assert str(ll) == '[1, 5, 10, 20, 40, 100, 1000, 10000]'

    while not ll.is_empty():
        ll.pop_back()
    
    assert ll.size == 0
    assert str(ll) == '[]'
    
    print("* assertion test ok *")





