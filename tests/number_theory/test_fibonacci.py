import pytest
from random import randint
from mypkg.number_theory.fibonacci import fibonacci, fibonacci_gen


F = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


def test_fibonacci():
    for i in range(len(F)):
        assert fibonacci(i+1) == F[i]    # 関数は 1 番目のフィボナッチ数を 1 としている。i 番目のフィボナッチ数を返す。


def test_fibonacci_gen():
    g = fibonacci_gen()
    next(g)
    for _ in range(100):
        i = randint(0, len(F) - 1)
        assert g.send(i+1) == F[i]




if __name__ == "__main__":
    pytest.main(['-v', __file__])

