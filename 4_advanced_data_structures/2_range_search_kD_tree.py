"""
kD tree (range search)

query
d 次元状の空間の点の集合に対し与えられた領域に含まれる点を列挙する
点の数 n として、kD tree の構築に O(n*(logn)^2) (O(nlgn) のソートを木の高さ lgn 回行うので)
サーチで引っかかる要素数 k として、1 回のサーチに O(n^(1-1/d) + k) 
だけかかることが知られている。

algorithm
1D: 普通の BST を作成。現在のノードがレンジに含まれるか、左側の部分木が含まれる可能性はあるか、右側の部分木が含まれる可能性はあるかを再帰的に調べるのみ
2D: depth ごとに大小関係を調査する key を x 座標、 y 座標と交互に変更する BST を作成。同様に調べる。
"""


class OneDimNode:
    def __init__(self, x=None, parent=None, left=None, right=None):
        self.x = x
        self.parent = parent
        self.left = left
        self.right = right
        self.flag = True

class OneDimTree:
    def __init__(self):
        self.nil = OneDimNode()
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.root = self.nil
    
    def traverse(self, node=None):
        if node is None:
            node = self.root
        if node != self.nil:
            self.traverse(node=node.left)
            print(node.x, end=' ')
            self.traverse(node=node.right)
        
    def insert(self, x):
        trailer = self.nil
        pos = self.root
        while pos != self.nil:
            trailer = pos
            if x < pos.x:
                pos = pos.left
            elif pos.x < x:
                pos = pos.right
            else:
                pos.flag ^= pos.flag
                pos = pos.left if pos.flag else pos.right
        inserted_node = OneDimNode(x, trailer, self.nil, self.nil)
        # tree is empty
        if trailer == self.nil:
            self.root = inserted_node
        elif x < trailer.x or (x == trailer.x and trailer.flag):
            trailer.left = inserted_node
        else:
            trailer.right = inserted_node
    
    def one_dim_search(self, sx, tx, node=None):
        buf = []
        if node is None:
            node = self.root
        if node.left != self.nil and node.left.x <= tx:
            buf += self.one_dim_search(sx, tx, node.left)
        if sx <= node.x <= tx:
            buf.append(node.x)
        if node.right != self.nil and sx <= node.right.x:
            buf += self.one_dim_search(sx, tx, node.right)
        return buf



class TwoDimNode:
    def __init__(self, x=None, y=None, parent=None, left=None, right=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.left = left
        self.right = right
        self.flag = True

class TwoDimTree:
    def __init__(self):
        self.nil = TwoDimNode()
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.root = self.nil
    
    def preorder_traverse(self, node=None):
        if node is None:
            node = self.root
        if node != self.nil:
            print(f"({node.x},{node.y})", end=' ')
            self.preorder_traverse(node=node.left)
            self.preorder_traverse(node=node.right)
        
    def insert(self, x, y):
        trailer = self.nil
        pos = self.root
        depth = 0
        while pos != self.nil:
            trailer = pos
            if depth % 2 == 0:
                k, pos_k = x, pos.x
            else:
                k, pos_k = y, pos.y
            if k < pos_k:
                pos = pos.left
            elif pos_k < k:
                pos = pos.right
            else:
                pos.flag ^= pos.flag
                pos = pos.left if pos.flag else pos.right
            depth += 1
        inserted_node = TwoDimNode(x, y, trailer, self.nil, self.nil)
        # trailer の depth
        depth -= 1
        if depth % 2 == 0:
            k, trailer_k = x, trailer.x
        else:
            k, trailer_k = y, trailer.y
        # tree is empty
        if trailer == self.nil:
            self.root = inserted_node
        elif k < trailer_k or (k == trailer_k and trailer.flag):
            trailer.left = inserted_node
        else:
            trailer.right = inserted_node
    
    def two_dim_search(self, sx, tx, sy, ty, node=None, depth=0):
        buf = []
        if node is None:
            node = self.root
        # print(f"{node.x} {node.y}")
        if depth % 2 == 0:
            if node.left != self.nil and node.left.x <= tx:
                buf += self.two_dim_search(sx, tx, sy, ty, node.left, depth+1)
            if sx <= node.x <= tx and sy <= node.y <= ty:
                buf.append((node.x, node.y))
            if node.right != self.nil and sx <= node.right.x:
                buf += self.two_dim_search(sx, tx, sy, ty, node.right, depth+1)
        else:
            if node.left != self.nil and node.left.y <= ty:
                buf += self.two_dim_search(sx, tx, sy, ty, node.left, depth+1)
            if sx <= node.x <= tx and sy <= node.y <= ty:
                buf.append((node.x, node.y))
            if node.right != self.nil and sy <= node.right.y:
                buf += self.two_dim_search(sx, tx, sy, ty, node.right, depth+1)
        return buf


if __name__ == "__main__":
    import random
    print("\none dimentional kD tree")
    tree_1 = OneDimTree()
    L_1 = [random.randint(0, 20) for _ in range(15)]
    print(L_1)
    for x in L_1:
        tree_1.insert(x)
    tree_1.traverse()
    print('')
    for _ in range(5):
        sx = random.randint(0, 20)
        tx = random.randint(0, 20)
        sx, tx = min(sx, tx), max(sx, tx)
        print(f"range search {sx} ~ {tx}: {tree_1.one_dim_search(sx, tx)}")

    print("\ntwo dimentional kD tree")
    tree_2 = TwoDimTree()
    L_2 = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(10)]
    print(L_2)
    for x, y in L_2:
        tree_2.insert(x, y)
    tree_2.preorder_traverse()
    print('')
    for _ in range(5):
        sx, tx, sy, ty = [random.randint(0, 20) for _ in range(4)]
        sx, tx = min(sx, tx), max(sx, tx)
        sy, ty = min(sy, ty), max(sy, ty)
        print(f"range search ({sx},{sy}) ~ ({tx},{ty}): {tree_2.two_dim_search(sx, tx, sy, ty)}")
    print(f"range search (0,0) ~ (20,20): {tree_2.two_dim_search(0, 20, 0, 20)}")
