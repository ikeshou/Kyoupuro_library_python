"""
数え上げや組み合わせ関連の詰め合わせ


factorial_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n! を求める


Combinatorics:
    __init__(size, m):
        O(n) で 0! ... n! (mod m) までの階乗の計算結果のテーブルを作り self.fact に保存
        O(n + lgm) で 1/0! ... 1/n! (modm) までの階乗の逆元の計算結果のテーブルを作り self.inv に保存
    comb(a, b):
        O(1) で aCb (mod m) を計算する


Pascal:
    __init__(n):
        O(n^2) で初期化、0C0 ... nCn までのパスカルの三角形を構築する
    comb(a, b):
        O(1) で aCb を計算する
"""


from typing import Generator, List



# ==== generator ====
def factorial_gen() -> Generator[int, int, None]:
    """
    >>> g = factorial_gen()
    >>> next(g)
    >>> g.send(5)
    120
    >>> g.send(10)
    3628800
    >>> g.send(9)    # just refer the table
    362880
    """
    fact_memo = [1]    # i! が fact_memo[i] に入るようにする
    ind = yield
    while True:
        if len(fact_memo)-1 < ind:
            for i in range(len(fact_memo), ind+1):
                fact_memo.append(i * fact_memo[i-1])
        ind = yield fact_memo[ind]    # # send メソッドで generator に計算して欲しい値を送り込むことを想定
# ===================



# ===== combination with mod =======
# verified @ABC021D, ABC034C, ABC042D, ABC065C, ABC066D, ABC172E...
class Combinatorics:
    def __init__(self, size: int, mod: int):
        """
        >>> c = Combinatorics(size=10, mod=10**9+7)
        >>> c.fact
        [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
        >>> c.inv
        [1, 1, 500000004, 166666668, 41666667, 808333339, 301388891, 900198419, 487524805, 831947206, 283194722]
        """
        self.size =  size
        self.mod = mod
        self.fact = self._build_factorial(size, mod)
        self.inv = self._build_inv_factorial(size, mod)
    
    def _build_factorial(self, size:int , mod: int) -> None:
        """
        fact_mod[i] は i! % mod を表すとする
        O(n) で fact_mod[size] まで計算結果がメモされたテーブルを構築して返す
        """
        fact = [1] * (size + 1)
        for i in range(1, size + 1):
            fact[i] = (fact[i-1] * i) % mod
        return fact
    
    def _build_inv_factorial(self, size: int, mod: int) -> None:
        """
        inv_fact_mod[i] は 1/i! % mod を表すとする
        O(n+lgm) で inv_fact_mod[size] まで計算結果がメモされたテーブルを構築して返す
        Note:
            [フェルマーの小定理]
            a ^ p-1 ≡ 1 (mod p)
            a ^ p-2 ≡ 1/a (mod p) (逆元)
            nCr = (n!) / ((n-r)! * r!) だが、mod p の世界ではこの分母を逆元を用いて計算しておくことが可能
        """
        inv_fact_mod = [1] * (size + 1)
        inv_fact_mod[size] = pow(self.fact[size], mod-2, mod)    # a ^ p-2 ≡ 1/a (mod p) において a = n! とする。 1/n! (mod p) を求める
        for i in range(size-1, -1, -1):
            inv_fact_mod[i] = (inv_fact_mod[i+1] * (i+1)) % mod    # 1/(n-1)! = 1/n! * n
        return inv_fact_mod
    
    def comb(self, n: int, r: int) -> int:
        """
        nCr % mod を O(1) で計算する。
        Examples:
            >>> c = Combinatorics(size=100, mod=10**9+7)
            >>> c.comb(100, 50)
            538992043   
        """
        numerator = self.fact[n]
        denominator = (self.inv[n-r] * self.inv[r]) % self.mod
        return (numerator * denominator) % self.mod
# ==================================    



# ==== Pascal's triangle ===========
# verified @ABC008C, ABC057D
class Pascal:
    def __init__(self, n: int):
        """
        0C0 ... nCn までのコンビネーションの値を計算したパスカルの三角形を O(n^2) で構築する。
        self.pascal[i][j] = iCj を表す。
        """
        self.n = n
        self.pascal = [[1] * (i+1) for i in range(n+1)]    # iC0, iCi は 1. 初期化をかねて記入しておく
        for i in range(2, n+1):    # i 段目 iC0 ... iCi (0, 1 段目は 1 なので更新する必要がない。2 段目以降をみる。)
            for j in range(1, i):    # iC0, iCi 以外について update
                self.pascal[i][j] = self.pascal[i-1][j-1] + self.pascal[i-1][j]
    
    def comb(self, a: int, b: int) -> int:
        """
        >>> p = Pascal(10)
        >>> p.comb(10, 5)    # 10C5
        252
        """
        assert a >= b
        return self.pascal[a][b]
# ================================== 



if __name__ == "__main__":
    import doctest
    doctest.testmod()
