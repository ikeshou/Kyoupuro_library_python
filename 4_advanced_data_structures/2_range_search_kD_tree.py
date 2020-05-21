"""
多次元データを扱うための二分探索木である kD tree (一次元、二次元まで実装)
range search なる区間幅を指定してそれに含まれるデータを探索するクエリを O(n) で捌くことができる


query
d 次元状の空間の点の集合に対し与えられた領域に含まれる点を列挙する
点の数 n として、kD tree の構築に O(n*(logn)^2) (O(nlgn) のソートを木の高さ lgn 回行うので)
サーチで引っかかる要素数 k として、1 回のサーチに O(n^(1-1/d) + k) 
だけかかることが知られている。

algorithm
1D: 普通の BST を作成。現在のノードがレンジに含まれるか、左側の部分木が含まれる可能性はあるか、右側の部分木が含まれる可能性はあるかを再帰的に調べるのみ
2D: depth ごとに大小関係を調査する key を x 座標、 y 座標と交互に変更する BST を作成。同様に調べる。
    (root を depth = 0 として、depth % 2 == 0 のノードでは x 座標で、1 のノードでは  y 座標で比較を行う)
    (一致していた場合 最初は右に振り分け以降は前回と逆方向に振り分ける)

verified @ABC045_D
"""


class OneDimNode:
    def __init__(self, x=None, parent=None, left=None, right=None):
        """
        1 次元二分探索木のためのノード
        """
        self.x = x
        self.parent = parent
        self.left = left
        self.right = right
        self.flag = True

class OneDimTree:
    def __init__(self, points=[]):
        """
        1 次元二分探索木 (kD tree) を作成する
        """
        # nil の設定
        self.nil = OneDimNode()
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        # root の設定
        self.root = self.nil
        # もし予め一次元の点の集合が与えられるのならバランスする形で kD tree を構築する
        self._balance_insert(sorted(points))
    
    def _balance_insert(self, seq):
        # seq はソートずみであるとする (1 次元の場合ソートするキーを変える必要がないので 1 回ですむ)
        # 毎回中央値をとって insert すれば平衡になる
        if seq:
            mid = len(seq) // 2
            self.insert(seq[mid])
            self._balance_insert(seq[:mid])
            self._balance_insert(seq[mid+1:])

    
    def traverse(self, node=None):
        node = self.root if node is None else node
        if node != self.nil:
            self.traverse(node=node.left)
            print(node.x, end=' ')
            self.traverse(node=node.right)
        
    def insert(self, x):
        """
        kD tree に値が x であるノードを O(depth) で挿入する
        (コンストラクタで生成した kD tree は平衡であることが保証されるが、insert により生成した部分の平衡性は保証されないことに注意)
        """
        trailer = self.nil    # x を挿入するべき nil の一つ前のノードを保存するトレーラポインタ
        pos = self.root    # x を挿入するべき nil の場所を探す
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
        # どこかのノードの子供の位置に挿入する時
        elif x < trailer.x or (x == trailer.x and trailer.flag):
            trailer.left = inserted_node
        else:
            trailer.right = inserted_node
    
    def one_dim_search(self, sx, tx, node=None):
        """
        kD tree に対し閉区間 [sx, tx] 内に存在する点を探してリストにまとめて返す (対応する点の個数 k として O(k))
        下記のように検索必要性を判断し再帰的に左右の子に対し探索を行えば良い

        <-------- node.x -------->
           <----------->
          少しでも [sx,tx] が左側ゾーン ((-inf, node.x]) に被っていたら検索しておく必要がある
                      <----->
                      少しでも [sx, tx] が右側ゾーン ([node.x, inf)) に被っていたら検索しておく必要がある
        """
        buf = []
        node = self.root if node is None else node
        if node.left != self.nil and sx <= node.x:
            buf += self.one_dim_search(sx, tx, node.left)
        if sx <= node.x <= tx:
            buf.append(node.x)
        if node.right != self.nil and tx >= node.x:
            buf += self.one_dim_search(sx, tx, node.right)
        return buf


from operator import itemgetter
class TwoDimNode:
    def __init__(self, x=None, y=None, parent=None, left=None, right=None):
        """
        2 次元二分探索木のためのノード
        """        
        self.x = x
        self.y = y
        self.parent = parent
        self.left = left
        self.right = right
        self.flag = True

