import pytest
from pytest import approx
from random import randint
import numpy as np
import scipy.sparse.csgraph as cs
from mypkg.graphs.shortest_path.bellman_ford import NegativeCycleError, Edge, bellman



def test_bellman():
    """
    最大ノード数 M, 最大エッジ数 M**2 の負のサイクルを含まない重み付き有向グラフをランダム生成することを Iteration 回行う。
    それぞれについて単一始点最短距離を求め、 scipy.sparce.csgraph.bellman_ford の結果と照合するストレステストを行う。
    """
    Iteration = 50
    M = 30
    inf = float('inf')
    for _ in range(Iteration):
        v = randint(2, M)
        e = randint(v, v**2)

        # ---- ndarray, csr_matrix, エッジリスト生成 ----
        mat = np.full((v, v), inf)
        for i in range(e):    # 最大で v**2 個辺を張ろうとする
            a, b = randint(0, v-1), randint(0, v-1)
            if a == b:    # 自己ループはだめ
                continue
            w = randint(-M, M)    # - M
            mat[a, b] = w    # 上書きすることも多々あるだろう。
        csr = cs.csgraph_from_dense(mat, null_value=inf)
        edges = []
        for i in range(v):
            for j in range(v):
                if mat[i, j] != inf:
                    edges.append(Edge(i, j, mat[i, j]))
        
        # ---- 結果の比較 ----
        try:
            dist_mat = cs.bellman_ford(csr, return_predecessors=False).tolist()
            for i in range(v):
                # print(dist_mat)
                assert bellman(edges, v, i) == approx(dist_mat[i])
        # 負サイクルができてしまった場合に検出できるか
        except cs._shortest_path.NegativeCycleError:
            with pytest.raises(NegativeCycleError):
                for i in range(v):
                    bellman(edges, v, i)





if __name__ == "__main__":
    pytest.main(['-v', __file__])

