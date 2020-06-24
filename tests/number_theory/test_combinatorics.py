import pytest
from random import randint, shuffle
import math
from mypkg.number_theory.combinatorics import factorial_gen, make_factorial_table, make_inv_factorial_table, combination, Pascal


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


def test_make_factorial():
    """
    mod 10**9+7 or mod 998244353 とする。
    n = 10 ** 2 までの階乗テーブルが正しいか math.factorial を用いて検証する
    """
    N = 10 ** 2
    mod_list = [1000000007, 998244353]
    for mod in mod_list:
        fact = make_factorial_table(N, mod)
        for i in range(N+1):
            assert fact[i] == math.factorial(i) % mod



def test_make_factorial_inv():
    """
    mod 10**9+7 or mod 998244353 とする。
    n = 10 ** 2 までの階乗テーブルが正しいか math.factorial を用いて検証する    
    """
    N = 10 ** 2
    mod_list = [1000000007, 998244353]
    for mod in mod_list:
        inv_fact = make_inv_factorial_table(N, mod)
        for i in range(N+1):
            assert (inv_fact[i] * (math.factorial(i) % mod)) % mod == 1


def test_combination():
    """
    mod 10**9+7 or mod 998244353 とする。
    n <= 10 ** 2 とし、n, r をランダムに選択することを Iteration 回行う。
    それぞれについて combination を計算し、math.comb を用いて検証する
    """
    n = 10 ** 2
    Iteration = 300
    mod_list = [1000000007, 998244353]
    for mod in mod_list:    
        fact = make_factorial_table(n, mod)
        inv_vact = make_inv_factorial_table(n, mod)
        for _ in range(Iteration):
            a = randint(0, n)
            b = randint(0, a)
            expected = math.comb(a, b) % mod
            assert combination(a, b, mod, fact) == expected
            assert combination(a, b, mod, fact, inv_vact) == expected



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