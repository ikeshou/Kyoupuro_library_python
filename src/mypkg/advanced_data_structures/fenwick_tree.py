"""
Fenwick Tree (Binary Indexced Tree) は特殊な segment tree である。
インターフェースは 0-index, 内部では 1-index として実装を行う。

query
L = {a0, a1, ..., an-1}
add(k, x): L[k] に x を足す
sum(i, j): L[i:j] の和を求める
これを共に O(lgn) で行うためのデータ構造


<algorithm>
- 和の場合は二つの子供の区間和データのうち片方の情報は冗長である。それを取り除いた形でデータを保持する。
(左と上見たらわかるくね？という場所を削除)
                8
        4               N
    2      N        6       N
  1   N  3   N    5   N    7   N

- 1-index で LSB の位が下からの段数 (=区間の長さ) を表す
                     1000
          0100                     N
     0010        N          0110         N
  0001   N   0011   N    0101   N    0111    N


- LSB は i&(-i) で求められる

- a1+...+a7 を求めるには、LSB を引いていく。
    7 = 0b0111 -> (0b0111 - 0b0001 =) 6 = 0b0110 -> (0b0110 - 0b0010 =)  4 = 0b0100 -> (0b0100 - 0b0100 =) 0
    [7] + [6] + [4] で求められることがわかる

- a7 を更新するには、LSB を足していく。
    7 = 0b0111 -> (0b0111 + 0b0001 =) 8 = 0b1000
    [7], [8] を更新すれば良いことがわかる
"""



from typing import Union

Num = Union[int, float]



class FenwickTree:
    def __init__(self, size: int):
        self.size = size
        self.bit = [0] * (self.size + 1)
    
    def add(self, k: int, x: Num) -> None:
        """
        (0-index で) k 番目の要素に x をたす。
        >>> b = FenwickTree(5)
        >>> b.add(0, 10)
        >>> b.bit
        [0, 10, 10, 0, 10, 0]
        """
        if not 0 <= k < self.size:
            raise IndexError(f"FenwickTree.add(): size is {self.size}. accessed [{k}]")
        k += 1    # 1-index
        while k <= self.size:
            self.bit[k] += x
            LSB = k & (-k)
            k += LSB
    
    def _accum_sum(self, k: int) -> Num:
        """ (1-index, 内部関数) bit の 1 ~ k 番目の要素の和を求める。"""
        s = 0
        while k > 0:
            s += self.bit[k]
            LSB = k & (-k)
            k -= LSB
        return s
    
    def sum(self, l: int, r: int) -> Num:
        """
        (0-index で) [l, r) 区間の和を求める。
        >>> b = FenwickTree(5)
        >>> b.add(1, 10)
        >>> b.add(2, 20)
        >>> b.sum(1, 3)
        30
        """
        if not 0 <= l <= r <= self.size:
            raise IndexError(f"FenwickTree.sum(): size is {self.size}. got slice is [{l}:{r}]")
        # 0-index の数列における [l]...[r-1] の閉区間を計算。1-index なら [l+1]...[r]。
        return self._accum_sum(r) - self._accum_sum(l)




if __name__ == "__main__":
    import doctest
    doctest.testmod()