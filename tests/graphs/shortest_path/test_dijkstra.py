import pytest
from pytest import approx
from random import randint
import numpy as np
import scipy.sparse.csgraph as cs
from mypkg.graphs.shortest_path.dijkstra import dijkstra, dijkstra_matrix




def test_dijkstra():
    """
    最大ノード数 M, 最大エッジ数 M**2 の非負辺重み付き有向グラフをランダム生成することを Iteration 回行う。
    それぞれについて単一始点最短距離を求め、 scipy.sparce.csgraph.dijkstra の結果と照合するストレステストを行う。
    """
    Iteration = 20
    M = 20
    inf = float('inf')
    for _ in range(Iteration):
        v = randint(2, M)
        e = randint(v, v**2)

        # ---- ndarray, csr_matrix, 隣接リスト、隣接行列生成 ----
        mat = np.full((v, v), inf)
        for i in range(e):    # 最大で v**2 個辺を張ろうとする
            a, b = randint(0, v-1), randint(0, v-1)
            if a == b:    # 自己ループはだめ
                continue
            if mat[b, a] == inf:    # 無向グラフにしたいので
                w = randint(1, M)
                mat[a, b] = w    # 上書きすることも多々あるだろう。
        csr = cs.csgraph_from_dense(mat, null_value=inf)
        adj_with_weight = [[] for _ in range(v)]
        adj_mat = [[inf] * v for _ in range(v)]
        for i in range(v):
            for j in range(v):
                if mat[i, j] != inf:
                    adj_mat[i][j] = mat[i, j]
                    adj_mat[j][i] = mat[i, j]
                    adj_with_weight[i].append((j, mat[i, j]))
                    adj_with_weight[j].append((i, mat[i, j]))
        
        # ---- 結果の比較 ----
        for i in range(v):
            dist = cs.dijkstra(csr, indices = i, directed=False, return_predecessors=False)
            assert dijkstra(adj_with_weight, i) == approx(dist)
            print(adj_mat)
            print(dijkstra(adj_with_weight, i))
            print(dijkstra_matrix(adj_mat, i))
            assert dijkstra_matrix(adj_mat, i) == approx(dist)



if __name__ == "__main__":
    pytest.main(['-v', __file__])

