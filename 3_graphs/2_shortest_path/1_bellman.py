"""
<Algorithm Introduction p.248-251>
Bellman-Ford 法 (O(V * E))
負サイクルを含まない一般の重みつき有向グラフについて、ある頂点から全頂点について最短距離を求める

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


class NegativeLoopError(Exception):
    pass


class Edge:
    def __init__(self, here, to, weight):
        self.here = here
        self.to = to
        self.weight = weight



def bellman(edges, start=0):
    'start から全頂点までの最短コストを計算して返す。辿り着けぬ場合は inf が出力される。負サイクルがある場合 NegativeLoopError があげられる'
    # E = len(edges)
    V = max(map(lambda x: max(x.here, x.to), edges)) + 1    # 0 to この値なので
    cost = [float('inf')] * V
    cost[start] = 0
    updated = True
    i = 1
    while i <= V and updated:
        updated = False
        for e in edges:
            possible_value = cost[e.here]+e.weight
            if cost[e.to] > possible_value:
                cost[e.to] = possible_value
                updated = True
        i += 1
    if i == V:
        raise NegativeLoopError
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

    cost = bellman(edge_list)
    print(cost)    # [0, 5, 4, 6, 3, 0, 7, 10, 1, 0]