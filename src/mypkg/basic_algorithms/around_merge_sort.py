"""
(参考) <Algorithm Introduction vol.1 p.24-35, p.140-152, 177-180>
マージソートテク関連の基本的な関数の詰め合わせ


stable_partition(seq, func):
    O(n)
    空間計算量も O(n)
    述語が True を返す全ての要素が、述語が False を返す全ての要素よりも前になるようにシーケンスを並び替える (破壊、安定)


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
    if end - begin == 0:
        return 0, []
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
