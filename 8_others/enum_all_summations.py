from typing import List, Sequence, Union
from itertools import product

Num = Union[int, float]

def enum_all_summations(L: Sequence[Num]) -> List[Num]:
    """
    L の任意個の要素を選択してできる部分集合 (2^n 通り) の和を計算しリストにまとめて返す (O(n * 2^n))
    何も選択しない場合の和は 0 と見なす
    和の値の重複を避けるには呼び出しもとで set に変換する必要がある

    Args:
        L (list)

    Returns:
        list: L の任意個の要素を選択してできる部分集合の和を要素にもつリスト。長さは 2^n

    Examples:
        >>> sorted(enum_all_summations([-1, 2, 3]))
        [-1, 0, 1, 2, 2, 3, 4, 5]
    """
    n = len(L)
    all_sums = []
    for pattern in product([True, False], repeat=n):
        all_sums.append(sum([L[i] for i in range(n) if pattern[i]]))
    return all_sums



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # empty list
    assert(enum_all_summations([]) == [0])
    # list of int
    assert(sorted(enum_all_summations([1])) == [0, 1])
    assert(sorted(enum_all_summations([-1, 1])) == [-1, 0, 0, 1])
    # list of float
    assert(sorted(enum_all_summations([0.5, 1.0])) == [0, 0.5, 1.0, 1.5])
    print(" * assertion test ok * ")
