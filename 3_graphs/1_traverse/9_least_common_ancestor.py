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
"""


from math import log2
class Node:
    def __init__(self, val, dist_from_root=0, parent=None, children=[]):
        self.data = val
        self.dist_from_root = dist_from_root
        self.ancestors = [parent] if parent else []    # デフォルト値 (None) の時は [] となる
        assert(isinstance(children, list))
        self.children = children   # デフォルト値の時は [] になる
    
    def kth_ancestor(self, k):
        """
        k 個先の祖先の Node を返す
        ancestors は [2^0個先の祖先, 2^1個先の祖先, ..., 2^lgn個先の祖先] が記録されているので一番探索区間を縮められるものを選択し、再帰的に探索する。
        Args:
            k (int)
        Returns:
            Node
        """
        if k == 0:
            return self
        if self == NIL:
            return NIL
        power_of_two = int(log2(k))
        ind = min(len(self.ancestors) - 1, power_of_two)
        return self.ancestors[ind].kth_ancestor(k - pow(2, ind))


NIL = Node(None)
NIL.ancestors = [NIL]
NIL.children = [NIL]


class Tree:
    def __init__(self, root, size):
        self.root = root
        self.size = size

    def doubling_ancestors(self):
        """
        (ダブリング) 全ノードに対し 2^i 個先の祖先を .ancestors[i] に記録していく O(n) * O(lgn)
        """
        for i in range(1, int(log2(self.size))+1):
            stack = [self.root]
            while stack:
                u = stack.pop()
                u.ancestors.append(u.kth_ancestor(pow(2, i)))
                for child in u.children:
                    if child != NIL:
                        stack.append(child)
    
    def memorizing_dist(self, current_node=None, dist=0):
        """
        (距離の記録) 全ノードに対し root からの距離を .dist_from_root に記録していく O(n)
        Args:
            current_node (Node): 再帰の時にこれを現在のノードに指定する。ユーザーが呼び出す時は指定しない。(デフォルト値の時は current_node が self.root になってくれる)   
            dist (int): 再帰の時にこれを現在の root からの距離に指定する。ユーザーが呼び出す時は指定しない。(デフォルト値の時は current_node が self.root になってくれる)  
        """
        if current_node is None and dist == 0:
            current_node = self.root
        current_node.dist_from_root = dist
        for child in current_node.children:
            if child != NIL:
                self.memorizing_dist(current_node=child, dist=dist+1)



def calc_LCA(u, v):
    """
    2 つの node を受け取り、その最小共通祖先を求める。(O(lgn))
    なお、各ノードのルートからの距離と k 祖先は計算ずみであるとする。
    Args:
        u (Node)
        v (Node)
    Returns:
        Node
    """
    # u は v と同じ深さかより深いノードとする
    if u.dist_from_root < v.dist_from_root:
        u, v = v, u
    diff = u.dist_from_root - v.dist_from_root
    u1 = u.kth_ancestor(diff)
    v1 = v
    # そもそも同じ枝上に乗っていた場合
    if u1 == v1:
        return u1
    # 別の枝に乗っていた場合
    while u1.ancestors[0] != v1.ancestors[0]:
        assert(len(u1.ancestors) == len(v1.ancestors))
        n = len(u1.ancestors)
        for i in range(n):
            if u1.ancestors[i] == v1.ancestors[i]:
                # 合流せず遡れるギリギリまで遡る
                u1 = u1.ancestors[i-1]
                v1 = v1.ancestors[i-1]
                break
    return u1.ancestors[0]

                        

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
    parent_child_ind_list = ((0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 7), (3, 8), (5, 9), (6, 10), (6, 11), (6, 12), (6, 13),
                            (7, 14), (7, 15), (9, 16), (9, 17), (10, 18), (10, 19), (11, 20), (12, 21), (13, 22), (13, 23),
                            (14, 24), (15, 25), (17, 26), (17, 27), (18, 28), (21, 29), (21, 30), (22, 31), (23, 32))
    size = 33
    # ノードをリストの形で管理。普通は親子関係の入力がくるが今回は完全二分木なので親、子のインデックスが計算可能であるためそれを使ってポインタを繋ぐ
    node_list = [Node(i, dist_from_root=0, parent=None, children=[NIL]) for i in range(size)]
    node_list[0].ancestors = [NIL]
    # 親子関係の記録
    for parent, child in parent_child_ind_list:
        if node_list[parent].children == [NIL]:
            node_list[parent].children.pop()
        node_list[parent].children.append(node_list[child])
        node_list[child].ancestors.append(node_list[parent])
    
    # =============================================
    # 満を辞して tree 作成。ダブリングと距離のメモを行う。
    tree = Tree(node_list[0], size)
    tree.memorizing_dist()
    tree.doubling_ancestors()

    # 距離と k 祖先のチェック
    # 1 段目 (最初)
    assert(node_list[0].dist_from_root == 0)
    assert(node_list[0].kth_ancestor(0) == node_list[0])
    assert(node_list[0].kth_ancestor(1) == NIL)
    assert(node_list[0].kth_ancestor(2) == NIL)
    # 2 段目
    assert(node_list[1].dist_from_root == 1)
    assert(node_list[1].kth_ancestor(0) == node_list[1])
    assert(node_list[1].kth_ancestor(1) == node_list[0])
    assert(node_list[1].kth_ancestor(2) == NIL)
    assert(node_list[1].kth_ancestor(3) == NIL)
    assert(node_list[2].dist_from_root == 1)
    assert(node_list[2].kth_ancestor(0) == node_list[2])
    assert(node_list[2].kth_ancestor(1) == node_list[0])
    assert(node_list[2].kth_ancestor(2) == NIL)
    assert(node_list[2].kth_ancestor(3) == NIL)
    # 3 段目
    assert(node_list[3].dist_from_root == 2)
    assert(node_list[3].kth_ancestor(0) == node_list[3])
    assert(node_list[3].kth_ancestor(1) == node_list[1])
    assert(node_list[3].kth_ancestor(2) == node_list[0])
    assert(node_list[3].kth_ancestor(3) == NIL)
    assert(node_list[3].dist_from_root == 2)
    assert(node_list[4].kth_ancestor(0) == node_list[4])
    assert(node_list[4].kth_ancestor(1) == node_list[1])
    assert(node_list[4].kth_ancestor(2) == node_list[0])
    assert(node_list[4].kth_ancestor(3) == NIL)
    # 4 段目
    assert(node_list[8].dist_from_root == 3)
    assert(node_list[8].kth_ancestor(0) == node_list[8])
    assert(node_list[8].kth_ancestor(1) == node_list[3])
    assert(node_list[8].kth_ancestor(2) == node_list[1])
    assert(node_list[8].kth_ancestor(3) == node_list[0])
    assert(node_list[8].kth_ancestor(4) == NIL)
    # 5 段目
    assert(node_list[21].dist_from_root == 4)
    assert(node_list[21].kth_ancestor(0) == node_list[21])
    assert(node_list[21].kth_ancestor(1) == node_list[12])
    assert(node_list[21].kth_ancestor(2) == node_list[6])
    assert(node_list[21].kth_ancestor(3) == node_list[2])
    assert(node_list[21].kth_ancestor(4) == node_list[0])
    assert(node_list[21].kth_ancestor(5) == NIL)
    # 6 段目 (最後)
    assert(node_list[32].dist_from_root == 5)
    assert(node_list[32].kth_ancestor(0) == node_list[32])
    assert(node_list[32].kth_ancestor(1) == node_list[23])
    assert(node_list[32].kth_ancestor(2) == node_list[13])
    assert(node_list[32].kth_ancestor(3) == node_list[6])
    assert(node_list[32].kth_ancestor(4) == node_list[2])
    assert(node_list[32].kth_ancestor(5) == node_list[0])    
    assert(node_list[32].kth_ancestor(6) == NIL)  

    # LCA のチェック
    assert(calc_LCA(node_list[0], node_list[1]) == node_list[0])
    assert(calc_LCA(node_list[0], node_list[30]) == node_list[0])
    assert(calc_LCA(node_list[1], node_list[2]) == node_list[0])
    assert(calc_LCA(node_list[1], node_list[3]) == node_list[1])
    assert(calc_LCA(node_list[3], node_list[10]) == node_list[0])
    assert(calc_LCA(node_list[4], node_list[8]) == node_list[1])
    assert(calc_LCA(node_list[14], node_list[16]) == node_list[1])
    assert(calc_LCA(node_list[10], node_list[21]) == node_list[6])

    print(" * assertion test ok * ")
