from typing import Tuple, Iterable
from itertools import combinations_with_replacement

def generate_increasing_seq(size: int, start: int, stop: int) -> Iterable[Tuple[int]]:
    """
    A = {Ai | start <= Ai < stop, Ai ∈ Z, Ai <= Aj (i < j)} (|A| = size) なる A を生成する
    (start 以上 stop -1 以下の size 個からなる広義単調増加部分列を生成するイテレータ)
    
    Args:
        size, start, stop (int)
    
    Returns:
        iter: start 以上 stop 未満の size 個からなる広義単調増加部分列 (タプル) を返すイテレータ

    Examples:
        >>> list(generate_increasing_seq(2, start=1, stop=4))
        [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
    
    Note:
        diff = stop - start
        0 ... stop - 1 - diff で指定の数列を生成して最後に全てに diff を足せば良い
        これは n = stop - 1 - diff として、n 個のボールと size 個の仕切りを並べた時に各仕切りの左側に存在するボールの個数と 1 対 1 対応する (n H size 通り存在) 
    """
    return combinations_with_replacement(range(start, stop), r=size)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(list(generate_increasing_seq(0, 2, 3)) == [tuple()])
    assert(list(generate_increasing_seq(1, 2, 3)) == [(2,)])
    assert(list(generate_increasing_seq(2, 2, 3)) == [(2, 2)])
    assert(list(generate_increasing_seq(3, 2, 3)) == [(2, 2, 2)])
    print(" * assertion test ok * ")
