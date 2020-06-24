import pytest
from random import randint
import numpy as np
import scipy.sparse.csgraph as cs
from scipy.sparse import csr_matrix
from mypkg.graphs.flow.ford_fulkerson import FordFulkerson



def test_ford_fulkerson():
    """
    最大ノード数 M, 最大重み M, 最大辺数ノード数 * 2 で重み付き逆平行有向グラフをランダム作成することを Iteration 回行う。
    それぞれに対し、ソースとシンクを選んでフローを流すことをノード数だけ行い、scipy.sparse.csgraph.maximum_flow と結果を照合するストレステストを行う。
    """
    Iteration = 20
    M = 20
    for _ in range(Iteration):
        n = randint(2, M)

        # ---- ndarray, csr_matrix, エッジを張った FordFulkerson インスタンス生成 ----
        mat = np.full((n, n), 0)
        for _ in range(2 * n):    # 最大で 2 * n 個辺を張る
            a, b = randint(0, n-1), randint(0, n-1)
            if a == b:    # 自己ループはだめ
                continue
            if mat[b, a] == 0:    # 逆平行有向グラフにしたいので
                mat[a, b] = randint(1, M)    # 上書きすることも多々あるだろう
        G = csr_matrix(mat)
        FF = FordFulkerson(n)
        for i in range(n):
            for j in range(n):
                if mat[i, j] != 0:
                    assert i != j
                    assert mat[j, i] == 0
                    FF.add_edge(i, j, mat[i, j])

        # ---- source, sink を決定しフローを流して比較 ----
        for i in range(n):
            while True:
                source, sink = randint(0, n-1), randint(0, n-1)
                if source != sink:
                    break
            # ford_fulkerson をチェック
            if i % 2 == 0:
                expected_max_flow = cs.maximum_flow(G, source, sink).flow_value
                state = FF.reserve_state()
                got_max_flow = FF.ford_fulkerson(source, sink)
                assert got_max_flow == expected_max_flow
                FF.restore_state(state)
            # edmonds_karp をチェック
            else:
                expected_max_flow = cs.maximum_flow(G, source, sink).flow_value
                state = FF.reserve_state()
                got_max_flow = FF.edmonds_karp(source, sink)
                assert got_max_flow == expected_max_flow
                FF.restore_state(state)




if __name__ == "__main__":
    pytest.main(['-v', __file__])
