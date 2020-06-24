"""
いわゆる半分全列挙 (Split and List, Meet in the Middle という)

<algorithm>
全探索はきついが半分の全探索は可能なとき、全体を A, B の 2 グループに分けてそれぞれ全探索を行い、A の要素に対して B を工夫して探索する。
クエリが A を固定したとき B を二分探索すれば済むようなものの場合、
(e.g. 数列 {a_n} の元から適当に k 個を選んでいいとき、x 以下となる最大の部分和を答えよ)
愚直に全探索すると O(2^N)
半分全列挙を行い、B に対してソート & 二分探索を行うと O(NlgN) + O(2^(N/2)) * O(lg(2^(N/2))) = O(2^(N/2)) * O(N)

N~40 とかだと 2^20 ≒ 10^6 より半分全探索が通ることが多い
"""


from itertools import product
from bisect import bisect_right
from typing import List, Sequence, Union
from ..others.enum_all_summations import enum_all_summations

Num = Union[int, float]



def split_and_list(L: Sequence[Num], x: Num) -> Num:
    """
    L から部分和が x 以下で最大になるよう任意個 (0 個も含む) の要素を選ぶとき、その値を探索して返す。
    なお数列 L は全て 0 以上、x も 0 以上であるとする。(正でない場合 x が負の時解が存在しない場合がある)

    Args:
        L (sequence)
        x (int)

    Returns:
        int
    
    Examples:
        >>> split_and_list([1, 3, 5, 7], 20)    # 1 + 3 + 5 + 7 = 16
        16
        >>> split_and_list([1, 3, 5, 7], 10)    # 3 + 7 = 10
        10
    """
    assert all(map(lambda x: x>=0, L))
    assert x >= 0
    n = len(L)
    mid = n // 2
    L_left, L_right = L[:mid], L[mid:]
    group_A, group_B = sorted(set(enum_all_summations(L_left))), sorted(set(enum_all_summations(L_right)))
    ans = 0
    for elm_A in group_A:
        res = x - elm_A
        if res < 0:
            break
        candidate_ind = bisect_right(group_B, res) - 1    # res 「以下」最大の値を探したいので bisect_right
        ans = max(ans, elm_A + group_B[candidate_ind])
    return ans



if __name__ == "__main__":
    import doctest
    doctest.testmod()


