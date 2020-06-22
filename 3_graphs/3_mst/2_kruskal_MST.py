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


class UnionFindTree:
    def __init__(self, num_of_elm: int):
        self.n = num_of_elm
        self.table = [i for i in range(self.n)]
        self.rank = [0] * self.n
        self.group_size = [1] * self.n
    
    def _find_set(self, x: int):
        parent = self.table[x]
        if x == parent:
            return x
        else:
            root = self._find_set(parent)
            # 経路圧縮
            self.table[x] = root
            return root
    
    def is_same(self, x: int, y: int) -> bool:
        return self._find_set(x) == self._find_set(y)

    def union(self, x: int, y: int) -> bool:
        shallow_root = self._find_set(x)
        deep_root = self._find_set(y)
        if self.rank[shallow_root] > self.rank[deep_root]:
            shallow_root, deep_root = deep_root, shallow_root
        # そもそも同一グループだった時
        if shallow_root == deep_root:
            return False
        # グループが異なるので union
        else:
            self.table[shallow_root] = deep_root
            self.group_size[deep_root] += self.group_size[shallow_root]
            # 深さが等しかったときはつけ加えられた側の rank をインクリメントする
            if self.rank[shallow_root] == self.rank[deep_root]:
                self.rank[deep_root] += 1
            return True


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


