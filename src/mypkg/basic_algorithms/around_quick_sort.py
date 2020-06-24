"""
(参考) <Algorithm Introduction vol.1 p.24-35, p.140-152, 177-180>
クイックソートテク関連の基本的な関数の詰め合わせ (命名は C++ STL algorithm による)



randomized_select(seq, k, begin, end):
    O(n)
    E = seq[k] とする
    特定の要素 E よりも小さい全ての要素が E よりも前になり、 E 以上の全ての要素がEよりも後になるように seq[begin:end] を並び替える (破壊、不安定)


nth_element(seq, i, begin, end):
    O(n)
    randomized_select を用いて (seq[begin:end] に存在することがわかっている) i 番目の順序統計量を求める (i = 0, 1, ..., n-1)


quick_sort(seq, begin, end):
    O(nlgn)
    randomized_select を用いて seq[begin:end] をソートする (破壊、不安定)
"""



import random
from typing import TypeVar, Callable, List, Tuple, Union

T = TypeVar('T')
Num = Union[int, float]



# verified @AOJ ALDS1_6_B
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_B&lang=ja
def randomized_select(L: List[Num], pivot_ind: int, begin: int=-1, end: int=-1) -> int:
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
    
    Raises:
        IndexError: 0 <= begin <= pivot_ind < end <= len(L) でないとき

    Examples:
        >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
        >>> randomized_select(seq, 4)
        5
        >>> seq
        [1, 2, 0, 4, 3, 5, 7, 8, 9, 6]
        >>> randomized_select(seq, 3, begin=3, end=9)
        4
        >>> seq
        [1, 2, 0, 3, 4, 5, 7, 8, 9, 6]
    """
    if begin == -1 and end == -1:
        begin, end = 0, len(L)
    if not begin <= pivot_ind < end <= len(L):
        raise IndexError(f"randomized_select(): indices should be 0 <= begin <= pivot_ind < end <= len(L). got pivot_ind={pivot_ind}, begin={begin}, end={end}.")

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



def nth_element(L: List[Num], i: int, begin: int=-1, end: int=-1) -> Num:
    """
    O(n) で randomized_select を用いて L の i 番目の順序統計量を求める (i = 0, 1, ..., n - 1)
    [begin, end) に i 番目の順序統計量が存在する

    Args:
        L (list)
        i (int): start from 0
        begin, end (int): [begin, end) に i 番目の順序統計量が存在する

    Returns:
        int: i 番目の順序統計量 (i = 0, 1, ..., n - 1) 
    
    Raises:
        IndexError: 0 <= begin <= i < end <= len(L) でないとき

    Examples:
        >>> seq = [1, 9, 2, 7, 5, 6, 4, 8, 3, 0]
        >>> nth_element(seq, 0) == sorted(seq)[0]
        True
        >>> nth_element(seq, 4) == sorted(seq)[4]
        True
    """
    if begin == -1 and end == -1:
        begin, end = 0, len(L)
    if not 0 <= begin <= i < end <= len(L):
        raise IndexError(f"nth_element(): i should be 0 <= begin <= i < end <= len(L). got i={i}, begin={begin}, end={end}.")
    
    if end - begin == 1:
        return L[begin]
    
    # pivot_ind は begin ... end -1 から選ばれてほしい
    mid = randomized_select(L, random.randint(begin, end-1), begin, end)
    if mid == i:
        return L[mid]
    elif mid < i:
        return nth_element(L, i, begin=mid+1, end=end)
    else:
        return nth_element(L, i, begin=begin, end=mid)



# verified @AOJ ALDS1_6_C
# http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_C&lang=ja
def quick_sort(L: List[Num], begin: int, end: int) -> None:
    """
    O(nlgn) で randomized_select を用いて L[begin:end] を 破壊的に不安定でクイックソートする

    Args:
        L (list)
        begin, end (int)

    Raises:
        IndexError: 0 <= begin <= end <= len(L) でないとき
    
    Examples:
        >>> seq = [3, 5, 2, 1, 0, 3]
        >>> quick_sort(seq, 0, 6)
        >>> seq
        [0, 1, 2, 3, 3, 5]
    """
    if not 0 <= begin <= end <= len(L):
        raise IndexError(f"quick_sort(): begin and end should be 0 <= begin <= end <= len(L). got begin: {begin} end: {end}")
    if end - begin > 1:
        # pivot_ind は begin ... end -1 から選ばれてほしい
        mid = randomized_select(L, random.randint(begin, end - 1), begin, end)
        quick_sort(L, begin, mid)
        quick_sort(L, mid+1, end)
    



if __name__ == "__main__":
    import doctest
    doctest.testmod()
