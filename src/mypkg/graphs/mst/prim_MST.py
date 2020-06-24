"""
(参考) <Algorithm Introduction vol.2 p.230-236>
無向グラフに対する Prim 法による MST の構築 (O((V+E)lgV)

<algorithm>
MST を成長させる root を受け取る
これが最初の MST の部分木となる
MST 部分木の頂点(S) - それ以外の頂点を接続する(V-S) として、カット(S, V-S)と交差する最小の重みの辺を選択し、MST 部分木を成長させる。

候補となる最小の辺を効率的に選択するために min pqueue を使用する。
min pqueue には V-S の各頂点が、'それぞれの頂点と S の各頂点と接続する辺のうち最小のもの' をキーとして収納される。
その際、接続先の頂点の情報も保持する。(MST に取り込まれたら、この頂点の親になる)
V-S の各頂点について選択されうる S との接続辺の予選を行っておき min pqueue にぶち込んでおくイメージ
決勝は extract の際よしなに min pqueue 側で選択される
"""


from heapq import heappush, heappop
from typing import Sequence, List, Tuple, Union
from ...basic_data_structures.priority_queue import PQueueMin

Num = Union[int, float]

    

def prim_mst(adj: Sequence[Sequence[int]], start: int=0) -> Tuple[int, List[int]]:
    n = len(adj)
    pq = PQueueMin()
    pq.add_task((start, None), 0)    # task = (self, parent), priority = weight
    part_of_mst = [False] * n
    total_cost = 0
    parent_ind_of_each_node = [0] * n
    while not pq.empty():
        (u, parent), weight = pq.pop_task()
        # 選択された頂点が {V}\{S} 側であることを確認 (すでに S へ追加されている可能性あり)
        # 満たしていなかったらその辺は '捨てる'
        if not part_of_mst[u]:
            # S 側へ追加
            part_of_mst[u] = True
            total_cost += weight
            parent_ind_of_each_node[u] = parent
            # 各隣接頂点についてカットと交差する辺を全て追加していく
            for v, weight_uv in adj[u]:
                if not part_of_mst[v]:
                    pq.add_task((v, u), weight_uv)
    return total_cost, parent_ind_of_each_node



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
    total, parent_list = prim_mst(adj_with_weight)
    assert(total == 37)
    assert(parent_list == [None, 0, 5, 2, 3, 6, 7, 0, 2])
    print(" * assertion test ok * ")

