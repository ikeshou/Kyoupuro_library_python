import pytest
from random import randint
from math import sqrt
from mypkg.advanced_data_structures.sqrt_decomposition.sqrt_RAQ_RSQ import BucketRAQ_RSQ


def test_BucketRAQ_RSQ():
    """
    1 <= size <= M のサイズの列を Iteration 回ランダム生成し、それぞれについて Iteration 回ランダムクエリを投げる。
    クエリへの回答を愚直に更新したものと比較するテストを行う。
    """
    with pytest.raises(ValueError):
        BucketRAQ_RSQ(total_size=100, chunk_size=101)    # invalid chunk size
    with pytest.raises(IndexError):
        raq = BucketRAQ_RSQ(100, chunk_size=10)
        raq.range_add(-1, 50, 1000)    # invalid slices
    with pytest.raises(IndexError):
        raq = BucketRAQ_RSQ(100, chunk_size=10)
        raq.sum(-1, 50)    # invalid slices
    
    Iteration = 5
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        chunk_size = randint(int(sqrt(size)), size)
        L = [randint(-100, 100) for _ in range(size)]
        raq_rsq = BucketRAQ_RSQ(size, chunk_size)
        raq_rsq.build(L)

        for _ in range(Iteration):
            if randint(0, 1) == 0:
                # 範囲の加算クエリ
                l = randint(0, size)
                r = randint(l, size)
                num = randint(-100, 100)
                raq_rsq.range_add(l, r, num)
                for i in range(l, r):
                    L[i] += num
            else:
                # 範囲の質問クエリ
                l = randint(0, size)
                r = randint(l, size)
                print(L, l, r)
                print(raq_rsq.bucket_add)
                print(raq_rsq.bucket_sum)
                assert raq_rsq.sum(l, r) == sum(L[l:r])




if __name__ == "__main__":
    pytest.main(['-v', __file__])
