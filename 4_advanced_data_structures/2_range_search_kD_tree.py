"""
多次元データを扱うための二分探索木である kD tree (二次元版を実装)
前処理に O(nlg^2n), range search なる区間幅を指定してそれに含まれるデータを探索するクエリを O(n^(1-1/d) + k) で捌くことができる
(k はサーチで引っかかる要素数)


<algorithm>
depth ごとに大小関係を調査する key を x 座標、 y 座標と交互に変更する BST を作成
(root を depth = 0 として、depth % 2 == 0 のノードでは x 座標で、1 のノードでは  y 座標で比較を行う)
(一致していた場合 最初は右に振り分け以降は前回と逆方向に振り分ける)
"""


from operator import itemgetter
from typing import List, Tuple, Optional, Union, Sequence

Num = Union[int, float]


# verified @ABC045D, ABC075D
class TwoDimNode:
    def __init__(self, x: Optional[Num]=None, y: Optional[Num]=None, parent: Optional['TwoDimNode']=None, left: Optional['TwoDimNode']=None, right: Optional['TwoDimNode']=None):
        """
        2 次元二分探索木のためのノード
        """        
        self.x = x
        self.y = y
        self.parent = parent
        self.left = left
        self.right = right

class TwoDimTree:
    def __init__(self, points: Sequence[Sequence[Num]]=[]):
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
    
    def _balance_insert(self, seq: Sequence[Sequence[Num]], depth: int=0):
        # 毎回 x or y をキーとしてソートを行い、中央値をとって insert すれば平衡になる
        if seq:
            arranged = sorted(seq, key=itemgetter(depth % 2))
            mid = len(seq) // 2
            self._insert(arranged[mid][0], arranged[mid][1])
            self._balance_insert(arranged[:mid], depth+1)
            self._balance_insert(arranged[mid+1:], depth+1)


    def _insert(self, x: Num, y: Num):
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
            if k <= pos_k:
                pos = pos.left
            else:
                pos = pos.right
            depth += 1
        inserted_node = TwoDimNode(x, y, trailer, self.nil, self.nil)
        # trailer の depth
        depth -= 1
        k, trailer_k = (x, trailer.x) if depth % 2 == 0 else (y, trailer.y)
        # tree is empty
        if trailer == self.nil:
            self.root = inserted_node
        # どこかのノードの子供の位置に挿入する時
        elif k <= trailer_k:
            trailer.left = inserted_node
        else:
            trailer.right = inserted_node
    
    def two_dim_search(self, sx: Num, tx: Num, sy: Num, ty: Num, node: Optional[TwoDimNode]=None, depth: int=0) -> List[Tuple[Num]]:
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

    H = 1000
    W = 1000
    Iteration = 100

    # 盤面形成を 100 回
    for _ in range(Iteration):
        # (0,0) ~ (1000,1000) グリッドに 1000 個点をばらまく
        L_2 = [(random.randint(0, H), random.randint(0, W)) for _ in range(1000)]
        # 平衡した kD tree 作成
        tree_2 = TwoDimTree(L_2)
        # 100 個レンジサーチクエリをランダム作成
        query = []
        for _ in range(100):
            sx, tx = random.randint(0, H), random.randint(0, H)
            sy, ty = random.randint(0, W), random.randint(0, W)
            sx, tx = min(sx, tx), max(sx, tx)
            sy, ty = min(sy, ty), max(sy, ty)
            query.append((sx, tx, sy, ty))
        # クエリへの答えが 100 個全てについて正しかったか確認
        for sx, tx, sy, ty in query:
            calculated_points = tree_2.two_dim_search(sx, tx, sy, ty)
            ans_points = []
            for i, j in L_2:
                if sx <= i <= tx and sy <= j <= ty:
                    ans_points.append((i, j))
            assert (set(calculated_points) == set(ans_points))
    
    print(" * assertion test ok * ")
