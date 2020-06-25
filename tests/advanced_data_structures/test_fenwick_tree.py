import pytest
from random import randint
from mypkg.advanced_data_structures.fenwick_tree import FenwickTree


def test_fenwick_tree():
    """
    長さ 1 <= size <= M の数列を Iteration 回生成。
    合計 size * 2 回のランダムな加算クエリと区間和クエリを投げ、計算結果が愚直な計算結果と合致するか判定するテストを行う。
    """
    Iteration = 100
    M = 50
    for _ in range(Iteration):
        size = randint(1, M)
        # ナイーブに更新、計算する方
        L = [randint(-100, 100) for _ in range(size)]
        # 初期化
        ft = FenwickTree(size)
        for i in range(size):
            ft.add(i, L[i])
        # クエリをランダムに投げまくる
        for _ in range(size * 2):
            if randint(0, 1) == 0:
                # add
                ind = randint(0, size-1)
                num = randint(-100, 100)
                L[ind] += num
                ft.add(ind, num)
            else:
                # sum
                i = randint(0, size-1)
                j = randint(i, size-1)
                assert ft.sum(i, j) == sum(L[i:j])




if __name__ == "__main__":
    pytest.main(['-v', __file__])
