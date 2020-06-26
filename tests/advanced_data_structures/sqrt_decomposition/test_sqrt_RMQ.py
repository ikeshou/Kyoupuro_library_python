import pytest
from random import randint
from math import sqrt
from mypkg.advanced_data_structures.sqrt_decomposition.sqrt_RMQ import BucketRMQ


def test_BucketRMQ():
    """
    1 <= size <= M のサイズの列を Iteration 回ランダム生成し、それぞれについて Iteration 回ランダムクエリを投げる。
    クエリへの回答を愚直に更新したものと比較するテストを行う。
    """
    with pytest.raises(ValueError):
        BucketRMQ(total_size=100, chunk_size=101)    # invalid chunk size
    with pytest.raises(IndexError):
        rmq = BucketRMQ(100, chunk_size=10)
        rmq.min(-1, 50)    # invalid slices
        rmq.min(20, 20)    # also invalid slices (interval size == 0)

    Iteration = 50
    M = 50
    for _ in range(Iteration):
        size = randint(1, M)
        chunk_size = randint(int(sqrt(size)), size)
        L = [randint(-100, 100) for _ in range(size)]
        rmq = BucketRMQ(size, chunk_size)
        rmq.build(L)

        for _ in range(Iteration):
            if randint(0, 1) == 0:
                # 1 点の変更クエリ
                ind = randint(0, size - 1)
                num = randint(-100, 100)
                rmq.update(ind, num)
                L[ind] = num
            else:
                # 範囲の質問クエリ
                l = randint(0, size-1)
                r = randint(l+1, size)
                print(L, rmq.data, rmq.bucket_min, l, r)
                assert rmq.min(l, r) == min(L[l:r])



if __name__ == "__main__":
    pytest.main(['-v', __file__])
