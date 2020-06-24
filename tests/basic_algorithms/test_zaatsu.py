"""
TODO: two_dim_zaatsu_order(), two_dim_zaatsu_region() のテスト
"""


import pytest
from random import randint
from mypkg.basic_algorithms.zaatsu import one_dim_zaatsu_order, one_dim_zaatsu_region, two_dim_zaatsu_order, two_dim_zaatsu_region, TwoDimZaatsu



def test_one_dim_zaatsu_order():
    """
    最大長さが M である、 -100 ~ 100 をとる数列を Iteration 回生成する。
    もとの順番が保存された圧縮結果となっているか、性質を調べるストレステストを行う。
    """
    Iteration = 100
    M = 100
    for _ in range(Iteration):
        size = randint(1, M)
        L = [randint(-100, 100) for _ in range(size)]
        new_n, com, decom = one_dim_zaatsu_order(L)
        assert new_n == len(list(set(L)))
        for i, elm in enumerate(sorted(set(L))):
            assert com[elm] == i    # 点は正しく配置されているか
            assert decom[i] == elm    # 逆の辞書になっているか



def test_one_dim_zaatsu_region():
    """
    最大長さが M である、 -100 ~ 100 をとる数列を Iteration 回生成する。
    もとの順番および空白の存在が保存された圧縮結果となっているか、性質を調べるストレステストを行う。
    """    
    Iteration = 100
    M = 10
    for _ in range(Iteration):
        size = randint(1, M)
        left = randint(-100, 100)
        right = randint(left, 100)
        L = [randint(left, right) for _ in range(size)]
        new_n, com, decom = one_dim_zaatsu_region(L, left, right)
        line = [False] * (right - left + 1)
        for num in L:
            line[num - left] = True
        space_count = 0
        i = 0
        while i < (right - left + 1):
            if not line[i]:
                space_count += 1
                while i < (right - left + 1) and not line[i]:
                    i += 1
            i += 1
        # print(left, right, L)
        assert new_n == space_count + len(list(set(L)))    # スペースの数が正しく反映されているか
        assert list(map(lambda x: x[0], sorted(com.items(), key=lambda x: x[1]))) == sorted(set(L))    # 点は正しく配置されているか
        for k, v in com.items():    # 逆の辞書になっているか
            assert decom[v] == k





if __name__ == "__main__":
    pytest.main(['-v', __file__])
