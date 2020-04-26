#!/usr/bin/env python3
"""
尺取法

長さ n の数列 a_1, a_2, ..., a_n について
ある条件を満たす区間を O(n) で全て求めることができる。
    -> 条件を満たす区間のカウント、条件を満たす区間のうち k 番目の長さのものを求めるといったクエリに対応可能

条件の例：区間の総和が x 以下 / 以上、積和が x 以下 / 以上、単調増加・減少、値の重複がない、ある値以下の数が k 個以上存在 etc.

適用可能な条件の性質：
「区間 [left,right) が条件を満たす => それに含まれる区間も条件を満たす」(case 1)
or
「区間 [left,right) が条件を満たす => それを含む区間も条件を満たす」(case 2)


ポイント
半開区間 [left, right) で考える。
cf. python の slice. a[2:5] は区間 [a[2], a[5]) を表す。 *** 区間を数列の間の櫛ベースで考えると楽！ ***


左端を left に固定した時、条件を満たす右端 right は
case 1 の場合 left で始まる狭義単調増加数列となる。この最後の値を f(left) とすると、f は広義単調増加となる (case 1 の性質より)
case 2 の場合 n で終わる狭義単調増加数列となる。この最初の値を f(left) とすると、f は広義単調増加となる (case 2 の性質より)
ナイーブな実装をすると各 left に対し毎回 O(n) かけて {a_n} を走査する必要があったのが、
left で f(left)==x  であった (満足する right は left...x) 時、
left+1 では満足する right は left+1...x...y であるから f(left+1) を求める際に x+1 から走査を開始すれば良くなる。(自明な重複部分のスキップ)
"""


def scan_longest_interval_lt_eq_x(L, x):
    """
    L = {a_i | a_i >=0} とする
    a_1...a_n のうち、区間和が x 以下であるような区間を O(n) で探索する。
    満足する区間の数と、そのうち最長の区間全てのリストを返す

    >>> cnt, longest_intervals = scan_longest_interval_lt_eq_x([6,3,8,1,10], 12)
    >>> cnt
    10
    >>> longest_intervals
    [(1, 4)]
    """
    assert(all(map(lambda x:x>=0, L)))
    n = len(L)
    cnt = 0
    max_size = 0
    longest_intervals = []
    right_end = 0
    summation = 0
    for left in range(0, n):
        while right_end < n and summation + L[right_end] <= x:
            summation += L[right_end]
            right_end += 1
        # 終了時に summation は sum(L[left:right_end]) を表す。[left, right_end) は (left を左端に固定した時の) 最長インターバル
        size = right_end - left
        if max_size < size:
            max_size = size
            longest_intervals = [(left, right_end)]
        elif max_size == size:
            longest_intervals.append((left, right_end))
        cnt += size
        # 尺取りで完全に区間が潰れたら right_end も動かす
        if right_end == left:
            right_end += 1
        else:
            summation -= L[left]
    return cnt, longest_intervals


def scan_shortest_intervals_gt_eq_x(L, x):
    """
    L = {a_i | a_i >=0} とする
    a_1...a_n のうち、区間和が x 以上であるような区間を O(n) で探索する。
    満足する区間の数と、そのうち最長の区間全てのリストを返す

    >>> cnt, shortest_intervals = scan_shortest_intervals_gt_eq_x([6,3,8,1,10], 11)
    >>> cnt
    8
    >>> shortest_intervals
    [(1, 3), (3, 5)]
    """
    assert(all(map(lambda x:x>=0, L)))
    n = len(L)
    cnt = 0
    summation = 0
    min_size = float('inf')
    shortest_intervals = []
    right_start = 0
    for left in range(n):
        while right_start < n and summation < x:
            summation += L[right_start]
            right_start += 1
        # 終了時に summation は sum(a[left:right_start]) を表す。
        # [left, right_start) は (left を左端に固定した時の) 最短インターバル 'とは限らない'。満たすものが発見できずに末尾までくるパターンがある。
        # これは sum < x で判定可能。(right_start が末尾かどうかで判定してはダメ。summation < x => 末尾は真だけれど...)
        if summation < x:    # これ以上 left を進めても満たす区間は存在しない
            break
        size = right_start - left
        if min_size > size:
            min_size = size
            shortest_intervals = [(left, right_start)]
        elif min_size == size:
            shortest_intervals.append((left, right_start))
        # 上述の break 判定により必ず L[left:right_start] ... L[left:n] は必ず条件を満たす
        cnt += n - right_start + 1
        # 尺取りで完全に区間が潰れたら right_end も動かす
        if right_start == left:
            right_start += 1
        else:
            summation -= L[left]
    return cnt, shortest_intervals        
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    L_1 = [4, 6, 7, 8, 1, 2, 110, 2, 4, 12, 3, 9]
    cnt, longest_intervals = scan_longest_interval_lt_eq_x(L_1, 25)
    assert(cnt == 32)
    assert(longest_intervals == [(1, 6)])
    assert(L_1[longest_intervals[0][0]:longest_intervals[0][1]] == [6, 7, 8, 1, 2])

    L_2 = [4, 6, 7, 8, 1, 2, 110, 2, 4, 20, 3, 9]
    cnt, shortest_intervals = scan_shortest_intervals_gt_eq_x(L_2, 25)
    assert(cnt == 51)
    assert(shortest_intervals == [(6, 7)])
    assert(L_2[shortest_intervals[0][0]:shortest_intervals[0][1]] == [110])

    # test for empty list
    assert(scan_longest_interval_lt_eq_x([], 0) == (0, []))
    assert(scan_shortest_intervals_gt_eq_x([], 0) == (0, []))

    print(" * assertion test ok *")
    