class TwoDimTree:
    def __init__(self, points=[]):
        """
        2 次元二分探索木 (kD tree) を作成する
        root の深さを 0 として、深さが偶数の場合そこでは x を基準に、奇数の場合 y を基準に二分探索木条件を満たすようにする
        """
        # nil の設定
        self.nil = TwoDimNode()
        self.nil.parent = self.nil
        self.nil.left = self.nil
        self.nil.right = self.nil
        # root の設定
        self.root = self.nil
        # もし予め一次元の点の集合が与えられるのならバランスする形で kD tree を構築する
        self._balance_insert(points)
    
    def preorder_traverse(self, node=None):
        node = self.root if node is None else node
        if node != self.nil:
            print(f"({node.x},{node.y})", end=' ')
            self.preorder_traverse(node=node.left)
            self.preorder_traverse(node=node.right)
        
    def postorder_traverse(self, node=None):
        node = self.root if node is None else node
        if node != self.nil:
            self.preorder_traverse(node=node.left)
            self.preorder_traverse(node=node.right)
            print(f"({node.x},{node.y})", end=' ')

    def inorder_traverse(self, node=None):
        node = self.root if node is None else node
        if node != self.nil:
            self.preorder_traverse(node=node.left)
            print(f"({node.x},{node.y})", end=' ')
            self.preorder_traverse(node=node.right)
    
    def _balance_insert(self, seq, depth=0):
        # 毎回 x or y をキーとしてソートを行い、中央値をとって insert すれば平衡になる
        if seq:
            arranged = sorted(seq, key=itemgetter(depth % 2))
            mid = len(seq) // 2
            self.insert(seq[mid][0], seq[mid][1])
            self._balance_insert(arranged[:mid], depth+1)
            self._balance_insert(arranged[mid+1:], depth+1)


    def insert(self, x, y):
        """
        kD tree に値が (x, y) であるノードを O(depth) で挿入する
        (コンストラクタで生成した kD tree は平衡であることが保証されるが、insert により生成した部分の平衡性は保証されないことに注意)        
        """
        trailer = self.nil    # (x, y) を挿入するべき nil の一つ前のノードを保存するトレーラポインタ
        pos = self.root    # (x, y) を挿入するべき nil の場所を探す
        depth = 0
        while pos != self.nil:
            trailer = pos
            k, pos_k = (x, pos.x) if depth % 2 == 0 else (y, pos.y)
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
        k, trailer_k = (x, trailer.x) if depth % 2 == 0 else (y, trailer.y)
        # tree is empty
        if trailer == self.nil:
            self.root = inserted_node
        # どこかのノードの子供の位置に挿入する時
        elif k < trailer_k or (k == trailer_k and trailer.flag):
            trailer.left = inserted_node
        else:
            trailer.right = inserted_node
    
    def two_dim_search(self, sx, tx, sy, ty, node=None, depth=0):
        """
        kD tree に対し閉区間 D = {(x, y) | sx<=x<=tx, sy<=y<=ty} 内に存在する点を探してリストにまとめて返す (対応する点の個数 k として O(√n + k))
        下記のように検索必要性を判断し再帰的に左右の子に対し探索を行えば良い

        <-------- node.x -------->
           <----------->
          少しでも [sx,tx] が左側ゾーン ((-inf, node.x]) に被っていたら検索しておく必要がある
                      <----->
                      少しでも [sx, tx] が右側ゾーン ([node.x, inf)) に被っていたら検索しておく必要がある
        """        
        buf = []
        node = self.root if node is None else node
        # print(f"{node.x} {node.y}")
        if depth % 2 == 0:
            if node.left != self.nil and sx <= node.x:
                buf += self.two_dim_search(sx, tx, sy, ty, node.left, depth+1)
            if sx <= node.x <= tx and sy <= node.y <= ty:
                buf.append((node.x, node.y))
            if node.right != self.nil and tx >= node.x:
                buf += self.two_dim_search(sx, tx, sy, ty, node.right, depth+1)
        else:
            if node.left != self.nil and sy <= node.y:
                buf += self.two_dim_search(sx, tx, sy, ty, node.left, depth+1)
            if sx <= node.x <= tx and sy <= node.y <= ty:
                buf.append((node.x, node.y))
            if node.right != self.nil and ty >= node.y:
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
