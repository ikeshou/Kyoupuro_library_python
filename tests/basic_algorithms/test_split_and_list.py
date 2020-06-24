import pytest
from random import randint
from bisect import bisect_right
from itertools import product
from mypkg.basic_algorithms.split_and_list import split_and_list



def test_split_and_list():
    """
    最大長さが M である、 0 ~ 1000 をとる数列を Iteration 回生成する。
    ターゲット値 x を 0 ~ 1000 のランダムな値で決定し、それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """    
    Iteration = 50
    M = 8    # L の最大サイズ
    for _ in range(Iteration):
        size = randint(0, M)
        L = [randint(0, 1000) for _ in range(size)]
        # ナイーブに全列挙したもので照合を行う。
        enum_all = set()
        for pattern in product([True, False], repeat=size):
            total = 0
            for i in range(size):
                if pattern[i]:
                    total += L[i]
            enum_all.add(total)
        enum_all = sorted(enum_all)
        for _ in range(Iteration):
            x = randint(0, 1000)
            assert split_and_list(L, x) == enum_all[bisect_right(enum_all, x) - 1]





if __name__ == "__main__":
    pytest.main(['-v', __file__])
