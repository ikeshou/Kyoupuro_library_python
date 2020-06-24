import pytest
from random import sample, randint, randrange
import networkx as nx
from networkx.algorithms import bipartite
from mypkg.graphs.flow.max_size_bipartite_matching import bipartite_max_matching



def test_bipartite_max_matching():
    """
    最大ノード数 M で二部グラフ作成を Iteration 回行う。
    それぞれに対し最大サイズマッチングを行い、結果を networkx.max_weight_matching と照合し、ストレステストを行う。
    """
    Iteration = 50
    M = 50
    for _ in range(Iteration):
        n = randrange(2, M+1, 2)

        # ---- 辺を張った networkx グラフインスタンス、隣接リストを生成 ----
        adj = [[] for _ in range(n)]
        group1 = range(n//2)
        group2 = range(n//2, n)
        G = nx.Graph()
        G.add_nodes_from(group1, bipartite=0)
        G.add_nodes_from(group2, bipartite=1)
        for i in group1:
            target = sample(group2, randint(0, n//2))
            # i から (group2 からサンプリングされた) target の各要素に辺を張る
            for j in target:
                G.add_edge(i, j, weight=1)    # 重み 1
                adj[i].append(j)
                adj[j].append(i)
                
        # ---- 最大マッチングの結果を比較 ----
        got_max_match = bipartite_max_matching(adj, group1, group2)
        expected_max_match = len(nx.max_weight_matching(G))    # マッチした組の辞書が返ってくるけど
        assert got_max_match == expected_max_match







if __name__ == "__main__":
    pytest.main(['-v', __file__])
