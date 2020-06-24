def ceil_div_alternative(x: int, y: int) -> int:
    """
    y * m >= x なる最小の m, つまり ceil(x / y) を正確に返す

    Args:
        x, y (int)
    
    Returns:
        int: y * m >= x なる最小の m
    
    Raises:
        TypeError: x, y が int でないとき
        ValueError: x >= 0 かつ y > 0 でないとき

    Examples:
        >>> ceil_div_alternative(4, 2)
        2
        >>> ceil_div_alternative(4, 3)
        2
    
    Note:
        math.ceil(x / y) を用いて計算すると浮動小数点数のオーバーフローで正確な値が計算できないことに注意
        例えば math.ceil((2**53+1) / 2) は本来なら 2**52+1 のはずなのに 2**52 になってしまう (2**52 + 0.5 なる浮動小数点数を途中で経由しオーバーフローする)
    """
    if not (isinstance(x, int) and isinstance(y, int)):
        raise TypeError(f"ceil_div_alternative(): got non integer. got: {x} and {y}")
    if not (x >= 0 and y > 0):
        raise ValueError(f"ceil_div_alternative(): x should be >= 0, y shoud be > 0. got {x} and {y}")
    return (x + y - 1) // y



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(ceil_div_alternative(0, 1) == 0)
    assert(ceil_div_alternative(1, 1) == 1)
    assert(ceil_div_alternative(2, 1) == 2)
    assert(ceil_div_alternative(7, 3) == 3)
    assert(ceil_div_alternative(7, 4) == 2)
    assert(ceil_div_alternative(7, 5) == 2)
    assert(ceil_div_alternative(7, 6) == 2)
    assert(ceil_div_alternative(7, 7) == 1)
    assert(ceil_div_alternative(7, 8) == 1)
    assert(ceil_div_alternative(2**53+1, 2) == 2**52+1)    # 4503599627370497
    print(" * assertion test ok * ")