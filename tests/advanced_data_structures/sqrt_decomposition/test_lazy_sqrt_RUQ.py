import pytest
from random import randint
from math import sqrt
from mypkg.advanced_data_structures.sqrt_decomposition.lazy_sqrt_RUQ import BucketRUQ


def test_lazy_BucketRUQ():
    """
    1 <= size <= M のサイズの列を Iteration 回ランダム生成し、それぞれについて Iteration 回ランダムクエリを投げる。
    クエリへの回答を愚直に更新したものと比較するテストを行う。
    """
    with pytest.raises(ValueError):
        BucketRUQ(total_size=100, chunk_size=101)    # invalid chunk size
    with pytest.raises(IndexError):
        ruq = BucketRUQ(100, chunk_size=10)
        ruq.range_update(-1, 50, 100)    # invalid slices

    Iteration = 50
    M = 50
    for _ in range(Iteration):
        size = randint(1, M)
        chunk_size = randint(int(sqrt(size)), size)
        L = [randint(-100, 100) for _ in range(size)]
        ruq = BucketRUQ(size, chunk_size)
        ruq.build(L)

        for _ in range(Iteration):
            if randint(0, 1) == 0:
                # 区間のの変更クエリ
                l = randint(0, size)
                r = randint(l, size)
                num = randint(-100, 100)
                ruq.range_update(l, r, num)
                for i in range(l, r):
                    L[i] = num
            else:
                # 1 点の質問クエリ
                i = randint(0, size - 1)
                assert ruq.get(i) == L[i]



if __name__ == "__main__":
    pytest.main(['-v', __file__])
