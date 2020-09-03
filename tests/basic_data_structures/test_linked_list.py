import pytest
from random import randint
from collections import deque
from mypkg.basic_data_structures.linked_list import Cell, LinkedList




def test_linked_list_access():
    """
    最大長さ M の linked list を Iteration 回作成し、アクセスメソッド front, back が正しいかテストを行う
    """
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.front()
    with pytest.raises(IndexError):
        ll.back()
    
    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-100, 100) for _ in range(size)]
        ll = LinkedList(L)
        assert ll.front().data == L[0]
        assert ll.back().data == L[-1]


def test_linked_list_empty_len_str_iter_getitem():
    """
    最大長さ M の linked list を Iteration 回作成し、情報取得メソッド empty, __len__, __str__, __iter__, __getitem__ が正しいかテストを行う
    """ 
    ll = LinkedList()
    assert ll.empty() is True
    assert len(ll) == 0
    assert str(ll) == '[]'
    for _ in ll:
        raise RuntimeError    # 回る前に StopIteration

    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-100, 100) for _ in range(size)]
        ll = LinkedList(L)
        assert ll.empty() is False
        assert len(ll) == len(L)
        assert str(ll) == str(L)
        for i, cell in enumerate(ll):
            assert cell.data == L[i]
            assert ll[i].data == L[i]


def test_linked_list_push_pop():
    """
    最大 M 回ランダムに前 or 後ろから追加し、最大 M 回ランダムに前 or 後ろから削除を行うことを Iteration 回繰り返す。
    deque を用いて、deque に対して処理した結果と同じになるか照合する。
    """
    Iteration = 100
    M = 10
    for _ in range(Iteration):
        dq = deque()
        ll = LinkedList()
        n = randint(0, M)
        for _ in range(n):
            num = randint(-1000, 1000)
            if randint(0, 1) == 0:
                ll.push_front(num)
                dq.appendleft(num)
            else:
                ll.push_back(num)
                dq.append(num)
            for j, cell in enumerate(ll):
                assert cell.data == dq[j]
        for _ in range(n):
            if randint(0, 1) == 0:
                assert ll.pop_front().data == dq.popleft()
            else:
                assert ll.pop_back().data == dq.pop()
            for j, cell in enumerate(ll):
                assert cell.data == dq[j]



def test_linked_list_count_find_remove():
    """
    最大長さ M の linked list を Iteration 回作成し、検索メソッド count, find, 検索削除メソッド remove が正しいかテストを行う
    毎回愚直にリストに対して処理した結果と同じになるか照合する。
    """
    ll = LinkedList([1, 2, 3, 4])
    assert ll.count(100) == 0
    assert ll.find(100) == -1

    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(0, M)
        L = [randint(-10, 10) for _ in range(size)]
        ll = LinkedList(L)
        for i in range(size):
            assert ll.count(L[i]) == L.count(L[i])
            assert ll.find(L[i]) == ll[L.index(L[i])]
        val = randint(- 20, 20)    # あえて要素の値の範囲から外れ得るようにする
        if val not in L:
            with pytest.raises(ValueError):
                ll.remove(val)
        else:
            ll.remove(val)
            L.remove(val)
        assert len(ll) == len(L)
        for j, cell in enumerate(ll):
            assert cell.data == L[j]


def test_linkedlist_insert_ref_erase():
    """
    最大長さ M の linked list を Iteration 回作成し、参照指定挿入メソッド、参照指定削除メソッド
    insert_prev_by_ref, insert_next_by_ref, erase が正しいかテストを行う
    毎回愚直にリストに対して処理した結果と同じになるか照合する。
    """
    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-10, 10) for _ in range(size)]
        ll = LinkedList(L)
        # test for insert_next_by_ref
        ind = randint(0, size - 1)
        num = randint(-1000, 1000)
        cell = ll.find(L[ind])
        ll.insert_next_by_ref(cell, num)
        L.insert(L.index(L[ind]) + 1, num)    # 後ろに挿入なので
        for j, cell in enumerate(ll):
            assert cell.data == L[j]
        # test for insert_prev_by_ref
        ind = randint(0, size)    # サイズは 1 増えている。
        num = randint(-1000, 1000)
        cell = ll.find(L[ind])
        ll.insert_prev_by_ref(cell, num)
        L.insert(L.index(L[ind]), num)
        for j, cell in enumerate(ll):
            assert cell.data == L[j]
        # test for erase
        ind = randint(0, size + 1)   # サイズはさらに 1 増えている。
        cell = ll.find(L[ind])
        ll.erase(cell)
        L.remove(L[ind])
        for j, cell in enumerate(ll):
            assert cell.data == L[j]        



def test_linked_list_insert_by_index():
    """
    最大長さ M の linked list を Iteration 回作成し、参照指定挿入メソッド
    insert_previous_by_reference, insert_next_by_reference が正しいかテストを行う
    毎回愚直にリストに対して処理した結果と同じになるか照合する。
    """
    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(0, M)
        L = [randint(-10, 10) for _ in range(size)]
        ll = LinkedList(L)
        ind = randint(0, size)
        num = randint(-1000, 1000)
        L.insert(ind, num)
        ll.insert_by_index(ind, num)
        assert ll[ind].data == L[ind]


def test_linked_list_rotate_reverse_rotate():
    """
    最大長さ M の linked list を Iteration 回作成し、rotate をランダム回数行う。
    先頭と末尾が正しい値になっているか調査することで簡易的なテストを行う。
    """
    # nothing happens
    ll = LinkedList()
    ll.rotate()
    ll.reverse_rotate()

    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        ll = LinkedList(L)
        k = randint(0, M)    # 適当な回数 rotate
        print(ll, k)
        ll.rotate(k)
        print(ll)
        assert ll.front().data == L[k % size]
        assert ll.back().data == L[k % size - 1]
        ll.reverse_rotate(k)
        assert ll.front().data == L[0]
        assert ll.back().data == L[-1]




if __name__ == "__main__":
    pytest.main(['-v', __file__])
