"""
<Algorithm Introduction vol.2 p.254-259>
Dijkstra 法 
負辺を含まぬ重みつきグラフについて単一始点最短距離を O((E+V)lgV) で計算する
(頂点を回るときに最小のものを取り出していくのに VlgV, cost の更新で ElgV)

<algorithm>
距離が確定していない頂点のうち最短距離であるものを貪欲に選び距離を確定。その頂点から隣接に対し再び最短距離計算を行うことを繰り返す。
"""


from heapq import heappush, heappop
from typing import Sequence, List, Tuple, Union
from ...basic_data_structures.priority_queue import PQueueMin

Num = Union[int, float]



# verified @ABC035D, ABC051D
def dijkstra(adj_with_weight: Sequence[Sequence[int]], start: int=0) -> List[Num]:
    """
    重みつき隣接リストを用いた Dijkstra 法 O((E+V)lgV) (頂点を回るときに最小のものを取り出していくのに VlgV, cost の更新で ElgV)
    負辺を含まぬ重みつきグラフについて、ある頂点から他の頂点までの最短コストを貪欲に計算する
    """
    V = len(adj_with_weight)
    cost = [float('inf')] * V    # cost[i] = (minimum cost from node_start to node_i)
    cost[start] = 0
    fixed = [False] * V
    pq = PQueueMin()
    # 最初は始点が必ずコスト最小。pq に突っ込む
    pq.add_task(start, cost[start])
    while not pq.empty():
        # 現段階で最短のコストとなっている頂点を選択
        u, cost_of_u = pq.pop_task()
        fixed[u] = True
        for v, weight_of_uv in adj_with_weight[u]:
            if not fixed[v] and cost[v] > cost_of_u + weight_of_uv:
                cost[v] = cost_of_u + weight_of_uv
                pq.add_task(v, cost[v])
    return cost




def min_ind_except_for_fixed(seq: List[Num], fixed: List[bool]) -> int:
    m = float('inf')
    for i in range(len(seq)):
        if not fixed[i] and seq[i] < m:
            min_ind, m = i, seq[i]
    if m != float('inf'):
        return min_ind
    else:
        return -1


# verified @ABC022C, ABC079D
def dijkstra_matrix(adj_matrix_weight: Sequence[Sequence[int]], start: int) -> List[int]:
    """
    重みつき隣接行列を用いた Dijkstra 法 O(V^2) (毎回全頂点を見て距離が確定してない奴らの中で最小となっているものを選ぶ)
    負辺を含まぬ重みつきグラフについて、ある頂点から他の頂点までの最短コストを貪欲に計算する
    """
    V = len(adj_matrix_weight)
    cost = [float('inf')] * V    # cost[i] = (minimum cost from node_start to node_i)
    cost[start] = 0
    fixed = [False] * V
    for _ in range(V):
        u = min_ind_except_for_fixed(cost, fixed)
        if u < 0:
            break
        fixed[u] = True
        for j in range(V):
            cost[j] = min(cost[j], cost[u] + adj_matrix_weight[u][j])
    return cost






if __name__ == "__main__":
    #                             to/weight
    adjacent_list_with_weight = (((1, 5), (2, 6)),
                                 ((0, 5), (4, 2)),
                                 ((0, 6), (3, 2), (5, 4)),
                                 ((2, 2), (6, 1)),
                                 ((1, 2), (5, 3), (7, 7)),
                                 ((2, 4), (4, 3), (8, 1)),
                                 ((3, 1),),
                                 ((4, 7),),
                                 ((5, 1), (9, 1)),
                                 ((8, 1),))
    cost = dijkstra(adjacent_list_with_weight)
    assert(cost == [0, 5, 6, 8, 7, 10, 9, 14, 11, 12])


    """
    - 引数として隣接行列 or CSR フォーマットの疎行列を渡して最短距離を計算させる
        null_value として存在しない辺を指定する (デフォルトは 0, 10**9 や inf を指定しよう)
    - 戻り値は各点に対する最短距離の行列 (numpy array)
        到達できない頂点に対しては inf が入る
        スタート頂点に対しては 0 が入る
    - return_predecessors = True とすると最短経路と合わせて「その経路を取った時一つ前の頂点のインデックス」を記録した行列も返る
        自身など到達できない頂点に対しては適当な負の値 (-9999 など) が入る
    - 単一始点最短経路を求めたい場合、その始点を indices = int or list として指定する。リストで複数指定したらそれだけ計算してくれる
    - デフォルトは有向グラフとして扱われる。 directed = False とすることで無向グラフとして扱うようになる (mat[i, j], mat[j, i] のうち小さい方の値を勝手に他方に fill してくれるイメージ)
    - デフォルトは重みつきとして扱われる。 unweighted = True とすることで重みなしグラフとして扱うようになる (全ての重みが 1 になるイメージ)    
    """
    import numpy as np
    import scipy.sparse.csgraph as cs
    I = float('inf')
    mat = [[I, 5, 6, I, I, I, I, I, I, I],
           [5, I, I, I, 2, I, I, I, I, I],
           [6, I, I, 2, I, 4, I, I, I, I],
           [I, I, 2, I, I, I, 1, I, I, I],
           [I, 2, I, I, I, 3, I, 7, I, I],
           [I, I, 4, I, 3, I, I, I, 1, I],
           [I, I, I, 1, I, I, I, I, I, I],
           [I, I, I, I, 7, I, I, I, I, I],
           [I, I, I, I, I, 1, I, I, I, 1],
           [I, I, I, I, I, I, I, I, 1, I]]
    G = cs.csgraph_from_dense(mat, null_value=I)
    dist, path = cs.dijkstra(G, return_predecessors=True)
    print("SciPy Power!")
    print(dist)
    print(path)
    """
    [[ 0.  5.  6.  8.  7. 10.  9. 14. 11. 12.]
    [ 5.  0.  9. 11.  2.  5. 12.  9.  6.  7.]
    [ 6.  9.  0.  2.  7.  4.  3. 14.  5.  6.]
    [ 8. 11.  2.  0.  9.  6.  1. 16.  7.  8.]
    [ 7.  2.  7.  9.  0.  3. 10.  7.  4.  5.]
    [10.  5.  4.  6.  3.  0.  7. 10.  1.  2.]
    [ 9. 12.  3.  1. 10.  7.  0. 17.  8.  9.]
    [14.  9. 14. 16.  7. 10. 17.  0. 11. 12.]
    [11.  6.  5.  7.  4.  1.  8. 11.  0.  1.]
    [12.  7.  6.  8.  5.  2.  9. 12.  1.  0.]] 

    [[-9999     0     0     2     1     2     3     4     5     8]
    [    1 -9999     5     2     1     4     3     4     5     8]
    [    2     4 -9999     2     5     2     3     4     5     8]
    [    2     4     3 -9999     5     2     3     4     5     8]
    [    1     4     5     2 -9999     4     3     4     5     8]
    [    2     4     5     2     5 -9999     3     4     5     8]
    [    2     4     3     6     5     2 -9999     4     5     8]
    [    1     4     5     2     7     4     3 -9999     5     8]
    [    2     4     5     2     5     8     3     4 -9999     8]
    [    2     4     5     2     5     8     3     4     9 -9999]]    
    """    