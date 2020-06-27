"""
<Algorithm Introduction vol.2 p.248-251>
Bellman-Ford 法 (O(V * E))
負サイクルを含まない一般の重みつき有向グラフについて、ある頂点から全頂点について最短距離を求める


<algorithm>
start 以外の全ての頂点のコストを inf, start を 0 に設定する
E 個存在する各エッジ uv に対し cost[v] = min(cost[v], cost[u]+w[uv]) によりコストを緩和する

これを更新がある限り繰り返す
-> 負サイクルがない場合高々 |v-1| 回で更新がなくなることが証明できる。逆に v 回目にも更新が行われる場合は負サイクルを含む

帰納法で証明
i 回目のループについて
1. cost[v]=inf->start から高々 i 本の辺を通るのでは辿り着けぬ
   cost[v]=val->start から高々 i 本の辺を通った何らかの経路の合計コストに等しい
2. 高々 i 個の辺を通って start~v へたどり着けるとき、 cost[v] は高々 i 本の辺を通ったときの最短経路に等しい
なる性質を満たしていることを示す
1 については自明
2 について
基底は示されている
k 回目のループで cost[u1]...cost[uj] (u is adjacent to v) は高々 k 本の辺を start~u で通ったときの最短経路となっていると仮定
このとき k+1 回目のループで cost[v] は高々 k+1 本の辺を start~v で通ったときの最短経路となる
以上より示された
この示された 1 2 の性質、負サイクルがない時頂点数 v の時の頂点間の最短経路に同一頂点が複数出現することはないため高々 |v-1| 本の辺を通った時の最短経路が分かれば良いことを
併せて考えると、 |v-1| 回のループで更新がストップすることがわかる。
"""

from typing import Sequence, List, Union

Num = Union[int, float]


class NegativeCycleError(Exception):
    pass


class Edge:
    def __init__(self, here: int, to: int, weight: Num):
        self.here = here
        self.to = to
        self.weight = weight



def bellman(edges: Sequence[Edge], V: int, start: int=0) -> List[int]:
    """
    start から全頂点までの最短コストを計算して返す。辿り着けぬ場合は inf が出力される。(O(V * E))
    負サイクルがある場合 NegativeCycleError があげられる
    """
    cost = [float('inf')] * V
    cost[start] = 0
    updated = True
    i = 0    # 何回ループを回ったか
    while i < V and updated:
        updated = False
        for e in edges:
            possible_value = cost[e.here]+e.weight
            if cost[e.to] > possible_value:
                cost[e.to] = possible_value
                updated = True
        i += 1
    if i == V and updated:
        raise NegativeCycleError
    else:
        return cost



if __name__ == "__main__":
    from itertools import starmap
    # here, to, cost
    t = ((0, 1, 5),
         (1, 4, -2),
         (4, 5, -3),
         (4, 7, 7),
         (5, 2, 4),
         (5, 8, 1),
         (2, 3, 2),
         (8, 9, -1),
         (3, 6, 1),
         (2, 0, 6))
    edge_list = list(starmap(Edge, t))

    cost = bellman(edge_list, V=10, start=0)
    assert(cost ==  [0, 5, 4, 6, 3, 0, 7, 10, 1, 0])


    # scipy の bellman_ford と比較
    """
    - 引数として隣接行列 or CSR フォーマットの疎行列を渡して最短距離を計算させる
        null_value として存在しない辺を指定する (デフォルトは 0, 10**9 や inf を指定しよう)
    - 戻り値は各点に対する最短距離の行列 (numpy array) (各値は float になっていることに注意)
        到達できない頂点に対しては inf が入る
    - return_predecessors = True とすると最短経路と合わせて「その経路を取った時一つ前の頂点のインデックス」を記録した行列も返る
        到達できない頂点に対しては適当な負の値 (-9999 など) が入る
    - 単一始点最短経路を求めたい場合、その始点を indices = int or list として指定する。リストで複数指定したらそれだけ計算してくれる
    - デフォルトは有向グラフとして扱われる。 directed = False とすることで無向グラフとして扱うようになる (mat[i, j], mat[j, i] のうち小さい方の値を勝手に他方に fill してくれるイメージ)
    - デフォルトは重みつきとして扱われる。 unweighted = True とすることで重みなしグラフとして扱うようになる (全ての重みが 1 になるイメージ)
    """
    import numpy as np
    import scipy.sparse.csgraph as cs
    inf = float('inf')
    mat = np.full((10, 10), inf)
    mat[0, 1] = 5
    mat[1, 4] = -2
    mat[2, 0] = 6
    mat[2, 3] = 2
    mat[3, 6] = 1
    mat[4, 5] = -3
    mat[4, 7] = 7
    mat[5, 2] = 4
    mat[5, 8] = 1
    mat[8, 9] = -1
    G = cs.csgraph_from_dense(mat, null_value=inf)
    dist, path = cs.bellman_ford(G, return_predecessors=True)
    print("SciPy Power!")
    print(dist)
    print(path)
    """
    [[ 0.  5.  4.  6.  3.  0.  7. 10.  1.  0.]
    [ 5.  0. -1.  1. -2. -5.  2.  5. -4. -5.]
    [ 6. 11.  0.  2.  9.  6.  3. 16.  7.  6.]
    [inf inf inf  0. inf inf  1. inf inf inf]
    [ 7. 12.  1.  3.  0. -3.  4.  7. -2. -3.]
    [10. 15.  4.  6. 13.  0.  7. 20.  1.  0.]
    [inf inf inf inf inf inf  0. inf inf inf]
    [inf inf inf inf inf inf inf  0. inf inf]
    [inf inf inf inf inf inf inf inf  0. -1.]
    [inf inf inf inf inf inf inf inf inf  0.]]

    [[-9999     0     5     2     1     4     3     4     5     8]
    [    2 -9999     5     2     1     4     3     4     5     8]
    [    2     0 -9999     2     1     4     3     4     5     8]
    [-9999 -9999 -9999 -9999 -9999 -9999     3 -9999 -9999 -9999]
    [    2     0     5     2 -9999     4     3     4     5     8]
    [    2     0     5     2     1 -9999     3     4     5     8]
    [-9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999]
    [-9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999]
    [-9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999     8]
    [-9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999 -9999]]
    """





