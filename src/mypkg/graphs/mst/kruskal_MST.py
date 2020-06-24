"""
(参考) <Algorithm Introduction vol.2 p.230-236>
無向グラフに対する Kruskal 法による MST の構築 (O((V+E)lgV)

<algorithm>
それぞれのノード単体からなる MST が V 個存在する
これを成長連結させて一つの巨大な MST にする。
成長させるための辺の選択は、まだ MST の内部に取り込まれていない辺のうち最小のものを選択するようにする。その結果必ず異なる 2 つのグループが 1 つに union される。

verified @ABC065D
"""


from typing import Sequence
from ...advanced_data_structures.union_find_tree import UnionFindTree



def kruskal(adj: Sequence[Sequence[int]]) -> int:
    n = len(adj)
    uf = UnionFindTree(n)
    edges = []
    total_cost = 0
    for i, e in enumerate(adj):
        for j, weight in e:
            if i <= j:
                edges.append((i, j, weight))
    edges.sort(key=lambda x: x[2])
    for edge in edges:
        u, v, weight = edge
        if uf.union(u, v):
            total_cost += weight
    return total_cost



if __name__ == "__main__":
    adj_with_weight = (((1, 4), (7, 8)),
                    ((0, 4), (2, 8), (7, 11)),
                    ((1, 8), (3, 7), (5, 4), (8, 2)),
                    ((2, 7), (4, 9), (5, 14)),
                    ((3, 9), (5, 10)),
                    ((2, 4), (3, 14), (4, 10), (6, 2)),
                    ((5, 2), (7, 1), (8, 6)),
                    ((0, 8), (1, 11), (6, 1), (8, 7)),
                    ((2, 2), (6, 6), (7, 7)))
    total = kruskal(adj_with_weight)
    assert(total == 37)
    print(" * assertion test ok * ")


