import pytest
from random import randint
import numpy as np
import scipy.sparse.csgraph as cs
from mypkg.graphs.mst.kruskal_MST import kruskal



def test_kruskal():
    """
    最大ノード数 M, 最大エッジ数 M**2 の連結な重み付き無向グラフをランダム生成することを Iteration 回行う。
    それぞれについて MST を求め、 scipy.sparce.csgraph.minimum_spanning_tree の結果と照合するストレステストを行う。
    """
    Iteration = 50
    M = 50
    for _ in range(Iteration):
        v = randint(2, M)
        e = randint(v, v**2)

        # ---- ndarray 生成、scipy で解く ----
        mat = np.full((v, v), 0)
        # 連結を保証
        for i in range(1, v):
            mat[i-1, i] = randint(1, M)        
        for _ in range(e):    # 最大で v**2 個辺を張ろうとする
            a, b = randint(0, v-1), randint(0, v-1)
            if a == b:    # 自己ループはだめ
                continue
            w = randint(1, M)
            mat[a, b] = w    # 上三角行列の形で OK. 上書きすることも多々あるだろう。

        mst = cs.minimum_spanning_tree(mat)
        expected_total = mst.sum()        

        # ---- 隣接リスト生成、ライブラリで解く ----
        adj = [[] for _ in range(v)]
        for i in range(v):
            for j in range(v):
                if mat[i, j] != 0:
                    adj[i].append((j, mat[i, j]))
                    adj[j].append((i, mat[i, j]))
        got_total = kruskal(adj)

        assert got_total == expected_total





if __name__ == "__main__":
    pytest.main(['-v', __file__])


