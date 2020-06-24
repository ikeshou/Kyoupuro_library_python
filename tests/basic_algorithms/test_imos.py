import pytest
from random import randint
from mypkg.basic_algorithms.imos import Imos1D, Imos2D



def test_imos_1d():
    """
    幅の最大が M である区間を Iteration 回ランダム生成する。
    それぞれについて Iteration 回加算クエリをランダム生成し、ナイーブな手法と結果を照合するストレステストを行う。
    """
    with pytest.raises(ValueError):
        im = Imos1D(10)
        im.add(5, 3, 100)    # i <= j でないと
    with pytest.raises(IndexError):
        im = Imos1D(10)
        im.add(0, 10, 100)    # [0, 10] はだめ
    with pytest.raises(IndexError):
        im = Imos1D(10)
        im.add(-1, 5, 100)    # [-1, 5] はだめ
    
    Iteration = 50
    M = 1000    #  区間の最大長
    for _ in range(Iteration):
        n = randint(1, M)
        im = Imos1D(n)
        naive_interval = [0] * n
        for _ in range(Iteration):
            l = randint(0, n-1)
            r = randint(l, n-1)
            num = randint(-1000, 1000)
            im.add(l, r, num)
            for i in range(l, r+1):
                naive_interval[i] += num
        assert im.total() == naive_interval



def test_imos_2d():
    """
    縦、横の幅の最大が M であるグリッドを Iteration 回ランダム生成する。
    それぞれについて Iteration 回加算クエリをランダム生成し、ナイーブな手法と結果を照合するストレステストを行う。
    """    
    with pytest.raises(ValueError):
        im = Imos2D(10, 10)
        im.add(5, 3, 0, 1, 100)    # sx <= tx でないと
    with pytest.raises(ValueError):
        im = Imos2D(10, 10)
        im.add(0, 1, 5, 3, 100)    # sy <= ty でないと
    with pytest.raises(IndexError):
        im = Imos2D(10, 10)
        im.add(0, 10, 0, 1, 100)    # [0, 10] はだめ
    with pytest.raises(IndexError):
        im = Imos2D(10, 10)
        im.add(-1, 5, 0, 1, 100)    # [-1, 5] はだめ
    with pytest.raises(IndexError):
        im = Imos2D(10, 10)
        im.add(0, 1, 0, 10, 100)    # [0, 10] はだめ
    with pytest.raises(IndexError):
        im = Imos2D(10, 10)
        im.add(0, 1, -1, 5, 100)    # [-1, 5] はだめ
    
    Iteration = 30
    M = 50    # 縦および横の最大長
    for _ in range(Iteration):
        H = randint(1, M)
        W = randint(1, M)
        im = Imos2D(H, W)
        naive_grid = [[0] * W for _ in range(H)]
        for _ in range(Iteration):
            sx, sy = randint(0, H-1), randint(0, W-1)
            tx, ty = randint(sx, H-1), randint(sy, W-1)
            num = randint(-1000, 1000)
            im.add(sx, tx, sy, ty, num)
            for i in range(sx, tx+1):
                for j in range(sy, ty+1):
                    naive_grid[i][j] += num
        assert im.total() == naive_grid




if __name__ == "__main__":
    pytest.main(['-v', __file__])

            
