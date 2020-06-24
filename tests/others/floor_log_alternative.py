def floor_log_alternative(x: int, y: int) -> int:
    """
    y ^ m <= x なる最大の整数 m, つまり floor(log(x, y)) を正確に返す
    なお、x は s^100 ≒ 10^30 未満であると仮定している

    Args:
        x, y (int)

    Returns:
        int: y ^ m <= x なる最大の整数 m
    
    Raises:
        TypeError: x, y が int でないとき
        ValueError: x >= 1 かつ y > 1 でないとき        

    Examples:
        >>> floor_log_alternative(9**5-1, 9)
        4
        >>> floor_log_alternative(9**5, 9)
        5
        >>> floor_log_alternative(9**5+1, 9)
        5

    Note:
        math.floor(math.log(x, y)) を用いて計算すると浮動小数点数の誤差で正確に計算できないことに注意
        例えば math.log(9**5, 9) は本来なら 5 のはずなのに 4.9999 になってしまうため floor により 4 に切り捨てられてしまう
    """
    if not (isinstance(x, int) and isinstance(y, int)):
        raise TypeError(f"floor_log_alternative(): got non integer. got: {x} and {y}")
    if not (x >= 1 and y > 1):
        raise ValueError(f"floor_log_alternative(): x should be >= 1, y shoud be > 1. got {x} and {y}")
    left = -1
    right = 100    # 2^100 > 10^30. さすがにこれを超えることはないはず
    while right - left > 1:
        mid = (right + left) // 2
        if pow(y, mid) > x:
            right = mid
        else:
            left = mid
    return left



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(floor_log_alternative(1, 2) == 0)
    assert(floor_log_alternative(1, 10) == 0)
    assert(floor_log_alternative(999, 1000) == 0)
    assert(floor_log_alternative(999, 999) == 1)
    assert(floor_log_alternative(999, 998) == 1)
    assert(floor_log_alternative(1000, 2) == 9)
    assert(floor_log_alternative(1023, 2) == 9)
    assert(floor_log_alternative(1024, 2) == 10)
    assert(floor_log_alternative(1025, 2) == 10)
    print(" * assertion test ok * ")

