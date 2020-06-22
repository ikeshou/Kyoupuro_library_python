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

Num = Union[int, float]



def enum_all_summations(L: Sequence[Num]) -> List[Num]:
    """
    L の任意個の要素を選択してできる部分集合 (2^n 通り) の和を計算しリストにまとめて返す (O(n * 2^n))
    何も選択しない場合の和は 0 と見なす
    和の値の重複を避けるには呼び出しもとで set に変換する必要がある

    Args:
        L (sequence)

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


def split_and_list(L: Sequence[Num], x: Num) -> Num:
    """
    L から部分和が x 以下で最大になるよう任意個 (0 個も含む) の要素を選ぶとき、その値を探索して返す。
    なお数列 L は全て正であるとする。
    Args:
        L (sequence)
        x (int)
    Returns:
        int
    """
    assert(all(map(lambda x: x>0, L)))
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
    L = [31, 15, 11, 20, 13, 8, 5, 9]
    assert(split_and_list(L, 3) == 0)
    assert(split_and_list(L, 7) == 5)
    assert(split_and_list(L, 8) == 8)
    assert(split_and_list(L, 9) == 9)
    assert(split_and_list(L, 10) == 9)
    assert(split_and_list(L, 30) == 30)
    assert(split_and_list(L, 62) == 62)
    assert(split_and_list(L, 100) == 99)
    print(" * assertion test ok * ")

