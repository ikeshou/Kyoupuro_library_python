import pytest
from random import randint, shuffle
import math
from mypkg.number_theory.combinatorics import factorial_gen, Combinatorics, Pascal


def test_factorial_gen():
    """
    とりあえず 0 から 10 までチェック
    """
    g = factorial_gen()
    next(g)
    indices = list(range(11))
    shuffle(indices)
    for num in indices:
        assert g.send(num) == math.factorial(num)



def test_combinatorics_fact_inv():
    """
    mod 10**9+7 or mod 998244353 とする。
    n = 10 ** 2 までの階乗テーブル、階乗の逆元テーブルが正しいか math.factorial を用いて検証する。
    n <= 10 ** 2 とし、n, r をランダムに選択することを Iteration 回行う。
    それぞれについて combination を計算し、math.comb を用いて検証する
    """
    N = 10 ** 2
    mod_list = [1000000007, 998244353]
    for mod in mod_list:
        c = Combinatorics(N, mod)
        for i in range(N+1):
            assert c.fact[i] == math.factorial(i) % mod
        for i in range(N+1):
            assert (c.inv[i] * (math.factorial(i) % mod)) % mod == 1


def test_combinatorics_comb():
    """
    mod 10**9+7 or mod 998244353 とする。
    n <= 10 ** 2 とし、n, r をランダムに選択することを Iteration 回行う。
    それぞれについて combination を計算し、math.comb を用いて検証する    
    """
    n = 10 ** 2
    Iteration = 300
    mod_list = [1000000007, 998244353]
    for mod in mod_list:    
        c = Combinatorics(n, mod)
        for _ in range(Iteration):
            a = randint(0, n)
            b = randint(0, a)
            expected = math.comb(a, b) % mod
            assert c.comb(a, b) == expected



def test_pascal():
    """
    n <= 10 ** 2 とし、n, r をランダムに選択することを Iteration 回行う。
    それぞれについて combination を計算し、math.comb を用いて検証する
    """
    Iteration = 300
    n = 10 ** 2
    p = Pascal(100)
    for _ in range(Iteration):
        a = randint(0, n)
        b = randint(0, a)
        assert p.comb(a, b) == math.comb(a, b)



if __name__ == "__main__":
    pytest.main(['-v', __file__])