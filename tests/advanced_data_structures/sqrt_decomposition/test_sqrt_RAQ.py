import pytest
from random import randint
from math import sqrt
from mypkg.advanced_data_structures.sqrt_decomposition.sqrt_RAQ import BucketRAQ


def test_BucketRAQ():
    """
    1 <= size <= M のサイズの列を Iteration 回ランダム生成し、それぞれについて Iteration 回ランダムクエリを投げる。
    クエリへの回答を愚直に更新したものと比較するテストを行う。
    """
    with pytest.raises(ValueError):
        BucketRAQ(total_size=100, chunk_size=101)    # invalid chunk size
    with pytest.raises(IndexError):
        raq = BucketRAQ(100, chunk_size=10)
        raq.range_add(-1, 50, 1000)    # invalid slices
    
    Iteration = 100
    M = 100
    for _ in range(Iteration):
        size = randint(1, M)
        chunk_size = randint(int(sqrt(size)), size)
        L = [randint(-100, 100) for _ in range(size)]
        raq = BucketRAQ(size, chunk_size)
        raq.build(L)

        for _ in range(Iteration):
            if randint(0, 1) == 0:
                # 範囲の加算クエリ
                l = randint(0, size)
                r = randint(l, size)
                num = randint(-100, 100)
                raq.range_add(l, r, num)
                for i in range(l, r):
                    L[i] += num
            else:
                # 1 点の質問クエリ
                ind = randint(0, size - 1)
                assert raq.get(ind) == L[ind]



if __name__ == "__main__":
    pytest.main(['-v', __file__])
