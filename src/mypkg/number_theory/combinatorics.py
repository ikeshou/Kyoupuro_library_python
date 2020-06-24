"""
数え上げや組み合わせ関連の詰め合わせ


factorial_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n! を求める

make_factorial_table(n, m):
    O(n)
    0! ... n! (mod m) までの階乗の計算結果のテーブルを作る

make_inv_factorial_table(n, m):
    O(n + lg m)
    1/0! ... 1/n! (modm) までの階乗の逆元の計算結果のテーブルを作る

combination(n, r, m, fact_table, inv_fact_table=None):
    O(lgm) (inv_fact_table を与えない場合、mod の階乗が繰返し二乗法の分だけかかる) or O(1) (与える場合)
    nCr (mod m) を求める

Pascal:
    __init__(n):
        O(n^2) で初期化、0C0 ... nCn までのパスカルの三角形を構築する
    combination(a, b):
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
# verified @ABC011D, ABC021D, ABC034C, ABC042D, ABC065C, ...
def make_factorial_table(size: int, mod: int) -> List[int]:
    """
    fact_mod[i] は i! % mod を表すとする
    O(n) で fact_mod[size] まで計算結果がメモされたテーブルを構築して返す

    Args:
        size, mod (int)
    Returns:
        list: fact_mod[i] は i! % mod を表す
    Examples:
        >>> make_factorial_table(10, 10**9+7)
        [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
    """
    fact_mod = [1] * (size + 1)
    for i in range(1, size + 1):
        fact_mod[i] = (fact_mod[i - 1] * i) % mod
    return fact_mod


def make_inv_factorial_table(size: int, mod: int) -> List[int]:
    """
    inv_fact_mod[i] は 1/i! % mod を表すとする
    O(n+lgm) で inv_fact_mod[size] まで計算結果がメモされたテーブルを構築して返す

    Args:
        size, mod (int)
    Returns:
        list: inv_fact_mod[i] は 1/i! % mod を表す
    Examples:
        >>> make_inv_factorial_table(10, 10**9+7)
        [1, 1, 500000004, 166666668, 41666667, 808333339, 301388891, 900198419, 487524805, 831947206, 283194722]
    """
    inv_fact_mod = [1] * (size + 1)
    n_fact = 1
    for i in range(2, size+1):
        n_fact = (n_fact * i) % mod
    inv_fact_mod[size] = pow(n_fact, mod-2, mod)    # a ^ p-2 ≡ 1/a (mod p) において a = n! とする。 1/n! (mod p) を求める
    for i in range(size-1, -1, -1):
        inv_fact_mod[i] = (inv_fact_mod[i+1] * (i+1)) % mod    # 1/(n-1)! = 1/n! * n
    return inv_fact_mod


# verified @ABC021D, ABC034C, ABC042D, ABC065C, ABC066D, ...
def combination(n: int, r: int, mod: int, fact_table: List[int], inv_fact_table: List[int]=[]) -> int:
    """
    nCr % mod を逆元テーブルが与えられない場合繰返し二乗法により O(lgm) で計算する。与えられる場合 O(1) で計算する。

    Args:
        n, r, mod (int)
        fact_table (list)
        inv_fact_table (list)
    
    Examples:
        >>> m = 1000000007
        >>> f_table = make_factorial_table(100, m)
        >>> combination(10, 5, m, f_table)
        252
        >>> combination(100, 50, m, f_table)
        538992043
        >>> inv_f_table = make_inv_factorial_table(100, m)
        >>> combination(100, 50, m, f_table, inv_f_table)
        538992043

    Note:
        [フェルマーの小定理]
        a ^ p-1 ≡ 1 (mod p)
        a ^ p-2 ≡ 1/a (mod p) (逆元)
        nCr = (n!) / ((n-r)! * r!) だが、mod p の世界ではこの分母を逆元を用いて計算しておくことが可能
    """
    numerator = fact_table[n]
    if not inv_fact_table:
        # pow はすでに繰り返し二乗法で効率的に実装されている
        denominator = pow((fact_table[n-r] * fact_table[r]) % mod, mod-2, mod)
    else:
        denominator = (inv_fact_table[n-r] * inv_fact_table[r]) % mod
    return (numerator * denominator) % mod
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
