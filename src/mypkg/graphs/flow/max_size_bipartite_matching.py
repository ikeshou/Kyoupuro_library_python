"""
(参考) <Algorithm Introduction vol.2 p.315-318>
二部グラフの最大マッチング問題

<algorithm>
超入口、超出口を用意して各辺を容量 1 と見なして最大フローを流すのみ

二部グラフの最大マッチングを求めるアルゴリズムを用いて
二部グラフの
最小辺被覆問題 (選んだ辺の両端の頂点を集めることができる。このとき、全ての頂点をカバーできるような最小の辺集合は何か？)
最小点被覆問題 (選んだ頂点から伸びる全ての辺を集めることができる。このとき、全ての辺をカバーできるような最小の頂点集合は何か？)
最大安定点問題 (その集合のどの 2 頂点も直接辺で結ばれていないような最大の頂点集合は何か？) <- 実は最小点被覆集合の補集合だけど
を解くことができる

verified @AtCoder ABC091_C
"""


from collections import deque
from copy import deepcopy
from typing import Sequence, List, Union, Any
from .ford_fulkerson import Edge, FordFulkerson

Num = Union[int, float]



def bipartite_max_matching(adj_list: Sequence[Sequence[int]], left_indices: Sequence[int], right_indices: Sequence[int], ford_fulkerson: bool=True) -> Num:
    """
    [left_indices] + [right_indices] なる頂点集合で (無向) 二部グラフが構成されているとする
    隣接リストが渡されるので、超入口と超出口を追加し、left から right へと有向辺 (capacity 1) を接続し、逆辺 (capacity 0) もはった有向グラフを構築する。
    Ford Fulkerson 法を用いて最大流を求めることで最大マッチングを計算できる。

    Args:
        adj_list (list): 隣接リスト
        left_indices (list): (無向) 二部グラフの片側の頂点集合 (0-index 表記)
        right_indices (list): (無向) 二部グラフのもう片側の頂点集合 (0-index 表記)
        ford_fulkerson (bool): True の時は最大フローを ford_fulkerson アルゴリズムで、False の時は edmonds_karp アルゴリズムで求める
    Returns:
        max_size_matching (int)
    """
    n, l, r = len(adj_list), len(left_indices), len(right_indices)
    if n != l + r:
        raise RuntimeError(f"bipartite_max_matching(): the number of vertice mismatched. num of vertice: {n}, left: {l}, right: {r}")
    ff = FordFulkerson(n + 2)    # 超入口と超出口分
    # 順辺、逆辺をはる
    for i in left_indices:
        for j in adj_list[i]:
            ff.add_edge(i+1, j+1, 1)    # 超入口分 1 だけ増やし 1-index 風になる
    # 超入口、出口を作成し capacity 1 で辺をはる
    super_entrance = 0
    for j in left_indices:
        ff.add_edge(super_entrance, j+1, 1)
    super_exit = n + 1
    for i in right_indices:
        ff.add_edge(i+1, super_exit, 1)
    # 最大流を求める
    return ff.ford_fulkerson(super_entrance, super_exit) if ford_fulkerson else  ff.edmonds_karp(super_entrance, super_exit)




if __name__ == "__main__":
    adjacent_list = ((1,),    # 0->
                     (0, 2, 4),
                     (1, 9),    # 2->
                     (4, ),
                     (1, 3, 5, 9),    # 4->
                     (4, 6),
                     (5, 7, 9),    # 6->
                     (6, ),
                     (9,),    # 8->
                     (2, 4, 6, 8))
    max_match = bipartite_max_matching(adjacent_list, left_indices=(0,2,4,6,8), right_indices=(1,3,5,7,9))
    print(max_match)
    """
    path: [0, 1], current flow: 1
    path: [2, 9], current flow: 2
    path: [4, 3], current flow: 3
    path: [6, 5], current flow: 4
    4
    """
