"""
(参考) <Algorithm Introduction vol.1 p.24-35, p.140-152, 177-180>
ソートテク関連の基本的な関数の詰め合わせ (命名は C++ STL algorithm による)


stable_partition(seq, func):
    O(n)
    空間計算量も O(n)
    述語が True を返す全ての要素が、述語が False を返す全ての要素よりも前になるようにシーケンスを並び替える (破壊、安定)


nth_element(seq, k, begin, end):
    O(n)
    E = seq[k] とする
    特定の要素 E よりも小さい全ての要素が E よりも前になり、 E 以上の全ての要素がEよりも後になるように seq[begin:end] を並び替える (破壊、不安定)
    heapq の nlargest とは異なるので注意


ith_order_statistic(seq, i, begin, end):
    O(n)
    nth_element を用いて (seq[begin:end] に存在することがわかっている) i 番目の順序統計量を求める (i = 0, 1, ..., n-1)


simple_quick_sort(seq, begin, end):
    O(nlgn)
    nth_element を用いて seq[begin:end] をソートする (破壊、不安定)


modified_merge_sort(seq, begin, end):
    O(nlgn)
    _modified_merge を用いて seq[begin:end] をソートする (非破壊、安定)
    転倒数とソート済み配列を返す


count_inversion(seq):
    O(nlgn)
    modified_merge_sort を用いて seq の転倒数を求める
    (転倒数: seq[i] > seq[j] (i < j) なる (i, j) の組み合わせの数のこと)
"""


import random
from typing import TypeVar, Callable, List, Tuple, Union

T = TypeVar('T')
Num = Union[int, float]



