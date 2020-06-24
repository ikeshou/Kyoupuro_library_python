import pytest
from random import randint
from mypkg.number_theory.modpow import modpow



def test_modpow():
    """
    Iteration 回 a, r, mod をランダム生成して modpow を計算し、組み込みの pow と計算結果を比較するテストを行う。
    """
    Iteration = 100
    for _ in range(Iteration):
        a = randint(-10000, 10000)    # a は任意の整数
        r = randint(0, 100)    # r >= 0 を仮定
        mod = randint(1, 10000)    # mod >= 1　を仮定
        print(a, r, mod)
        assert modpow(a, r, mod) == pow(a, r, mod)




if __name__ == "__main__":
    pytest.main(['-v', __file__])
