#!/usr/bin/env python3
"""
STL algorithms implemented in Python3 for programming competition
と言いつつソートテク関連の基本的な関数の詰め合わせ


stable_partition(seq, func):
    O(n)
    空間計算量も O(n)
    述語が True を返す全ての要素が、述語が False を返す全ての要素よりも前になるようにシーケンスを並び替える (安定)


nth_element(seq, k):
    O(n)
    E = seq[k] とする
    特定の要素 E よりも小さい全ての要素が E よりも前になり、 E 以上の全ての要素がEよりも後になるようにシーケンスを並び替える
    heapq の nlargest とは異なるので注意


ith_order_statistic(seq, i):
    O(n)
    i 番目の順序統計量を求める
    これまた heapq の nlargest とは異なるので注意


count_inversion(seq):
    O(nlgn)
    seq の転倒数を求める
    (転倒数: seq[i] > seq[j] (i < j) なる (i, j) の組み合わせの数のこと)
"""


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
    if not begin <= i - 1 <= end:
        raise RuntimeError(f"ith_order_statistics(): some bugs in indexing. i={i}, begin={begin}, end={end}.")
    if begin == end:
        return L[begin]
    
    mid = nth_element(L, random.randint(begin, end), begin, end)
    if mid == i-1:
        return L[mid]
    elif mid < i-1:
        return ith_order_statistic(L, i, begin=mid+1, end=end)
    else:
        return ith_order_statistic(L, i, begin=begin, end=mid-1)



def simple_quick_sort(L, i, j):
    """
    nth_element 関数を用いて L[i:j] を O(nlgn) で破壊的に不安定でクイックソートする
    
    >>> seq = [3, 5, 2, 1, 0, 3]
    >>> simple_quick_sort(seq, 0, 6)
    >>> seq
    [0, 1, 2, 3, 3, 5]
    """
    if i + 1 >= j:
        # len(L[i:j]) <= 1 であり再帰の底となる
        return
    # nth_element の k, begin, end はインデックスを取っていることに注意 (スライスではない)
    import random
    begin, end = i, j - 1
    mid = nth_element(L, random.randint(begin, end), begin, end)
    simple_quick_sort(L, i, mid)
    simple_quick_sort(L, mid+1, j)




def modified_merge(left, right):
    """
    ソート済み配列 left, right を受け取り、 O(n) で全体のソート済み配列を生成する
    マージの過程で転倒数をメモして返す

    >>> modified_merge([1, 5, 7], [2, 3, 3])
    (6, [1, 2, 3, 3, 5, 7])

    Args:
        left (list)
        right (list)
    Returns:
        inv (int)
        sorted_list (list)
    """
    sorted_list = []
    i, j, inv = 0, 0, 0
    buf_1 = left[:] + [float('inf')]
    buf_2 = right[:] + [float('inf')]
    for _ in range(len(left) + len(right)):
        if buf_1[i] < buf_2[j]:
            sorted_list.append(buf_1[i])
            i += 1
            inv += j
        else:
            sorted_list.append(buf_2[j])
            j += 1
    return inv, sorted_list


def modified_merge_sort(L, i, j):
    """
    [i, j), つまりL[i:j] を O(nlgn) で非破壊的かつ安定にマージソートする
    マージソートの過程で転倒数をメモして返す
    
    >>> modified_merge_sort([3, 5, 2, 1, 0], 0, 5)
    (9, [0, 1, 2, 3, 5])

    Args:
        L (list)
        i (int)
        j (int)
    Returns:
        inv (int)
        sorted_list (list)
    """
    if i + 1 == j:
        # L[i:j+1] = [L[i]]
        return 0, [L[i]]
    mid = (i + j) // 2
    left_inv_cnt, left = modified_merge_sort(L, i, mid)
    right_inv_cnt, right = modified_merge_sort(L, mid, j)
    merge_inv_cnt, sorted_list = modified_merge(left, right)
    return left_inv_cnt + right_inv_cnt + merge_inv_cnt, sorted_list


def count_inversion(L):
    """
    O(nlgn) で L の要素の転倒数を求める

    >>> count_inversion([1, 9, 2, 7, 5, 6, 4, 8, 3, 0])
    26
    """
    cnt, _ = modified_merge_sort(L, 0, len(L))
    return cnt



if __name__ == "__main__":
    import doctest
    doctest.testmod()