def stable_partition(L: List[T], func: Callable[[T], bool]) -> None:
    """
    O(n) で述語 func を True とする要素が前に、False とする要素が後ろに並ぶよう安定的かつ破壊的に L を並び替える。
    False とする要素の開始インデックスを返す。そのような要素が存在しない場合 L の長さを返す。

    Args:
        L (list)
        func (function)

    Examples:
        >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
        >>> stable_partition(seq, lambda x: x%2==0)
        5
        >>> seq
        [2, 6, 4, 8, 0, 1, 9, 7, 5, 3]
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



# verified @AOJ ALDS1_6_B
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_B&lang=ja
def nth_element(L: List[Num], pivot_ind: int, begin: int=-1, end: int=-1) -> int:
    """
    pivot = L[pivot_ind] とする。 O(n) で 'pivot 未満の要素 ... pivot ... pivot 以上の要素' となるよう L を破壊的に並び替える。
    最後に基準値の pivot がおさまった場所のインデックスを返す。
    begin <= pivot_ind < end の要請はあるが、begin, end の指定により L[begin:end] に対象を絞り L[pivot_ind] 未満 / 以上に並べ替えることもできる。

    Args:
        L (list)
        pivot_ind (int)
        begin, end (int): L の [begin, end) 半開区間を考える。デフォルトでは L[0:n] となる

    Returns:
        int: 最後に基準値の pivot がおさまった場所のインデックス

    Examples:
        >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
        >>> nth_element(seq, 4)
        5
        >>> seq
        [1, 2, 0, 4, 3, 5, 7, 8, 9, 6]
        >>> nth_element(seq, 3, begin=3, end=9)
        4
        >>> seq
        [1, 2, 0, 3, 4, 5, 7, 8, 9, 6]
    """
    if begin == -1 and end == -1:
        begin, end = 0, len(L)
    if not begin <= pivot_ind < end:
        raise RuntimeError(f"nth_element(): pivot_ind should be begin <= pivot_ind < end. got pivot_ind={pivot_ind}, begin={begin}, end={end}.")

    # [begin]...[end] が対象範囲である
    end -= 1
    pivot = L[pivot_ind]
    L[pivot_ind], L[end] = L[end], L[pivot_ind]
    # i: 確定済みのバッファ先頭。ループ開始時点で pivot 未満であると判明しているところの先端を指す。
    i = begin - 1
    # j: 斥候。ループ開始時にここより前は検査済となっている。
    # begin ... end - 1 を動けば良い。(end は最初の swap の結果 pivot 自身がいるため探索しなくて良い)
    for j in range(begin, end):
        if L[j] <= pivot:
            i += 1
            L[j], L[i] = L[i], L[j]
    L[i+1], L[end] = L[end], L[i+1]
    return i+1



def ith_order_statistic(L: List[Num], i: int, begin: int=-1, end: int=-1) -> Num:
    """
    O(n) で nth_element を用いて L の i 番目の順序統計量を求める (i = 0, 1, ..., n - 1)
    [begin, end) に i 番目の順序統計量が存在する

    Args:
        L (list)
        i (int): start from 0
        begin, end (int): [begin, end) に i 番目の順序統計量が存在する

    Returns:
        int: i 番目の順序統計量 (i = 0, 1, ..., n - 1) 

    Examples:
        >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
        >>> ith_order_statistic(seq, 0) == sorted(seq)[0]
        True
        >>> ith_order_statistic(seq, 4) == sorted(seq)[4]
        True
    """
    if begin == -1 and end == -1:
        begin, end = 0, len(L)
    if not begin <= i  < end:
        raise RuntimeError(f"ith_order_statistics(): i should be begin <= i < end. got i={i}, begin={begin}, end={end}.")
    
    if end - begin == 1:
        return L[begin]
    
    # pivot_ind は begin ... end -1 から選ばれてほしい
    mid = nth_element(L, random.randint(begin, end-1), begin, end)
    if mid == i:
        return L[mid]
    elif mid < i:
        return ith_order_statistic(L, i, begin=mid+1, end=end)
    else:
        return ith_order_statistic(L, i, begin=begin, end=mid)



# verified @AOJ ALDS1_6_C
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_C&lang=ja
def simple_quick_sort(L: List[Num], begin: int, end: int) -> None:
    """
    O(nlgn) で nth_element を用いて L[begin:end] を 破壊的に不安定でクイックソートする

    Args:
        L (list)
        begin, end (int)
    
    Examples:
        >>> seq = [3, 5, 2, 1, 0, 3]
        >>> simple_quick_sort(seq, 0, 6)
        >>> seq
        [0, 1, 2, 3, 3, 5]
    """
    if end - begin > 1:
        # pivot_ind は begin ... end -1 から選ばれてほしい
        mid = nth_element(L, random.randint(begin, end - 1), begin, end)
        simple_quick_sort(L, begin, mid)
        simple_quick_sort(L, mid+1, end)




def _modified_merge(left: List[Num], right: List[Num]) -> Tuple[int, List[Num]]:
    """
    O(n) でソート済み配列 left, right を受け取り、全体のソート済み配列を生成する
    マージの過程で転倒数をメモして返す

    Args:
        left (list): ソート済み
        right (list): ソート済み

    Returns:
        inv (int): 転倒数
        sorted_list (list): ソート済み
    
    Examples:
        >>> _modified_merge([1, 5, 7], [2, 3, 3])
        (6, [1, 2, 3, 3, 5, 7])
    """
    sorted_list = []
    i, j, inv = 0, 0, 0
    buf_1 = left[:] + [float('inf')]
    buf_2 = right[:] + [float('inf')]
    for _ in range(len(left) + len(right)):
        if buf_1[i] <= buf_2[j]:    # 値が同じなら安定性のために left のものが先に入るべき
            sorted_list.append(buf_1[i])
            i += 1
            inv += j
        else:
            sorted_list.append(buf_2[j])
            j += 1
    return inv, sorted_list



# verified @AOJ ALDS1_5_B
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_5_B&lang=ja
def modified_merge_sort(L, begin, end):
    """
    O(nlgn) で L[begin:end] を 非破壊的かつ安定にマージソートする
    マージソートの過程で転倒数をメモして返す

    Args:
        L (list)
        begin, end (int)
    
    Returns:
        inv (int): 転倒数
        sorted_list (list): ソート済み
    
    Examples:
        >>> modified_merge_sort([3, 5, 2, 1, 0], 0, 5)
        (9, [0, 1, 2, 3, 5])
    """
    if end - begin == 1:
        return 0, [L[begin]]
    mid = (begin + end) // 2
    left_inv_cnt, left = modified_merge_sort(L, begin, mid)
    right_inv_cnt, right = modified_merge_sort(L, mid, end)
    merge_inv_cnt, sorted_list = _modified_merge(left, right)
    return left_inv_cnt + right_inv_cnt + merge_inv_cnt, sorted_list



# verified @AOJ ALDS1_5_D
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_5_D&lang=jp
def count_inversion(L):
    """
    O(nlgn) で modified_merge_sort() を用いて L の要素の転倒数を求める

    Examples:
        >>> count_inversion([1, 9, 2, 7, 5, 6, 4, 8, 3, 0])
        26
    """
    cnt, _ = modified_merge_sort(L, 0, len(L))
    return cnt




if __name__ == "__main__":
    import doctest
    doctest.testmod()
