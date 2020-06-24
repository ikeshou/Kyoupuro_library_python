"""
最長共通部分文字列問題 (Longest Common Substring, LCS)

2 つの文字列の最長共通部分文字列 (部分列ではない！) およびその長さを計算する
(e.g.) abcdefg と cdeg の最長共通部分文字列は cde (cdeg ではない！)
愚直に計算すると指数時間かかるが、LCS の部分構造最適性を用いると DP により、二つの文字列の長さ m, n として O(m * n) で計算できる
"""


def calc_LongestCommonSubstring(s, t):
    """
    2 つの文字列最長共通部分文字列 (部分列ではない！) およびその長さを計算する
        - 定式化
        - dp[0][j] = 0, dp[i][0] = 0
        - dp[i+1][j+1] = dp[i][j] + 1 if s[i] == t[j] else 0

    Args:
        s (str)
        t (str)
    Returns:
        dp (list): dp[i+1][j+1] = (s[i] == t[j] の時 s[i], t[j] は共通部分文字列の何文字目か)
    """
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            dp[i+1][j+1] = dp[i][j] + 1 if s[i] == t[j] else 0
    return dp


def reconstruct_LCS(s, t, dp):
    """
    dp テーブルから最長共通部分文字列全てを求める
    """
    n, m = len(s), len(t)
    max_size = 1
    i_memo = []
    for i in range(1, n+1):
        for j in range(1, m+1):
            if dp[i][j] > max_size:
                max_size, i_memo = dp[i][j], [i]
            elif dp[i][j] == max_size:
                i_memo.append(i)
    return [s[i-max_size:i] for i in i_memo]



if __name__ == "__main__":
    s = "ABCBDAB"
    t = "BDCABA"
    dp = calc_LongestCommonSubstring(s, t)
    assert(reconstruct_LCS(s, t, dp) == ["AB", "BD", "AB"])
    
    # 共通部分文字列なし
    s2 = "aaa"
    t2 = "bbb"
    assert(reconstruct_LCS(s2, t2, calc_LongestCommonSubstring(s2, t2)) == [])

    # そもそも空文字列
    s3 = "muscle"
    t3 = ""
    assert(reconstruct_LCS(s3, t3, calc_LongestCommonSubstring(s2, t2)) == [])

    # |LCS| = 1
    s4 = "ABC"
    t4 = "AGC"
    assert(reconstruct_LCS(s4, t4, calc_LongestCommonSubstring(s4, t4)) == ["A", "C"])

    # 全て同じ
    s5 = "piyo"
    t5 = "piyo"
    assert(reconstruct_LCS(s5, t5, calc_LongestCommonSubstring(s5, t5)) == ["piyo"])

    # 包含
    s6 = "bowwow"
    t6 = "wow"
    assert(reconstruct_LCS(s6, t6, calc_LongestCommonSubstring(s6, t6)) == ["wow"])

    print(" * assertion test ok * ")
