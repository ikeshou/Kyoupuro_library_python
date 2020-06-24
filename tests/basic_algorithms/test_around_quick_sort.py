import pytest
from random import randint
from mypkg.basic_algorithms.around_quick_sort import randomized_select, nth_element, quick_sort


def test_randomized_select():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """    
    # 0 <= begin <= pivot_ind < end <= len(L) でないとき
    with pytest.raises(IndexError):
        randomized_select([], 0, 0, 0)    # 空はだめ
    with pytest.raises(IndexError):
        randomized_select([1, 2], 0, 3, 1)    # end がオーバー
    with pytest.raises(IndexError):
        randomized_select([1, 2], 0, 1, 2)    # pivot が範囲にいない
    with pytest.raises(IndexError):
        randomized_select([1, 2], -1, 2, 1)    # begin がオーバー

    Iteration = 100
    M = 100    # L の最大の長さ
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        pivot_ind = randint(0, size - 1)
        pivot = L[pivot_ind]
        begin = randint(0, pivot_ind)
        end = randint(pivot_ind + 1, size)
        ind = randomized_select(L, pivot_ind, begin, end)
        for i in range(begin, ind):
            assert L[i] <= pivot
        assert L[ind] == pivot
        for i in range(ind+1, end):
            assert L[i] >= pivot


def test_nth_element():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """
    # 0 <= begin <= i < end <= len(L) でないとき
    with pytest.raises(IndexError):
        nth_element([], 0, 0, 0)    # 空はだめ
    with pytest.raises(IndexError):
        nth_element([1, 2], 1, 0, 3)    # end がオーバー
    with pytest.raises(IndexError):
        nth_element([1, 2], 2, 0, 2)    # ith-order-statitic が範囲にいない
    with pytest.raises(IndexError):
        nth_element([1, 2], 1, -1, 2)    # begin がオーバー
    
    Iteration = 100
    M = 100    # L の最大の長さ
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        i = randint(0, size-1)
        ith_order_statistic = nth_element(L, i)
        assert sorted(L)[i] == ith_order_statistic



def test_quick_sort():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """    
    # begin <= end でないとき
    with pytest.raises(IndexError):
        quick_sort([1, 2], 1, 0)    # 逆転
    with pytest.raises(IndexError):
        quick_sort([1, 2], 0, 3)    # end がオーバー
    with pytest.raises(IndexError):
        quick_sort([1, 2], -1, 2)    # begin がオーバー
    
    # 空の場合
    empty = []
    quick_sort(empty, 0, 0)
    assert empty == []

    Iteration = 100
    M = 100    # L の最大の長さ
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        begin = randint(0, size)
        end = randint(begin, size)
        quick_sort(L, begin, end)
        for i in range(begin + 1, end):
            assert L[i] >= L[i-1]




if __name__ == "__main__":
    pytest.main(['-v', __file__])
