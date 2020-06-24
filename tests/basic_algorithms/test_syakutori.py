import pytest
from random import randint
from mypkg.basic_algorithms.syakutori import intervals_lt_x, intervals_gt_x


def test_intervals_lt_x():
    """
    最大長さが M である、 1 ~ 1000 をとる数列を Iteration 回生成する。
    ターゲット値 x を 1 ~ 1000 のランダムな値で決定し、それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """
    Iteration = 1000
    M = 10    # L の最大の長さ
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(1, 1000) for _ in range(size)]
        x = randint(1, 1000)
        got_cnt, got_max_width, got_intervals = intervals_lt_x(L, x)
        cnt, max_width, intervals = 0, 0, []
        for i in range(size+1):
            for j in range(i+1, size+1):
                if sum(L[i:j]) <= x:
                    cnt += 1
                    if max_width < j - i:
                        max_width = j - i
                        intervals = [(i, j)]
                    elif max_width == j - i:
                        intervals.append((i, j))
        assert cnt == got_cnt
        assert max_width == got_max_width
        assert intervals == got_intervals



def test_intervals_gt_x():
    """
    最大長さが M である、 1 ~ 1000 をとる数列を Iteration 回生成する。
    ターゲット値 x を 1 ~ 1000 のランダムな値で決定し、それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """    
    Iteration = 100
    M = 10    # L の最大の長さ
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(1, 1000) for _ in range(size)]
        x = randint(1, 1000)
        got_cnt, got_min_width, got_intervals = intervals_gt_x(L, x)
        cnt, min_width, intervals = 0, float('inf'), []
        for i in range(size+1):
            for j in range(i+1, size+1):
                if sum(L[i:j]) >= x:
                    cnt += 1
                    if min_width > j - i:
                        min_width = j - i
                        intervals = [(i, j)]
                    elif min_width == j - i:
                        intervals.append((i, j))
        assert cnt == got_cnt
        assert min_width == got_min_width
        assert intervals == got_intervals    



if __name__ == "__main__":
    pytest.main(['-v', __file__])
