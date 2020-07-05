import pytest
from random import randint
import math
from mypkg.number_theory.euclid_gcd import euclid_gcd, euclid_ext_gcd


def test_euclid_gcd():
    """
    Iteration 回 a, b を生成し gcd を計算。math.gcd と結果を比較するテストを行う。
    """
    Iteration = 1000
    for _ in range(Iteration):
        a, b = randint(-100, 100), randint(-100, 100)
        assert euclid_gcd(a, b) == math.gcd(a, b)


def test_euclid_ext_gcd():
    """
    Iteration 回 a, b を生成し ax + by = d (=gcd) なる x, y, d を計算。
    ax + by の結果を検算し、d を math.gcd と比較するテストを行う。
    """
    Iteration = 1000
    for _ in range(Iteration):
        a, b = randint(-100, 100), randint(-100, 100)
        x, y, d = euclid_ext_gcd(a, b)
        print(a, b, x, y, d)
        assert a * x + b * y == d
        assert d == math.gcd(a, b)



if __name__ == "__main__":
    pytest.main(['-v', __file__])

