#!/usr/bin/env python3
"""
number theory algorithms implemented in Python3 for programming competition

euclid_gcd(a, b):
    O(lgn)
    a, b の gcd を求める

fibonacci(n):
    O(n)
    n 番目のフィボナッチ数を求める

fibonacci_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n 番目のフィボナッチ数を求める

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



# ==== memorizing recursive function =====
def euclid_gcd(a, b):
    """
    ユークリッドの互除法 gcd(a, b) = gcd(b, r) (但し r = a % b)
    >>> euclid_gcd(74, 54)
    2
    """
    a, b = max(a, b), min(a, b)
    if b == 0:
        return a
    return euclid_gcd(b, a%b)


def fibonacci(n, a=1, b=0):
    """
    (0), 1, 1, 2, 3, 5, 8, 13, ...
    と考える。最初 a は 1 を b は 0 を指す。これが再帰の度に一つずつ進んでいく。
    第一引数 x は n - x 回再帰を回ったことを表し、第二引数 a は n - x + 1 番目の fibonacci のメモ、第三引数 b は n - x 番目の fibonacci のメモとなっている。
    x = 1 となった段階で a が n 番目の fibonacci 数を指していることになるのでこれを返せば良い。
    >>> fibonacci(10)
    55
    """
    if n == 1:
        return a
    return fibonacci(n-1, a+b, a)
# ========================================


# ==== generator ====
def fibonacci_gen():
    """
    >>> g = fibonacci_gen()
    >>> next(g)
    >>> g.send(1)
    1
    >>> g.send(2)
    1
    >>> g.send(10)
    55
    >>> g.send(9)    # just refer the table
    34
    """
    fibo_memo = [0, 1, 1]    # i 番目の fibonacci 数が fibo_memo[i] に入るようにする
    ind = yield
    while True:
        if len(fibo_memo)-1 < ind:
            for i in range(len(fibo_memo), ind+1):
                fibo_memo.append(fibo_memo[i-1]+fibo_memo[i-2])
        ind = yield fibo_memo[ind]    # send メソッドで generator に計算して欲しい値を送り込むことを想定


def factorial_gen():
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
def make_factorial_table(size, mod):
    """
    fact_mod[i] は i! % mod を表す。fact_mod[0] ~ fact_mod[size] まで計算可能なテーブルを O(n) で返す
    >>> make_factorial_table(10, 10**9+7)
    [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
    """
    fact_mod = [1] * (size + 1)
    for i in range(1, size + 1):
        fact_mod[i] = (fact_mod[i - 1] * i) % mod
    return fact_mod


def make_inv_factorial_table(size, mod):
    """
    inv_fact_mod[i] は 1/i! % mod を表す。inv_fact_mod[0] ~ inv_fact_mod[size] まで計算可能なテーブルを O(n+lgm) で返す
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



def combination(n, r, mod, fact_table, inv_fact_table=None):
    """
    フェルマーの小定理 
    a ^ p-1 ≡ 1 (mod p)
    a ^ p-2 ≡ 1/a (mod p) (逆元)
    nCr = (n!) / ((n-r)! * r!) だが、mod p の世界ではこの分母を逆元を用いて計算しておくことが可能
    逆元テーブルが与えられない場合繰返し二乗法により O(lgm) で計算する。与えられる場合 O(1) で計算する。
    
    >>> m = 1000000007
    >>> fact_table = make_factorial_table(100, m)
    >>> combination(10, 5, m, fact_table)
    252
    >>> combination(100, 50, m, fact_table)
    538992043
    >>> inv_fact_table = make_inv_factorial_table(100, m)
    >>> combination(100, 50, m, fact_table, inv_fact_table)
    538992043
    """
    numerator = fact_table[n]
    if inv_fact_table is None:
        denominator = pow((fact_table[n-r] * fact_table[r]) % mod, mod-2, mod)
    else:
        denominator = (inv_fact_table[n-r] * inv_fact_table[r]) % mod
    # pow はすでに繰り返し二乗法で効率的に実装されている
    return (numerator * denominator) % mod
# ==================================    


# ==== Pascal's triangle ===========
class Pascal:
    def __init__(self, num):
        """
        0C0 ... numCnum までのコンビネーションの値を計算したパスカルの三角形を O(n^2) で構築する。
        self.pascal[i][j] = i C j
        """
        self.n = num
        self.pascal = [[1] * (i+1) for i in range(num+1)]    # iC0, iCi は 1. 初期化をかねて記入しておく
        for i in range(2, num+1):    # i 段目 iC0 ... iCi (0, 1 段目は 1 なので更新する必要がない。2 段目以降をみる。)
            for j in range(1, i):    # iC0, iCi 以外について update
                self.pascal[i][j] = self.pascal[i-1][j-1] + self.pascal[i-1][j]
    
    def comb(self, a, b):
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

    # check the corner cases!
    mod = 10 ** 9 + 7
    fact_mod = make_factorial_table(100, mod)
    inv_fact_mod = make_inv_factorial_table(100, mod)
    assert(combination(1, 0, mod, fact_mod) == 1)
    assert(combination(1, 0, mod, fact_mod, inv_fact_mod) == 1)
    assert(combination(100, 0, mod, fact_mod) == 1)
    assert(combination(100, 0, mod, fact_mod, inv_fact_mod) == 1)
    assert(combination(1, 1, mod, fact_mod) == 1)
    assert(combination(1, 1, mod, fact_mod, inv_fact_mod) == 1)
    assert(combination(100, 1, mod, fact_mod) == 100)
    assert(combination(100, 1, mod, fact_mod, inv_fact_mod) == 100)


    p = Pascal(50)
    assert(p.comb(0, 0) == 1)
    assert(p.comb(1, 0) == 1)
    assert(p.comb(1, 1) == 1)
    assert(p.comb(50, 0) == 1)
    assert(p.comb(50, 50) == 1)
    assert(p.comb(50, 25) == 126410606437752)

    print(" * assertion test ok * ")
