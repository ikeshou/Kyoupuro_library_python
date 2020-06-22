"""
<Algorithm Introduction vol.2 p.29>
最長共通部分列問題 (Longest Common Subsequence, LCS)

2 つの文字列の最長共通部分列およびその長さを計算する
(e.g.) abcdefg と cdeg の最長共通部分列は cdeg
愚直に計算すると指数時間かかるが、LCS の部分構造最適性を用いると DP により、二つの文字列の長さ m, n として O(m * n) で計算できる
"""


def calc_LongestCommonSequence(s, t):
    """
    2 つの文字列の最長共通部分列 (のうちの一つ) およびその長さを計算する
        - 定式化
        - dp[i][j] = 0 (i = 0 or j = 0)
        - dp[i][j] = dp[i-1][j-1] + 1 (i, j > 0 and s[i-1] = t[j-1])
        - dp[i][j] = max(dp[i-1][j], dp[i][j-1]) (i, j > 0 and s[i-1] != t[j-1])

    Args:
        s (str)
        t (str)
    Returns:
        dp (list): dp[i][j] = (s[:i], t[:j] の共通部分列のうち最長の長さ) (0<=i<=|s|, 0<=j<=|t|)
        reconstruct (list): reconstruct[i][j] = ('idecf', 'jdecf', 'i_and_j_decf' で遷移先が示される。'i_and_j_decf' は s[i-1] = t[j-1] のケースである)
    """
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    reconstruct = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                reconstruct[i][j] = 'i_and_j_decf'
            elif dp[i-1][j] >= dp[i][j-1]:
                dp[i][j] = dp[i-1][j]
                reconstruct[i][j] = 'idecf'
            else:
                dp[i][j] = dp[i][j-1]
                reconstruct[i][j] = 'jdecf'
    return dp, reconstruct


def reconstruct_LCS(table, s, t, n, m):
    """
    reconstruct テーブルをもとに s, t (|s|=n, |t|=m) の最長共通部分列を 1 つ復元して返す
    """
    ans = []
    i, j = n, m
    while i > 0 and j > 0:
        if table[i][j] == 'i_and_j_decf':
            ans.append(s[i-1])
            i -= 1
            j -= 1
        elif table[i][j] == 'idecf':
            i -= 1
        elif table[i][j] == 'jdecf':
            j -= 1
        else:
            raise RuntimeError(f"unknown marker. got {table[i][j]} (only idecf, jdecf, i_and_jdecf, i_or_j_decf are allowed.)")
    return ''.join(reversed(ans))



if __name__ == "__main__":
    s = "ABCBDAB"
    t = "BDCABA"
    dp, reconstruct = calc_LongestCommonSequence(s, t)
    assert(dp[7][6] == 4)
    assert(reconstruct_LCS(reconstruct, s, t, 7, 6) == 'BCBA')

    # 共通部分列なし
    dp2, reconstruct2 = calc_LongestCommonSequence('foof', 'barb')
    assert(dp2[4][4] == 0)
    assert(reconstruct_LCS(reconstruct2, 'foof', 'barb', 4, 4) == '')

    # そもそも空文字列
    dp3, reconstruct3 = calc_LongestCommonSequence('hoge', '')
    assert(dp3[4][0] == 0)
    assert(reconstruct_LCS(reconstruct3, 'hoge', '', 4, 0) == '')

    # |LCS| = 1
    dp4, reconstruct4 = calc_LongestCommonSequence('ch', 'bcaa')
    assert(dp4[2][4] == 1)
    assert(reconstruct_LCS(reconstruct4, 'ch', 'bcaa', 2, 4) == 'c')

    # 全て同じ
    dp5, reconstruct5 = calc_LongestCommonSequence('piyo', 'piyo')
    assert(dp5[4][4] == 4)
    assert(reconstruct_LCS(reconstruct5, 'piyo', 'piyo', 4, 4) == 'piyo')

    # 包含
    dp6, reconstruct6 = calc_LongestCommonSequence('bowwow', 'wow')
    assert(dp6[6][3] == 3)
    assert(reconstruct_LCS(reconstruct6, 'bowwow', 'wow', 6, 3) == 'wow')

    print(" * assertion test ok * ")
