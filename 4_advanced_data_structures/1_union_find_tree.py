"""
互いに素なグラフのためのデータ構造 Union Find 木
内部で基本的な操作 make_set, find_set, union をサポートする。トータルの操作 m, make_set の回数 n とする。
rank による合併戦略と経路圧縮を用いると O(m * α(n)) となる。(α(n) はほぼ定数)

クエリ
union(x, y) -> x と y の属するグループを統合する。
is_same(x, y) -> x と y の属するグループが一致するか判定する。
akin_num(x) -> x の属するグループのサイズを計算する。

ならしコスト
make_set: O(1)
find_set: O(α(n))
union:    O(α(n))
is_same:  O(α(n))
akin_num: O(1)
"""


class UnionFindTree:
    def __init__(self, num_of_elm):
        """
        0 ... num_of_elem - 1 まで数字で表される (0-index) グループを管理する union find tree を作成する (O(n))
        """
        self.n = num_of_elm
        self.table = [i for i in range(self.n)]    # table[ind] は ind の親の index を表す。ind == table[ind] の時そのグループの root である。
        self.rank = [0] * self.n    # root となる ind について rank[ind] はその木の深さを表す。それ以外の ind については意味を持たない。
        self.group_size = [1] * self.n    # root となる ind について group_size[ind] はそのグループに属するメンバの個数を表す。それ以外の ind については意味を持たない。
    
    def _find_set(self, x):
        """
        x の属するグループ番号を O(α(n)) で求める
        """
        parent = self.table[x]
        if x == parent:
            return x
        else:
            root = self._find_set(parent)
            # 経路圧縮
            self.table[x] = root
            return root
    
    def is_same(self, x, y):
        """
        x と y が同じグループに属するか O(α(n)) で判定する
        """
        return self._find_set(x) == self._find_set(y)

    def union(self, x, y):
        """
        x と y の属するグループを O(α(n)) で統合する
        """
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

    def akin_num(self, x):
        """
        x の属するグループのサイズを O(1) で計算する
        """
        x_root = self._find_set(x)
        return self.group_size[x_root]

    def print_group_id(self):
        print([self._find_set(x) for x in self.table])



if __name__ == "__main__":
    import random
    uf = UnionFindTree(20)
    for i in range(20):
        x = random.randint(0, 19)
        y = random.randint(0, 19)
        res = uf.union(x, y)
        if res:
            print(f"{x} and {y} are unioned.")
        else:
            print(f"-- {x} and {y} are in the same group.")
    print("")
    uf.print_group_id()
    print("")
    print(uf.is_same(0, 19))
    print(uf.akin_num(0))
