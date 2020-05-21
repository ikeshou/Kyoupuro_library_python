#!/usr/bin/env python3
"""
いわゆる半分全列挙 (Split and List, Meet in the Middle という)

全探索はきついが半分の全探索は可能なとき、全体を A, B の 2 グループに分けてそれぞれ全探索を行い、A の要素に対して B を工夫して探索する。
クエリが A を固定したとき B を二分探索すれば済むようなものの場合、
(e.g. 数列 {a_n} の元から適当に k 個を選んでいいとき、x 以下となる最大の部分和を答えよ)
愚直に全探索すると O(2^N)
半分全列挙を行い、B に対してソート & 二分探索を行うと O(NlgN) + O(2^(N/2)) * O(lg(2^(N/2))) = O(2^(N/2)) * O(N)

N~40 とかだと 2^20 ≒ 10^6 より半分全探索が通ることが多い
"""


from bisect import bisect_right
from itertools import accumulate


#### 連続でない要素を取りたい場合 sum(A0, A3) などが考慮されてないです
#### product でしっかり全列挙しましょう... (TODO)
def make_all_summation_set(accum_list):
    """
    split_and_list() の内部で使用する関数。ある数列の累積和のリストをもとに、その数列の任意個 (0 個も含む) の要素を選んだときに取りうる値の集合を返す。
    """
    group = set()
    m = len(accum_list)
    # [left, right) の和を考える。 accum[i] = [0, i) の和となって欲しいので、先頭に [0] を追加して L[0:0] = 0 となるようにする
    accum_list = [0] + accum_list
    for left in range(0, m):
        for right in range(left, m+1):
            group.add(accum_list[right] - accum_list[left])
    return group


def split_and_list(L, x):
    """
    L から部分和が x 以下で最大になるよう任意個 (0 個も含む) の要素を選ぶとき、その値を探索して返す。
    なお数列 L は全て正であるとする。
    Args:
        L (list)
        x (int)
    Returns:
        int
    """
    assert(all(map(lambda x: x>0, L)))
    n = len(L)
    mid = n // 2
    L_1, L_2 = L[:mid], L[mid:]
    accum_L_1, accum_L_2 = list(accumulate(L_1)), list(accumulate(L_2))
    group_A, group_B = sorted(make_all_summation_set(accum_L_1)), sorted(make_all_summation_set(accum_L_2))
    # print(group_A)
    # print(group_B)
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
    assert(split_and_list(L, 62) == 62)
    assert(split_and_list(L, 10) == 9)
    assert(split_and_list(L, 30) == 29)
    print(" * assertion test ok * ")

