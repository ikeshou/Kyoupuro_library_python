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

combination(n, r, m):
    O(nlgm) (階乗がすでに計算済みの場合 O(lgm)) (mod の階乗が繰返し二乗法分 O(lgm) かかる)
    nCr (mod m) を求める
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
    fact_mod[i] は i! % mod を表す。fact_mod[0] ~ facto_mod[size] まで計算可能なテーブルを返す
    >>> make_factorial_table(20, 10**9+7)
    [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800, 479001600, 227020758, 178290591, 674358851, 789741546, 425606191, 660911389, 557316307, 146326063]
    """
    fact_mod = [1] * (size + 1)
    for i in range(1, size + 1):
        fact_mod[i] = (fact_mod[i - 1] * i) % mod
    return fact_mod


def combination(n, r, mod, fact_table):
    """
    フェルマーの小定理 
    a ^ p-1 ≡ 1 (mod p)
    a ^ p-2 ≡ 1/a (mod p) (逆元)
    nCr = (n!) / ((n-r)! * r!) だが、mod p の世界ではこの分母を逆元を用いて計算しておくことが可能
    
    >>> m = 1000000007
    >>> fact_table = make_factorial_table(100, m)
    >>> combination(10, 5, m, fact_table)
    252
    >>> combination(100, 50, m, fact_table)
    538992043
    """
    numerator = fact_table[n]
    denominator = (fact_table[n-r] * fact_table[r]) % mod
    # pow はすでに繰り返し二乗法で効率的に実装されている
    return (numerator * pow(denominator, mod-2, mod)) % mod
# ==================================    



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # check the corner cases!
    mod = 10 ** 9 + 7
    fact_mod = make_factorial_table(100, mod)
    assert(combination(1, 0, mod, fact_mod) == 1)
    assert(combination(100, 0, mod, fact_mod) == 1)
    assert(combination(1, 1, mod, fact_mod) == 1)
    assert(combination(100, 1, mod, fact_mod) == 100)

    print(" * assertion test ok * ")
