import pytest
from random import randint
from math import sqrt
from mypkg.advanced_data_structures.sqrt_decomposition.sqrt_RSQ import BucketRSQ


def test_BucketRSQ():
    """
    1 <= size <= M のサイズの列を Iteration 回ランダム生成し、それぞれについて Iteration 回ランダムクエリを投げる。
    クエリへの回答を愚直に更新したものと比較するテストを行う。
    """
    with pytest.raises(ValueError):
        BucketRSQ(total_size=100, chunk_size=101)    # invalid chunk size
    with pytest.raises(IndexError):
        rsq = BucketRSQ(100, chunk_size=10)
        rsq.sum(-1, 50)    # invalid slices

    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        chunk_size = randint(int(sqrt(size)), size)
        L = [randint(-100, 100) for _ in range(size)]
        rsq = BucketRSQ(size, chunk_size)
        rsq.build(L)

        for _ in range(Iteration):
            if randint(0, 1) == 0:
                # 1 点の変更クエリ
                ind = randint(0, size - 1)
                num = randint(-100, 100)
                rsq.update(ind, num)
                L[ind] = num
            else:
                # 範囲の質問クエリ
                l = randint(0, size)
                r = randint(l, size)
                assert rsq.sum(l, r) == sum(L[l:r])



if __name__ == "__main__":
    pytest.main(['-v', __file__])
