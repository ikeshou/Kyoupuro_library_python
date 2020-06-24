import pytest
from random import randint
from mypkg.basic_algorithms.sliding_window_min import sliding_minimum_query


def test_sliding_minimum_query():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    ウィンドウサイズを size 以下のランダムな値で決定し、それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """
    with pytest.raises(ValueError):
        sliding_minimum_query([1, 2, 3], 0)   # k < 1
    with pytest.raises(IndexError):
        sliding_minimum_query([1, 2, 3], 4)    # k > n
    
    Iteration = 100
    M = 50    # L の最大長
    for _ in range(Iteration):
        size = randint(1, M)
        k = randint(1, size)
        L = [randint(-1000, 1000) for _ in range(size)]
        got = sliding_minimum_query(L, k)
        expected = [min(L[i:i+k]) for i in range(size - k + 1)]
        assert expected == got





if __name__ == "__main__":
    pytest.main(['-v', __file__])
