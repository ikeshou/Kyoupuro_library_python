import pytest
from random import randint
from mypkg.basic_algorithms.around_merge_sort import stable_partition, modified_merge_sort, count_inversion


def test_stable_partition():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか愚直に調べるストレステストを行う。
    """
    Iteration = 100
    M = 50    # L の長さの最大値
    func = lambda x: x % 3 == 0
    for _ in range(Iteration):
        size = randint(0, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        pivot_ind = stable_partition(L, func)
        for i in range(pivot_ind):
            assert func(L[i]) is True
        for i in range(pivot_ind + 1, size):
            assert func(L[i]) is False



def test_modified_merge_sort_count_inversion():
    """
    最大長さが M である、 -1000 ~ 1000 をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか愚直に調べ、組み込みの sorted() との照合を行いストレステストをする。
    """    
    Iteration = 100
    M = 50    # L の長さの最大値
    for _ in range(Iteration):
        size = randint(0, M)
        L = [randint(-1000, 1000) for _ in range(size)]
        naive_inv_cnt = 0
        for i in range(size):
            for j in range(i):
                if L[j] > L[i]:
                    naive_inv_cnt += 1
        assert naive_inv_cnt == count_inversion(L)
        c, seq = modified_merge_sort(L, 0, size)
        assert naive_inv_cnt == c
        assert sorted(L) == seq





if __name__ == "__main__":
    pytest.main(['-v', __file__])
