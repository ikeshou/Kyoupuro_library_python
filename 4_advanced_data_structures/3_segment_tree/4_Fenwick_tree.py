"""
Fenwick tree that handles Range Sum Query implemented in Python3 for programming competition

Fenwick Tree (Binary Indexced Tree) は特殊な segment tree である。

query
add(k, x): k 番目の数に x を足す 
(summation(k-1, k) で a_k 求めて差分を算出してやり add することで update もできるけど...そこまでやるなら seg tree でよくない？)
summation(i, j): i ... j なる区間の最小値を求める
これを共に O(lgn) で行うためのデータ構造

和の場合は二つの子供の区間和データのうち片方の情報は冗長である。それを取り除いた形でデータを保持する。
                8
        4               N
    2      N        6       N
  1   N  3   N    5   N    7   N

- 左と上見たらわかるくね？という場所を削除
- 1-index で LSB の位が下からの段数 (=区間の長さ) を表す

- LSB は i&(-i) で求められる
- a1+...a7 を求めるには、LSB を引いていく。
    7 = 0b0111 -> (0b0111 - 0b0001 =) 6 = 0b0110 -> (0b0110 - 0b0010 =)  4 = 0b0100 -> (0b0100 - 0b0100 =) 0
    [7] + [6] + [4] で求められることがわかる
- a7 を更新するには、LSB を足していく。
    7 = 0b0111 -> (0b0111 + 0b0001 =) 8 = 0b1000
    [7], [8] を更新すれば良いことがわかる
"""


class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.table = [0] * (self.size + 1)
    
    def add(self, k, x):
        """
        add x to a_k
        Args:
            k (int): 1-indexed integer
            x (object)        
        """
        while k <= self.size:
            self.table[k] += x
            LSB = k & (-k)
            k += LSB
    
    def accum_sum(self, k):
        """
        calculate the summation of elements ranging from a_1 to a_k
        Args:
            k (int): 1-indexed integer
            x (object)               
        """
        s = 0
        while k > 0:
            s += self.table[k]
            LSB = k & (-k)
            k -= LSB
        return s
    
    def summation(self, l, r):
        """
        calculate the summation of elements ranging from a_l to a_r
        Args:
            l (int): 1-indexed integer
            r (int): 1-indexed integer
        Returns:
            object
        """
        start_to_before_left = self.accum_sum(l-1) if l != 1 else 0    # accumulation sum of a_1 to a_(l-1)
        start_to_right = self.accum_sum(r)    # accumulation sum of a_1 to a_r
        return start_to_right - start_to_before_left


if __name__ == "__main__":
    import random
    ft = FenwickTree(7)
    L = [1, 5, 3, 10, 100, 7, 6]
    for i, num in enumerate(L):
        ft.add(i+1, num)    # 1-index
    print(ft.table)    # [0, 1, 6, 3, 19, 100, 107, 6]

    for _ in range(10):
        a = random.randint(1, 7)
        b = random.randint(1, 7)
        a, b = min(a, b), max(a, b)
        print(f"RMQ [{a}, {b}]: {ft.summation(a, b)}")