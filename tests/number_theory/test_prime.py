import pytest
from random import randint
from collections import defaultdict
from mypkg.number_theory.prime import is_prime, enum_divisor, Eratos



def test_is_prime_handmade():
    """
    とりあえず 50 までの数についてチェックする。
    """
    with pytest.raises(ValueError):
        is_prime(-1)
    with pytest.raises(ValueError):
        is_prime(0)
    p_list =  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for i in range(1, 51):
        assert is_prime(i) == (i in p_list)


def test_enum_divisor():
    """
    1 <= n <= 1000 までの整数を Iteration 回ランダム生成し、毎回約数列挙を行う。
    愚直に約数を調べた結果と照合する。
    """
    with pytest.raises(ValueError):
        enum_divisor(-1)
    with pytest.raises(ValueError):
        enum_divisor(0)
    Iteration = 100
    for _ in range(Iteration):
        n = randint(1, 1000)
        got = enum_divisor(n)
        expected = [i for i in range(1, n + 1) if n % i == 0]
        assert got == expected


def test_eratos_handmade():
    """
    とりあえず 50 までの数についてチェックする。
    素因数分解については、(素数とか関係なしに）愚直に小さい数から割って行った結果と比較照合を行う。
    """
    with pytest.raises(ValueError):
        Eratos(-1)
    with pytest.raises(ValueError):
        Eratos(0)
    with pytest.raises(ValueError):
        Eratos(10).is_prime(0)
    with pytest.raises(ValueError):
        Eratos(10).is_prime(11)
    with pytest.raises(ValueError):
        Eratos(10).prime_factorize(0)
    with pytest.raises(ValueError):
        Eratos(10).prime_factorize(121)    # (prime 判定が行える数 + 1) ^ 2 以上はアウト

    p_list =  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]        
    e = Eratos(50)
    for i in range(1, 51):
        assert e.is_prime(i) == (i in p_list)
    
    for i in range(1, 51**2):
        got = e.prime_factorize(i)
        expected = defaultdict(int)
        target = i
        div = 2
        while target > 1:
            while target % div == 0:
                target //= div
                expected[div] += 1
            div += 1
        expected = dict(expected)
        assert got == expected




if __name__ == "__main__":
    pytest.main(['-v', __file__])