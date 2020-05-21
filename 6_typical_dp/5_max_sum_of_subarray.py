"""
最大部分配列問題

ある配列 L について sum(L[i:j]) が最大となるような (i, j) を全て求めその最大値も求める問題
部分列ではなく部分配列、連続性が必要なことに注意。（不連続で良いなら正のものを足し合わせればおしまい）

algorithm intro vol.1 p.58 のように O(nlgn) の分割統治解も構成できるが、DP により O(n) の解を構成できる
"""


def find_max_subarray(L):
    """
    O(N) で sum(L[i:j]) が最大となるような (i, j) (i < j) を O(n) で全て求め、その最大値も求める
    (L が全て非正の場合最大の要素 (<=0) が出力される)
    (購入しない、つまり i = j となるようなケースは考えない。このような場合は和は 0 となるとも見なせるので適宜 max(0, result) を取れば良い))
        - 定式化
        - min_dp[0] = inf
        - min_dp[i] = min(min_dp[i-1], accum[i-1])

    >>> find_max_subarray([1, -4, 3, -4, 1, 2])  # L[2:3] = [3], L[4:6] = [1, 2] なる部分列の和が 3 であり最大
    (3, [(2, 3), (4, 6)])

    Args:
        L (list)
    Returns:
        maximum (number)
        intervals (List[tuple])
    """
    n = len(L)
    # accum[i] = sum(L[0:i]) とする, accum[j]-accum[i] = sum(L[i:j]) である。
    accum = [0] * (n + 1)
    for i in range(n):
        accum[i+1] = accum[i] + L[i]
    
    # min_dp[i] = (accum[i] より前の要素での最小値)
    # min_indices[i] = (accum[i] より前の要素で最小を示した index のリスト)
    min_dp = [0] * (n + 1)
    min_indices = [[] for _ in range(n + 1)]

    min_dp[0] = float('inf')
    for i in range(1, n + 1):
        if min_dp[i - 1] < accum[i - 1]:
            min_dp[i] = min_dp[i - 1]
            min_indices[i] = min_indices[i - 1]
        elif min_dp[i - 1] == accum[i - 1]:
            min_dp[i] = min_dp[i - 1]
            min_indices[i] = min_indices[i - 1] + [i - 1]
        else:
            min_dp[i] = accum[i - 1]
            min_indices[i] = [i - 1]
    
    # 各 accum[j] について、profit[j] = accum[j] - min_dp[j] が sum(L[x:j]) (0<=x<j) の最大値となる (j: 固定)
    # もちろんこの profit の最大値が答えである
    profit = [0] * (n + 1)
    profit[0] = None
    max_profit = -float('inf')
    max_profit_j = []
    for j in range(1, n + 1):
        profit[j] = accum[j] - min_dp[j]
        if profit[j] > max_profit:
            max_profit = profit[j]
            max_profit_j = [j]
        elif profit[j] == max_profit:
            max_profit_j.append(j)
    
    intervals = []
    for j in max_profit_j:
        for i in min_indices[j]:
            intervals.append((i, j))
    
    return max_profit, intervals



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # all of elements are lt 0
    assert(find_max_subarray([-1, -2, -3, -4, -5]) == (-1, [(0, 1)]))
    # all of elements are 0
    assert(find_max_subarray([0, 0, 0]) == (0, [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]))
    # all of elements are 0 or negative
    assert(find_max_subarray([-1, -2, 0, -3, -4, 0]) == (0, [(2, 3), (5, 6)]))

    # general cases
    assert(find_max_subarray([13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]) == (43, [(7, 11)]))
    # end が被るものが出てくるパターン
    assert(find_max_subarray([3, 4, -10, 2, -2, 2, 5, -8]) == (7, [(0, 2), (3, 7), (5, 7)]))
    # start が被るものが出てくるパターン
    assert(find_max_subarray([3, -3, 3, 5]) == (8, [(0, 4), (2, 4)]))

    print(" * assertion test ok * ")
