"""
ダブリング (kth_ancestor()) を用いて最小共通祖先 (least common ancestor, LCA) を求める 
(各クエリに対し O(lgn), 前処理はダブリングに O(nlgn), dist に O(n))

algorithm

O(n) で root から DFS を行い各ノードに対し root からの距離 dist を求める
O(nlgn) でダブリングを行い各ノードについて 2^i 個先の祖先がわかるようにする
LCA を求めるノードのペア u, v とする (dist(u) >= dist (v)) とする
|dist(u)-dist(v)| だけ u は親を遡ることにより dist(u1) = dist(v) なる u1 を発見可能。v はそのままでこれを v1 とする。
u1, v1 の ancestors を見るとあるところまでは不一致だがあるところから一致するはずである (branch は合流するので)。不一致しているところまで遡る。
u2, v2 についても同様に処理を行う。ancestors[0] が一致してしまうような u, v になった場合その親が最小共通祖先である。


verified @ABC014D
"""



from collections import deque
from typing import Sequence, List


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
        self.dist_from_root = [-1] * self.size
        self._build_rooted_tree()
        self._doubling_ancestors()
    
    def _build_rooted_tree(self) -> None:
        """
        O(N) で隣接リストと根をもとに self.children および self.ancestors の親のスロットを記載する
        self.dist_from_root を記録する
        """
        q = deque()
        q.append((self.root, 0))
        while q:
            u, dist = q.popleft()
            if self.dist_from_root[u] < 0:
                self.dist_from_root[u] = dist
                for v in self.adj[u]:
                    if self.dist_from_root[v] < 0:
                        self.children[u].append(v)
                        self.ancestors[v][0] = u
                        q.append((v, dist+1))
    
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



    def calc_LCA(self, u: int, v: int) -> int:
        """
        2 つの node を受け取り、その最小共通祖先を求める。(O(lgn))
        なお、各ノードのルートからの距離と k 祖先は計算ずみであるとする。
        Args:
            u, v (int)
        Returns:
            lca (int)
        """
        # u は v と同じ深さかより深いノードとする
        if self.dist_from_root[u] < self.dist_from_root[v]:
            u, v = v, u
        diff = self.dist_from_root[u] - self.dist_from_root[v]
        u1 = self.kth_ancestor(u, diff)
        v1 = v
        # そもそも同じ枝に乗っていた場合、深さを合わせるだけで一致する
        if u1 == v1:
            return u1
        # 別の枝に乗っていた場合
        while self.ancestors[u1][0] != self.ancestors[v1][0]:
            for level in range(self.size.bit_length()):
                if self.ancestors[u1][level] == self.ancestors[v1][level]:
                    # 合流せず遡れるギリギリまで遡る。
                    # u1, v1 の深さはそろっているため同じレベルで両方初めて -1 を引くことになる。ancestors[u1][level-1] が -1 となることはない
                    u1 = self.ancestors[u1][level-1]
                    v1 = self.ancestors[v1][level-1]
                    break
        return self.ancestors[u1][0]




