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
"""


from math import log2
class Node:
    def __init__(self, val, parent=None, children=[]):
        self.data = val
        self.ancestors = [parent] if parent else []    # デフォルト値 (None) の時は [] となる
        assert(isinstance(children, list))
        self.children = children    # デフォルト値の時は [] になる

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
        (ダブリング) 全ノードに対し 2^i 個先の祖先を .ancestors[i] に記録していく
        """
        for i in range(1, int(log2(self.size))+1):
            stack = [self.root]
            while stack:
                u = stack.pop()
                u.ancestors.append(u.kth_ancestor(pow(2, i)))
                for child in u.children:
                    if child != NIL:
                        stack.append(child)


if __name__ == "__main__":
    # 今回は深さ 4、段数 3 の完全二分木を考える
    depth = 4
    size = 2 ** depth - 1
    # ノードをリストの形で管理。普通は親子関係の入力がくるが今回は完全二分木なので親、子のインデックスが計算可能であるためそれを使ってポインタを繋ぐ
    # 木の準備をしているだけ
    node_list = []
    for i in range(size):
        if (i - 1) // 2 < 0:
            node_list.append(Node(i, NIL))
        else:
            node_list.append(Node(i, node_list[(i-1)//2]))
    for i in range(size):
        if 2 * i + 2 > size - 1:
            node_list[i].children.append(NIL)
        else:
            node_list[i].children.append(node_list[2 * i + 1])
            node_list[i].children.append(node_list[2 * i + 2])
    

    # ==================================================
    # 満を辞して tree 作成。ダブリングを行う。
    tree = Tree(node_list[0], size)
    tree.doubling_ancestors()
    
    # 1 段目 (最初)
    assert(node_list[0].kth_ancestor(0) == node_list[0])
    assert(node_list[0].kth_ancestor(1) == NIL)    # 実際にはここが root だが親には NIL がいることになっている
    assert(node_list[0].kth_ancestor(2) == NIL)    # オーバーするとき
    # 2 段目
    assert(node_list[1].kth_ancestor(0) == node_list[1])
    assert(node_list[1].kth_ancestor(1) == node_list[0])
    assert(node_list[1].kth_ancestor(2) == NIL)
    assert(node_list[2].kth_ancestor(0) == node_list[2])
    assert(node_list[2].kth_ancestor(1) == node_list[0])
    assert(node_list[2].kth_ancestor(2) == NIL)
    # 3 段目
    assert(node_list[9].kth_ancestor(0) == node_list[9])
    assert(node_list[9].kth_ancestor(1) == node_list[4])
    assert(node_list[9].kth_ancestor(2) == node_list[1])
    assert(node_list[9].kth_ancestor(3) == node_list[0])
    assert(node_list[9].kth_ancestor(4) == NIL)
    # 4 段目 (最後)
    assert(node_list[14].kth_ancestor(0) == node_list[14])
    assert(node_list[14].kth_ancestor(1) == node_list[6])
    assert(node_list[14].kth_ancestor(2) == node_list[2])
    assert(node_list[14].kth_ancestor(3) == node_list[0])
    assert(node_list[14].kth_ancestor(4) == NIL)

    print(" * assertion test ok * ")

            