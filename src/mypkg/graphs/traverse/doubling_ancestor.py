"""
ダブリング

サイズ n の木に対し、ダブリングにより前処理を O(n lg n) かけて行うことで、k 個先の祖先を探索するクエリに対し O(lgk) で答えられるようにする
Q 個のクエリが飛んでくるとすると O(Q) * O(k) であった時間計算量が O(nlgn) + O(Q) * O(lgk) へと変化する

基本的には二分探索のように各ノードが
1 個先の祖先
2 個先の祖先
4 個先の祖先
...
depth 個先の祖先
を知っているように前処理を行う。(上から順に上の結果を利用していけば O(n) + O(n) + ... O(n) (depth 個) = O(nlgn) となる)


verified @ABC014D
"""


from collections import deque
from typing import Sequence


class DoublingTree:
    """
    ダブリングにより 2^k 個先の祖先の情報を獲得した根付き木

    Attributes:
        adj (list): 隣接リスト
        size (int): 頂点数
        root (int): 根のインデックス
        children (list): children[i] = (頂点 i の子のインデックスのリスト)
        ancestors (list): ancestors[i][level] = (頂点 i の 2^level 個先の祖先). level は 0 から lgN - 1 まで存在し、そのような祖先が存在しない場合 -1 が入る
    """
    def __init__(self, adj: Sequence[Sequence[int]], root: int):
        self.adj = adj
        self.size = len(adj)
        self.root = root
        self.children = [[] for _ in range(self.size)]
        self.ancestors = [[-1] * self.size.bit_length() for _ in range(self.size)]
        self._build_rooted_tree()
        self._doubling_ancestors()
    
    def _build_rooted_tree(self) -> None:
        """
        O(N) で隣接リストと根をもとに self.children および self.ancestors の親のスロットを記載する
        """
        visited = [False] * self.size
        q = deque()
        q.append(self.root)
        while q:
            u = q.popleft()
            if not visited[u]:
                visited[u] = True
                for v in self.adj[u]:
                    if not visited[v]:
                        self.children[u].append(v)
                        self.ancestors[v][0] = u
                        q.append(v)
    
    def _doubling_ancestors(self) -> None:
        """
        O(NlgN) で各ノードの self.ancestors[i][level] のスロットを記載する。
        なお、_build_rooted_tree() により self.ancestors[i][0] は登記済みであるとする。
        """
        for level in range(1, self.size.bit_length()):
            for i in range(self.size):
                if self.ancestors[i][level-1] >= 0:
                    self.ancestors[i][level] = self.ancestors[self.ancestors[i][level-1]][level-1]

    def kth_ancestor(self, i: int, k: int) -> int:
        """
        O(lgk) でノード i の k 個先の祖先のノード番号を求める (k = 0 の場合自身 i となる)
        そのような祖先がいない場合 -1 を返す
        """
        if k >= self.size:
            raise ValueError(f"DoublingTree.kth_ancestor(): k shoule be lt num of vertices. got i: {i}, k: {k} (tree size = {self.size})")
        node_ind = i
        flag_bit = 1
        for level in range(k.bit_length()):
            if node_ind < 0:
                break
            if k & flag_bit:
                node_ind = self.ancestors[node_ind][level]
            flag_bit <<= 1
        return node_ind





if __name__ == "__main__":
    # ===================================
    # 木構造の無向グラフを作成
    # 今回は深さ 3、段数 4 の完全二分木を考える
    n = 15
    adj = [[] for _ in range(n)]
    
    def connect(adj, i, j):
        adj[i].append(j)
        adj[j].append(i)
    
    for i in range(7):
        connect(adj, i, i*2+1)
        connect(adj, i, i*2+2)
    # ===================================

    doubling_tree = DoublingTree(adj, 0)
    assert (doubling_tree.children == [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [], [], [], [], [], [], [], []])
    assert(doubling_tree.ancestors == [[-1, -1, -1, -1],
                                       [0, -1, -1, -1],
                                       [0, -1, -1, -1],
                                       [1, 0, -1, -1],
                                       [1, 0, -1, -1],
                                       [2, 0, -1, -1],
                                       [2, 0, -1, -1],
                                       [3, 1, -1, -1],
                                       [3, 1, -1, -1],
                                       [4, 1, -1, -1],
                                       [4, 1, -1, -1],
                                       [5, 2, -1, -1],
                                       [5, 2, -1, -1],
                                       [6, 2, -1, -1],
                                       [6, 2, -1, -1]])
    
    # 1 段目 (最初)
    assert(doubling_tree.kth_ancestor(0, 0) == 0)
    assert(doubling_tree.kth_ancestor(0, 1) == -1)    # オーバーするとき
    assert(doubling_tree.kth_ancestor(0, 2) == -1)    # オーバーするとき
    # 2 段目
    assert(doubling_tree.kth_ancestor(1, 0) == 1)
    assert(doubling_tree.kth_ancestor(1, 1) == 0)
    assert(doubling_tree.kth_ancestor(1, 2) == -1)
    assert(doubling_tree.kth_ancestor(2, 0) == 2)
    assert(doubling_tree.kth_ancestor(2, 1) == 0)
    assert(doubling_tree.kth_ancestor(2, 2) == -1)
    # 3 段目
    assert(doubling_tree.kth_ancestor(9, 0) == 9)
    assert(doubling_tree.kth_ancestor(9, 1) == 4)
    assert(doubling_tree.kth_ancestor(9, 2) == 1)
    assert(doubling_tree.kth_ancestor(9, 3) == 0)
    assert(doubling_tree.kth_ancestor(9, 4) == -1)
    # 4 段目 (最後)
    assert(doubling_tree.kth_ancestor(14, 0) == 14)
    assert(doubling_tree.kth_ancestor(14, 1) == 6)
    assert(doubling_tree.kth_ancestor(14, 2) == 2)
    assert(doubling_tree.kth_ancestor(14, 3) == 0)
    assert(doubling_tree.kth_ancestor(14, 4) == -1)

    print(" * assertion test ok * ")

            