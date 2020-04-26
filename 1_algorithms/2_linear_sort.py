#!/usr/bin/env python3
"""
Counting sort and radix sort implemented in Python3 for programming competition

counting_sort(seq, k, key_func):
    O(n + k)
    seq を安定的かつ非破壊的に計数ソートする (但し seq は 0...k をとるとする)

counting_sort_destructive(seq, k, key_func):
    O(n + k)
    seq を安定的かつ破壊的に計数ソートする (但し seq は 0...k をとるとする)

radix_sort(seq):
    O(d * (n + k))
    seq を安定的かつ非破壊的に基数ソートする (但し 各桁は 0...k をとるとする、 d は桁数)
"""


def counting_sort(L, k, key=lambda x: x):
    """
    O(n + k) で L を安定的かつ非破壊的に計数ソートする
    >>> seq = [1, 3, 5, 10, 4, 6, 15, 7, 2, 0] 
    >>> counting_sort(seq, 15)    # 0 to 15
    [0, 1, 2, 3, 4, 5, 6, 7, 10, 15]

    Args:
        L (list)
        k (int): L の要素は 0 to k であると仮定する
    Returns:
        list: sorted
    """
    n = len(L)
    accum_sum_memo = [0] * (k+1)    # 0 to k なので
    count_sorted = [0] * n

    for i in range(0, n):
        accum_sum_memo[key(L[i])] += 1
    for i in range(1, k+1):
        accum_sum_memo[i] = accum_sum_memo[i-1] + accum_sum_memo[i]

    for j in range(n-1, -1, -1):
        count_sorted[accum_sum_memo[key(L[j])] - 1] = L[j]
        accum_sum_memo[L[j]] -= 1    # 同じ値のものが来た時、一つ前の位置におさまるように調節してやる

    return count_sorted


def counting_sort_destructive(L, k, key=lambda x: x):
    """
    counting_sort() の破壊関数版
    >>> seq = [1, 3, 5, 10, 4, 6, 15, 7, 2, 0] 
    >>> counting_sort_destructive(seq, 15)    # 0 to 15
    >>> seq
    [0, 1, 2, 3, 4, 5, 6, 7, 10, 15]
    """
    n = len(L)
    accum_sum_memo = [0] * (k+1)    # 0 to k なので

    for i in range(0, n):
        accum_sum_memo[key(L[i])] += 1
    for i in range(1, k+1):
        accum_sum_memo[i] = accum_sum_memo[i-1] + accum_sum_memo[i]
    
    tmp = tuple(L[:])    # 変更されてはならない！
    for j in range(n-1, -1, -1):
        L[accum_sum_memo[key(tmp[j])] - 1] = tmp[j]
        accum_sum_memo[key(tmp[j])] -= 1    # 同じ値のものが来た時、一つ前の位置におさまるように調節してやる



def radix_sort(L_str):
    """
    O(d * (n + k)) で L_str を安定的かつ非破壊的に基数ソートする
    ここでは 10 進数表記の文字列のリストを受け取ること想定しているため、d = log10(k), k = 10
    >>> seq = ["4321", "5500", "8686", "5586", "1234", "1235", "0", "24", "7", "1000000007"]
    >>> radix_sort(seq)
    ['0', '7', '24', '1234', '1235', '4321', '5500', '5586', '8686', '1000000007']

    Args:
        L_str (list[str]): 各数値が 10 進数表記の文字列で表されたリスト
    Returns:
        list: sorted
    """
    # empty だと max の引数が [] になり困るのでチェック
    if L_str != []:
        max_digit = max(map(len, L_str))
        filled = ['0'*(max_digit-len(elm))+elm for elm in L_str]
        
        for digit in range(max_digit-1, -1, -1):
            counting_sort_destructive(filled, 9, key=lambda x: int(x[digit]))    # k = 0 to 9
        
        # '00000' といったものの処理に注意。単に 0 を取り除くだけではだめ
        return list(map(lambda x: x.lstrip('0') if not all(map(lambda x: x == '0', x)) else '0', filled))



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(counting_sort([], 0) == [])
    assert(counting_sort([100], 100) == [100])
    tmp = []
    radix_sort(tmp)
    assert(tmp == [])
    tmp_2 = ['100']
    radix_sort(tmp_2)
    assert(tmp_2 == ['100'])
    print(" * assertion test ok * ")