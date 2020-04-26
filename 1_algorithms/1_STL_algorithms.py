#!/usr/bin/env python3
"""
STL algorithms implemented in Python3 for programming competition


nth_element(seq, k):
    O(n)
    E = seq[k] とする
    特定の要素 E よりも小さい全ての要素が E よりも前になり、 E 以上の全ての要素がEよりも後になるようにシーケンスを並び替える
    heapq の nlargest とは異なるので注意


ith_order_statistic(seq, i):
    O(n)
    i 番目の順序統計量を求める
    これまた heapq の nlargest とは異なるので注意


stable_partition(seq):
    O(n)
    述語が True を返す全ての要素が、述語が False を返す全ての要素よりも前になるようにシーケンスを並び替える (安定)


他は対応する手法が自明なため省略。
"""



def nth_element(L, k, begin=None, end=None):
    """
    pivot = L[k] とする。 'pivot 未満の要素 ... pivot ... pivot 以上の要素' となるよう L を破壊的に並び替える。(O(n))
    最後に基準値の pivot がおさまった場所のインデックスを返す。
    begin <= k <= end の要請はあるが、begin, end の指定により L[begin:end+1] に対象を絞り L[k] 未満 / 以上に並べ替えることもできる。

    >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
    >>> nth_element(seq, 4)
    5
    >>> print(seq)
    [1, 2, 0, 4, 3, 5, 7, 8, 9, 6]
    >>> nth_element(seq, 3, begin=3, end=6)
    4
    >>> print(seq)
    [1, 2, 0, 3, 4, 5, 7, 8, 9, 6]

    Args:
        L (list)
        k (int): 0 origin
    Returns:
        int: 
    """
    n = len(L)
    if begin is None and end is None:
        begin = 0
        end = n - 1
    if not begin <= k <= end:
        raise RuntimeError(f"nth_element(): some bugs in indexing. k={k}, begin={begin}, end={end}.")

    pivot = L[k]
    L[k], L[end] = L[end], L[k]
    # i: 確定済みのバッファ先頭。ループ開始時点で pivot 未満であると判明しているところの先端を指す。
    i = begin - 1
    # j: 斥候。ループ開始時にここより前は検査済となっている。
    # begin ... end - 1 を動けば良い。(end は最初の swap の結果 pivot 自身がいるため探索しなくて良い)
    for j in range(begin, end):
        if L[j] < pivot:
            i += 1
            L[j], L[i] = L[i], L[j]
    L[i+1], L[end] = L[end], L[i+1]
    return i+1


def ith_order_statistic(L, i, begin=None, end=None):
    """
    O(n) で L の i 番目の順序統計量を求める
    begin, end は i 番目の順序統計量の候補が存在する範囲である。

    >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
    >>> ith_order_statistic(seq, 1) == sorted(seq)[0]
    True
    >>> ith_order_statistic(seq, 5) == sorted(seq)[4]
    True
    """
    import random

    if begin is None and end is None:
        begin = 0
        end = len(L) - 1
    if not begin <= i <= end:
        raise RuntimeError(f"ith_order_statistics(): some bugs in indexing. i={i}, begin={begin}, end={end}.")
    if begin == end:
        return L[begin]
    
    mid = nth_element(L, random.randint(begin, end), begin, end)
    if mid == i-1:
        return L[mid]
    elif mid < i-1:
        return ith_order_statistic(L, i, begin=mid, end=end)
    else:
        return ith_order_statistic(L, i, begin=begin, end=mid)



def stable_partition(L, func):
    """
    述語 func を True とする要素が前に、False とする要素が後ろに並ぶよう安定的かつ破壊的に L を並び替える。(O(n))
    False とする要素の開始インデックスを返す (存在しない場合 L の長さが返る)

    >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
    >>> stable_partition(seq, lambda x: x%2==0)
    5
    >>> seq
    [2, 6, 4, 8, 0, 1, 9, 7, 5, 3]

    Args:
        L (list)
    Returns:
        None
    """
    t_list = []
    f_list = []
    for elm in L:
        if func(elm):
            t_list.append(elm)
        else:
            f_list.append(elm)
    arranged = t_list + f_list
    for i in range(len(L)):
        L[i] = arranged[i]
    return len(t_list)



if __name__ == "__main__":
    import doctest
    doctest.testmod()