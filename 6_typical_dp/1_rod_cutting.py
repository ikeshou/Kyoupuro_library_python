"""
ロッド切り出し問題

ロッドの長さ i と価格 pi の対応表が与えられる。指定された長さのロッドを販売する時の最適な切り出し方と売値を求める問題
典型的な 1 次元 DP

(e.g.)
長さ i    1   2   3   4   5   6   7   8   9   10
価格 pi   1   5   8   9   10  17  17  20  24  30 
長さ 4 の場合は 2 - 2 に分割して価格 10 で売るのが最適である
"""


def rod_cutting_dp(prices):
    """
    ロッドの長さ i と価格 pi の対応表が与えられる。
    指定された長さのロッドを販売する時の最適な切り出し方と売値を O(n^2) で求める
        - 定式化
        - dp[0] = 0
        - dp[i] = max(prices[k] + dp[i-k] (1<=∀k<=i))

    >>> prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    >>> dp, reconstruct = rod_cutting_dp(prices)
    >>> dp
    [0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    >>> reconstruct
    [None, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10]

    Args:
        prices (list): ロッドの長さ i と価格 pi の対応表。長さ i の価格が prices[i] に登録されているものとする (prices[0] = 0 とする)
    Returns:
        dp (list): dp[i] = (長さ i の売値の最大値)
        reconstruct (list): restruncre[i] = (長さ i を x と i - x に分割する時の最適な分割位置 x)
    """
    assert(prices[0] == 0)
    n = len(prices)
    dp = [0] * n
    reconstruct = [None] * n
    for i in range(1, n):
        dp[i] = -float('inf')
        # 長さ i を長さ j (これ以上分割しない), i - j に二分割する
        for j in range(1, i + 1):
            profit = prices[j] + dp[i - j]
            if dp[i] < profit:
                dp[i] = profit
                reconstruct[i] = j
    return dp, reconstruct


def reconstruct_cut_pos(table):
    """
    reconstruct テーブルをもとに長さ i の棒の切り出し方を再構成する
    再帰でもいいが、効率化するなら各 i に対し再構成した結果 (list) を保存したリストをボトムアップに作ろう

    >>> reconstruct_table = [None, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10]
    >>> reconstruct_cut_pos(reconstruct_table)
    [[], [1], [2], [3], [2, 2], [3, 2], [6], [6, 1], [6, 2], [6, 3], [10]]
    """
    n = len(table)
    cut_pos = [[] for _ in range(n)]
    for i in range(1, n):
        cut_pos[i] = cut_pos[i - table[i]] + cut_pos[table[i]] if i != table[i] else [i]
    return cut_pos


if __name__ == "__main__":
    import doctest
    doctest.testmod()
