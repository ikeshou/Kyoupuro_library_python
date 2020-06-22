"""
尺取法

<algorithm>
長さ n の数列 a_1, a_2, ..., a_n について
以下の条件 C を満たす区間を O(n) で全て求めることができる。
条件を満たす区間のカウント、条件を満たす区間のうち k 番目の長さのものを求めるといったクエリに対応可能。

    適用可能な条件 C の性質：
    「区間 [left,right) が条件を満たす => それに含まれる区間も条件を満たす」(case 1)
    「区間 [left,right) が条件を満たす => それを含む区間も条件を満たす」(case 2)

    条件の例：区間の総和が x 以下 / 以上、積和が x 以下 / 以上、単調増加・減少、値の重複がない、ある値以下の数が k 個以上存在 etc.



半開区間 [left, right) で考える。
左端を left に固定した時、条件を満たす右端 right は
case 1 の場合 left で始まる狭義単調増加数列となる。この最後の値を f(left) とすると、f は広義単調増加となる (case 1 の性質より)
case 2 の場合 n で終わる狭義単調増加数列となる。この最初の値を f(left) とすると、f は広義単調増加となる (case 2 の性質より)
各 left に対し f(left) を求めるには毎回 O(n) かけて {a_n} を走査する必要があったのが、f(left-1) を用いて自明な重複部分を飛ばして走査すれば十分になる
"""


from typing import List, Tuple, Union

Num = Union[int, float]



def intervals_lt_x(L: List[Num], x: Num) -> Tuple[int, int, List[Tuple[int]]]:
    """
    正の数列 L の全区間について、区間和が x 以下であるようなものを O(n) で探索する。
    満足する区間の数と、そのうち最長の区間のサイズ、最長の区間全てのリストを返す。

    Args:
        L (list)
        x (number)

    Returns:
        cnt (int): 区間和が x 以下であった区間の総数
        width (int): 最長の区間の幅
        longest_intervals (list): 最長の区間全てのリスト (半開区間)

    Examples:
        >>> intervals_lt_x([6, 3, 8, 1, 10], 12)
        (10, 3, [(1, 4)])
    """
    assert(all(map(lambda x:x>=0, L)))
    n = len(L)
    cnt, max_width, longest_intervals = 0, 0, []    # 満足する区間の数、そのうち最長の区間のサイズ、最長の区間全てのリストをここに保存して最後に返す
    right_end = 0
    summation = 0
    for left in range(0, n):
        # 終了時に summation は sum(L[left:right_end]) を表す。
        # [left, right_end) は (left を左端に固定した時の) 最長インターバルとなる。        
        while right_end < n and summation + L[right_end] <= x:
            summation += L[right_end]
            right_end += 1
        size = right_end - left
        # cnt への加算。[left:left] ... [left:right_end] が left を左端点とした時の条件を満たす区間である。
        cnt += size
        # max_width, logest_intervals のメモ
        if max_width < size:
            max_width = size
            longest_intervals = [(left, right_end)]
        elif max_width == size:
            longest_intervals.append((left, right_end))

        # 尺取りで完全に区間が潰れたら right_end も動かす
        if right_end == left:
            right_end += 1
        else:
            summation -= L[left]
    return cnt, max_width, longest_intervals



def intervals_gt_x(L: List[Num], x: Num) -> Tuple[int, int, List[Tuple[int]]]:
    """
    正の数列 L の全区間について、区間和が x 以上であるようなものを O(n) で探索する。
    満足する区間の数と、そのうち最短の区間のサイズ、最短の区間全てのリストを返す。

    Args:
        L (list)
        x (number)

    Returns:
        cnt (int): 区間和が x 以上であった区間の総数
        width (int): 最短の区間幅
        shortest_intervals (list): 最短の区間全てのリスト (半開区間)
    
    Examples:
        >>> intervals_gt_x([6, 3, 8, 1, 10], 11)
        (8, 2, [(1, 3), (3, 5)])
    """
    assert(all(map(lambda x:x>=0, L)))
    n = len(L)
    cnt, min_width, shortest_intervals = 0, float('inf'), []    # 満足する区間の数、そのうち最短の区間のサイズ、最短の区間全てのリストをここに保存して最後に返す
    summation = 0
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
        # cnt への加算。上述の break 判定により必ず L[left:right_start] ... L[left:n] が left を左端点とした時の条件を満たす区間である
        cnt += n - right_start + 1
        # min_width, shortest_intervals のメモ
        if min_width > size:
            min_width = size
            shortest_intervals = [(left, right_start)]
        elif min_width == size:
            shortest_intervals.append((left, right_start))

        # 尺取りで完全に区間が潰れたら right_end も動かす
        if right_start == left:
            right_start += 1
        else:
            summation -= L[left]
    return cnt, min_width, shortest_intervals        
        



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    L_1 = [4, 6, 7, 8, 1, 2, 110, 2, 4, 12, 3, 9]
    cnt, width, longest_intervals = intervals_lt_x(L_1, 25)
    assert(cnt == 32)
    assert(width == 5)
    assert(longest_intervals == [(1, 6)])
    assert(L_1[longest_intervals[0][0]:longest_intervals[0][1]] == [6, 7, 8, 1, 2])

    L_2 = [4, 6, 7, 8, 1, 2, 110, 2, 4, 20, 3, 9]
    cnt, width, shortest_intervals = intervals_gt_x(L_2, 25)
    assert(cnt == 51)
    assert(width == 1)
    assert(shortest_intervals == [(6, 7)])
    assert(L_2[shortest_intervals[0][0]:shortest_intervals[0][1]] == [110])

    # test for empty list
    assert(intervals_lt_x([], 0) == (0, 0, []))
    assert(intervals_gt_x([], 0) == (0, float('inf'), []))

    print(" * assertion test ok *")
    