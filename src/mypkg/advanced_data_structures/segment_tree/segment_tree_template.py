class SegTree:
    "1-indexing segment tree that manages {a_1, a_2, ..., a_k, ..., a_size}"
    def __init__(self, size, identity, func):
        """
        for Range Minimum Query: identity=float('inf'), func=min
        for Range Sum Query: identity=0, func=op.add
        """
        self.size = size    # 数列の要素数
        self.identity = identity    # デフォルト値
        self.func = func    # 配下の 2 区間のデータに対しどのような処理を行うか
        self.n0 = 2 ** (self.size-1).bit_length()    # 最下段の開始 index。(size-1).bit_length() で最下段を含まぬ段数がわかる。
        self.table = [self.identity] * (2 * self.n0)    # self.table[0] はダミーとして用意
    
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
            self.table[table_k] = self.func(self.table[SegTree._left(table_k)], self.table[SegTree._right(table_k)])
    
    def query(self, l, r):
        """
        calculate the inquired value ranging from a_l to a_r
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
        ans = self.identity
        while table_l < table_r:
            if table_l & 0b1 == 1:
                ans = self.func(ans, self.table[table_l])
            if table_r & 0b1 == 0:
                ans = self.func(ans, self.table[table_r])
            table_l = SegTree._parent(table_l + 1)
            table_r = SegTree._parent(table_r - 1)
        if table_l == table_r:
            ans = self.func(ans, self.table[table_l])
        return ans


if __name__ == "__main__":
    import operator as op
    from random import randint

    for j in range(100):
        NUM = randint(1, 10**3)
        L = [randint(0, 10**3) for _ in range(NUM)]

        RMQ = SegTree(NUM, identity=float('inf'), func=min)
        for i, num in enumerate(L):
            RMQ.update(i+1, num)    # 1-index
        for _ in range(10**3):
            a = randint(1, NUM)
            b = randint(1, NUM)
            a, b = min(a, b), max(a, b)
            assert(RMQ.query(a, b) == min(L[a-1:b]))
        
        RSQ = SegTree(NUM, identity=0, func=op.add)
        for i, num in enumerate(L):
            RSQ.update(i+1, num)    # 1-index
        for _ in range(10**3):
            a = randint(1, NUM)
            b = randint(1, NUM)
            a, b = min(a, b), max(a, b)
            assert(RSQ.query(a, b) == sum(L[a-1:b]))
    
    print(" * assertion test ok *")

