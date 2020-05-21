from itertools import product
def enum_all_summations(L):
    """
    L の任意個の要素を選択してできる部分集合の和を計算しリストにまとめて返す (O(n * 2^n))
    戻り値となるリストの長さは 2^n。和の値の重複を避けるには呼び出しもとで set に変換する

    >>> sorted(enum_all_summations([-1, 2, 3]))
    [-1, 0, 1, 2, 2, 3, 4, 5]

    Args:
        L (list)
    Returns:
        list
    """
    n = len(L)
    all_sums = []
    for pattern in product([True, False], repeat=n):
        all_sums.append(sum([L[i] for i in range(n) if pattern[i]]))
    return all_sums



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(enum_all_summations([]) == [0])
    assert(sorted(enum_all_summations([1])) == [0, 1])
    assert(sorted(enum_all_summations([-1, 1])) == [-1, 0, 0, 1])
    print(" * assertion test ok * ")
