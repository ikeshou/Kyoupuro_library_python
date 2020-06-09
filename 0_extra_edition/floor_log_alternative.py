from math import log
def floor_log_alternative(x, y):
    """
    Args:
        x, y (int)
    Returns:
        int

    floor(log(x, y)) を正確に返す (最大で y を何整数乗するまでは x 以下ですむか？の値。y ^ m <= x なる最大の整数 m)

    >>> floor_log_alternative(9**5-1, 9)
    4
    >>> floor_log_alternative(9**5, 9)
    5
    >>> floor_log_alternative(9**5+1, 9)
    5

    > log(9**5-1, 9)
    4.99999229244412    # 9 を 5 乗すると x を超えてしまう。floor で 4 となる
    > log(9**5, 9)
    4.999999999999999    # これは正確に 5 になって欲しいが、誤差により 5 より若干小さくなってしまう。floor で 4 にされる...
    > log(9**10, 9)
    9.999999999999998

    基本的にこの代替関数を使用するようにする。
    ちなみに float を介した瞬間に overflow しうるため candidate = int(log(x, y)) として candidate if pow(y, candidate + 1) != x else candidate + 1 と返すのは駄目
    """
    assert (isinstance(x, int) and isinstance(y, int))
    assert (x >= 1 and y > 1)
    left = -1    # left は常に条件を満足する
    right = 100    # 2^100 > 10^30. さすがにこれを超えることはないはず。right は常に条件を破る
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