if __name__ == "__main__":
    """
                        0
            1                        2
        3    4   5                   6
      7   8      9           10   11    12    13
    14 15     16   17      18 19  20    21   22 23
    24 25         26 27    28          29 30 31 32
    という木を想定する。
    """
    n = 33
    adj = [[] for _ in range(n)]

    parent_child_ind_list = ((0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 7), (3, 8), (5, 9), (6, 10), (6, 11), (6, 12), (6, 13),
                            (7, 14), (7, 15), (9, 16), (9, 17), (10, 18), (10, 19), (11, 20), (12, 21), (13, 22), (13, 23),
                            (14, 24), (15, 25), (17, 26), (17, 27), (18, 28), (21, 29), (21, 30), (22, 31), (23, 32))
    
    def connect(adj, i, j):
        adj[i].append(j)
        adj[j].append(i)

    for p, c in parent_child_ind_list:
        connect(adj, p, c)
    # =============================================

    doubling_tree = DoublingTree(adj, 0)

    # 距離のチェック
    assert(doubling_tree.dist_from_root[0] == 0)
    assert(doubling_tree.dist_from_root[1] == 1)
    assert(doubling_tree.dist_from_root[2] == 1)
    assert(doubling_tree.dist_from_root[3] == 2)
    assert(doubling_tree.dist_from_root[4] == 2)
    assert(doubling_tree.dist_from_root[8] == 3)
    assert(doubling_tree.dist_from_root[21] == 4)
    assert(doubling_tree.dist_from_root[32] == 5)
    print("- test for dist_from_root passed.")


    # k 祖先のチェック
    # 1 段目 (最初)
    assert(doubling_tree.kth_ancestor(0, 0) == 0)
    assert(doubling_tree.kth_ancestor(0, 1) == -1)
    assert(doubling_tree.kth_ancestor(0, 2) == -1)
    # 2 段目
    assert(doubling_tree.kth_ancestor(1, 0) == 1)
    assert(doubling_tree.kth_ancestor(1, 1) == 0)
    assert(doubling_tree.kth_ancestor(1, 2) == -1)
    assert(doubling_tree.kth_ancestor(1, 3) == -1)
    assert(doubling_tree.kth_ancestor(2, 0) == 2)
    assert(doubling_tree.kth_ancestor(2, 1) == 0)
    assert(doubling_tree.kth_ancestor(2, 2) == -1)
    assert(doubling_tree.kth_ancestor(2, 3) == -1)
    # 3 段目
    assert(doubling_tree.kth_ancestor(3, 0) == 3)
    assert(doubling_tree.kth_ancestor(3, 1) == 1)
    assert(doubling_tree.kth_ancestor(3, 2) == 0)
    assert(doubling_tree.kth_ancestor(3, 3) == -1)
    assert(doubling_tree.kth_ancestor(5, 0) == 5)
    assert(doubling_tree.kth_ancestor(5, 1) == 1)
    assert(doubling_tree.kth_ancestor(5, 2) == 0)
    assert(doubling_tree.kth_ancestor(5, 3) == -1)
    # 4 段目
    assert(doubling_tree.kth_ancestor(8, 0) == 8)
    assert(doubling_tree.kth_ancestor(8, 1) == 3)
    assert(doubling_tree.kth_ancestor(8, 2) == 1)
    assert(doubling_tree.kth_ancestor(8, 3) == 0)
    assert(doubling_tree.kth_ancestor(8, 4) == -1)
    # 5 段目
    assert(doubling_tree.kth_ancestor(21, 0) == 21)
    assert(doubling_tree.kth_ancestor(21, 1) == 12)
    assert(doubling_tree.kth_ancestor(21, 2) == 6)
    assert(doubling_tree.kth_ancestor(21, 3) == 2)
    assert(doubling_tree.kth_ancestor(21, 4) == 0)
    assert(doubling_tree.kth_ancestor(21, 5) == -1)
    # 6 段目 (最後)
    assert(doubling_tree.kth_ancestor(32, 0) == 32)
    assert(doubling_tree.kth_ancestor(32, 1) == 23)
    assert(doubling_tree.kth_ancestor(32, 2) == 13)
    assert(doubling_tree.kth_ancestor(32, 3) == 6)
    assert(doubling_tree.kth_ancestor(32, 4) == 2)
    assert(doubling_tree.kth_ancestor(32, 5) == 0)
    assert(doubling_tree.kth_ancestor(32, 6) == -1)
    print("- test for kth_ancestor() passed.")

    # LCA のチェック
    # same branch
    assert(doubling_tree.calc_LCA(0, 1) == 0)
    assert(doubling_tree.calc_LCA(0, 30) == 0)
    assert(doubling_tree.calc_LCA(1, 3) == 1)
    # diffrent branch, same depth
    assert(doubling_tree.calc_LCA(1, 2) == 0)
    assert(doubling_tree.calc_LCA(4, 5) == 1)
    assert(doubling_tree.calc_LCA(18, 20) == 6)
    assert(doubling_tree.calc_LCA(31, 32) == 13)
    # diffrent branch, different depth
    assert(doubling_tree.calc_LCA(3, 10) == 0)
    assert(doubling_tree.calc_LCA(4, 8) == 1)
    assert(doubling_tree.calc_LCA(14, 16) == 1)
    assert(doubling_tree.calc_LCA(10, 21) == 6)
    print("- test for calc_LCA() passed.")

    print(" * assertion test ok * ")
