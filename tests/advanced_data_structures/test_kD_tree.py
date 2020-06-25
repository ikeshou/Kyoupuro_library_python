import pytest
from random import randint
from mypkg.advanced_data_structures.kD_tree import TwoDimNode, TwoDimTree



def test_two_dim_search():
    """
    1<=H<=1000, 1<=W<=1000 なるランダムな長方形に 1000 個ランダムに点がばらまかれた盤面を Iteration 回生成。
    それぞれについて Iteration 個のレンジサーチクエリをランダム作成し、ナイーブな手法と結果を照らし合わせるストレステストを行う。
    """
    Iteration = 10
    # Iteration 回盤面形成
    for _ in range(Iteration):
        H, W = randint(1, 1000), randint(1, 1000)
        # グリッドに点をばらまく
        L_2 = [(randint(0, H), randint(0, W)) for _ in range(1000)]
        # 平衡した kD tree 作成
        tree_2 = TwoDimTree(L_2)
        # Iteration 個レンジサーチクエリをランダム作成
        query = []
        for _ in range(Iteration):
            sx, tx = randint(0, H), randint(0, H)
            sy, ty = randint(0, W), randint(0, W)
            sx, tx = min(sx, tx), max(sx, tx)
            sy, ty = min(sy, ty), max(sy, ty)
            query.append((sx, tx, sy, ty))
        # クエリへの答えが Iteration 個全てについて正しかったか確認
        for sx, tx, sy, ty in query:
            calculated_points = tree_2.two_dim_search(sx, tx, sy, ty)
            ans_points = []
            for i, j in L_2:
                if sx <= i <= tx and sy <= j <= ty:
                    ans_points.append((i, j))
            assert (set(calculated_points) == set(ans_points))   



if __name__ == "__main__":
    pytest.main(['-v', __file__])


