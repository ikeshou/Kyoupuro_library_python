"""
<Algorithm Introduction vol.2 p.58>
ナップザック問題

n 個の品物があり、i 番目の品物のそれぞれ重さと価値が weight[i],value[i] (0 <= i <= n-1)


重さの総和が W 以下の範囲でそれぞれ 0 or 1 個選べるとき、価値を最大化せよ -> DP
重さの総和が W 以下の範囲でそれぞれ任意個選べるとき、価値を最大化せよ -> DP
重さの総和が W 以下の範囲でそれぞれ有理数個選べるとき、価値を最大化せよ -> 有理ナップザック問題。greedy に決まる。上の奴らの上界となる。
"""


def knapsack_01(weight, value, W):
    """
    n 個の品物があり、i 番目の品物のそれぞれ重さと価値が weight[i],value[i] (0 <= i <= n-1)
    重さの総和が W 以下の範囲でそれぞれ 0 or 1 個選べるとき、価値を最大化せよ (O(n * W))

    dp[i+1][w] = (n 個のうち最初の i 個を合計 w 以下で選んだ時の価値の最大値) とすれば
    dp[0][j] = 0
    dp[i][0] = 0
    dp[i+1][w] = max(dp[i][w], dp[i][w - weight[i]] + value[i]) if w - weight[i] >= 0 else dp[i][w]

    今回 w を昇順に逆向きで回すことで一次元配列を使い回すことが可能になる。
    (dp[i][j] -> dp[i+1][k] への遷移において常に j < k である場合配列を使いまわせる)
    """
    n = len(weight)
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, 0, -1):
            if w - weight[i] >= 0:
                dp[w] = max(dp[w], dp[w - weight[i]]+value[i])
    return dp[W]


def knapsack_int(weight, value, W):
    """
    n 個の品物があり、i 番目の品物のそれぞれ重さと価値が weight[i],value[i] (0 <= i <= n-1)
    重さの総和が W 以下の範囲でそれぞれ任意個選べるとき、価値を最大化せよ (O(n * W))

    dp[i+1][w] = (n 個のうち最初の i 個を合計 w 以下で選んだ時の価値の最大値) とすれば
    dp[0][j] = 0
    dp[i][0] = 0
    dp[i+1][w] = max(dp[i][w], dp[i+1][w - weight[i]] + value[i]) if w - weight[i] >= 0 else dp[i][w]
    """
    n = len(weight)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(n):
        for w in range(1, W + 1):
            if w - weight[i] >= 0:
                dp[i+1][w] = max(dp[i][w], dp[i+1][w - weight[i]] + value[i])
            else:
                dp[i+1][w] = dp[i][w]
    return dp[n][W]



if __name__ == "__main__":
    weight = [2, 1, 3, 2, 1, 5]
    value = [3, 2, 6, 1, 3, 85]
    assert(knapsack_01(weight, value, W=9) == 94)
    assert(knapsack_int(weight, value, W=9) == 97)
    print(" * assertion test ok * ")
