def ceil_alternative(x, y):
    """
    ceil(x / y) を返す (y を何整数倍すると x 以上になるか？の値)

    >>> ceil_alternative(4, 2)
    2
    >>> ceil_alternative(4, 3)
    2

    > ceil() 、 floor() 、および modf() 関数については、非常に大きな浮動小数点数が 全て 整数そのものになるということに注意してください。
    > 通常、Python の浮動小数点型は 53 ビット以上の精度をもたない (プラットフォームにおける C double 型と同じ) ので、
    > 結果的に abs(x) >= 2**52 であるような浮動小数点型 x は小数部分を持たなくなるのです。
    > 10 ** 15 + 0.2 == 10 ** 15
    > False
    > 10 ** 16 + 0.2 == 10 ** 16
    > True
    
    x / y が大きな浮動小数点数となる場合はこの関数を使うようにする。
    """
    assert (x >= 0 and y > 0)
    return (x + y - 1) // y



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(ceil_alternative(0, 1) == 0)
    assert(ceil_alternative(1, 1) == 1)
    assert(ceil_alternative(2, 1) == 2)
    assert(ceil_alternative(7, 3) == 3)
    assert(ceil_alternative(7, 4) == 2)
    assert(ceil_alternative(7, 5) == 2)
    assert(ceil_alternative(7, 6) == 2)
    assert(ceil_alternative(7, 7) == 1)
    assert(ceil_alternative(7, 8) == 1)
    print(" * assertion test ok * ")