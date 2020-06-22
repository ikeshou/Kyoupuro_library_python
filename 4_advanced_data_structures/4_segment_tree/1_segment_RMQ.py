"""
Segment tree that handles Range Minimum Query implemented in Python3 for programming competition

query
update(i, x): i 番目の数を x に変更する
minimum(i, j): i ... j なる区間の最小値を求める
これを共に O(lgn) で行うためのデータ構造

一般的に segment tree に突っ込むにはクエリが結合法則を満たしていれば良い。この場合で言うと minimum(a, b, c) = m(m(a, b), c) = m(a, m(b, c))
query の処理は実は [i, j) というように半開区間で受け持つと実装が少しシンプルになるらしい。m = (i + j) // 2 として [i, j) -> [i, m) と [m, j) のようにシンプルに分割できるので。

0...dummy
                1
        2               3
    4      5        6       7
  8   9  10  11   12  13  14  15
と言う形で各区間を受け持つ (葉は最小単位の区間を受け持っている)
"""

class SegTree:
    "1-indexing segment tree that manages {a_1, a_2, ..., a_k, ..., a_size}"
    def __init__(self, size):
        self.size = size    # 数列の要素数
        self.n0 = 2 ** (self.size-1).bit_length()    # 最下段の開始 index。(size-1).bit_length() で最下段を含まぬ段数がわかる。
        self.table = [float('inf')] * (2 * self.n0)    # [0] はダミーとして用意。minimum を考える都合上 inf で初期化する。
    
    @classmethod
    def _parent(cls, k):
        return k // 2
    @classmethod
    def _left(cls, k):
        return 2 * k
    @classmethod
    def _right(cls, k):
        return 2 * k + 1
    
    def update(self, k, x):
        """
        update the value of a_k to x
        Args:
            k (int): 1-indexed integer
            x (object)
        """
        table_k = k + self.n0 - 1    # table での index
        self.table[table_k] = x
        while SegTree._parent(table_k) > 0:
            table_k = SegTree._parent(table_k)
            self.table[table_k] = min(self.table[SegTree._left(table_k)], self.table[SegTree._right(table_k)])
    
    def minimum(self, l, r):
        """
        calculate the minimum value ranging from a_l to a_r
        Args:
            l (int): 1-indexed integer
            r (int): 1-indexed integer
        Returns:
            object
        """
        if l > r:
            raise RuntimeError(f'l should be less than or equals to r. got l={l} r={r}')
        table_l = l + self.n0 - 1
        table_r = r + self.n0 - 1
        # それぞれ一つ上の段の '現在のカバー範囲と被っていない、カバー範囲が倍の隣の領域' を見にいく。
        # 左端から右上の段へ移動していくやつについて。1-index で奇数の場合カバー範囲が変わり倍になる。
        # 右端から左上の段へ移動していくやつについて。1-index で偶数の場合カバー範囲が変わり倍になる。
        # left と right で反転したならば探索終了
        ans = float('inf')
        while table_l < table_r:
            if table_l & 0b1 == 1:
                ans = min(ans, self.table[table_l])
            if table_r & 0b1 == 0:
                ans = min(ans, self.table[table_r])
            table_l = SegTree._parent(table_l + 1)
            table_r = SegTree._parent(table_r - 1)
        if table_l == table_r:
            ans = min(ans, self.table[table_l])
        return ans


if __name__ == "__main__":
    import random
    seg = SegTree(7)
    L = [1, 5, 3, 10, 100, 7, 6]
    for i, num in enumerate(L):
        seg.update(i+1, num)    # 1-index
    print(seg.table)    # [inf, 1, 1, 6, 1, 3, 7, 6, 1, 5, 3, 10, 100, 7, 6, inf]

    for _ in range(10):
        a = random.randint(1, 7)
        b = random.randint(1, 7)
        a, b = min(a, b), max(a, b)
        print(f"RMQ [{a}, {b}]: {seg.minimum(a, b)}")
        