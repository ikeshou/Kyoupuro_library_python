"""
<Algorithm Introduction vol.2 p.41>
最長回文部分列問題

文字列 s (|s| = n) の部分列 (部分文字列ではない) について、O(n^3) で最長の回文を求め、長さを計算する
LCS を内部で用いる
因みに回文は言葉遊び的な意味以外に遺伝子工学とかで重要な概念らしい 
(パリンドローム配列という DNA/RNA 分子内の核酸配列が有名。回文構造を持つとヘアピンを形成できる)
"""


def calc_longest_palindrome_subsequence(s):
    """
    文字列 s (|s| = n) の部分列 (部分文字列ではない) について、O(n^3) で最長の回文を 1 つ求め、長さを計算する

    Args:
        s (str)
    Returns:
        size (int)
        palindrome_memo (str)
    """
    n = len(s)
    l_s = list(s)
    max_size = 0
    palindrome_memo = ''
    # 偶数長のものについての調査
    for i in range(1, n):
        left, right = l_s[:i], list(reversed(l_s[i:]))
        dp, table = calc_LongestCommonSequence(left, right)
        if 2 * dp[i][n-i] > max_size:
            max_size = 2 * dp[i][n-i]
            lcs = reconstruct_LCS(table, left, right, i, n - i)
            palindrome_memo = lcs + lcs[::-1]
    # 奇数長のものについての調査
    for i in range(n):
        left, right = l_s[:i], list(reversed(l_s[i+1:]))
        dp, table = calc_LongestCommonSequence(left, right)
        if 2 * dp[i][n-i-1] + 1 > max_size:
            max_size = 2 * dp[i][n-i-1] + 1
            lcs = reconstruct_LCS(table, left, right, i, n - i - 1)
            palindrome_memo = lcs + s[i] + lcs[::-1]
    return max_size, palindrome_memo



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
            raise RuntimeError(f"unknown marker.  got {table[i][j]} (only idecf, jdecf, i_and_jdecf, i_or_j_decf are allowed.)")
    return ''.join(reversed(ans))



if __name__ == "__main__":
    assert(calc_longest_palindrome_subsequence("character") == (5, "carac"))
    assert(calc_longest_palindrome_subsequence("hoge") == (1, "h"))
    assert(calc_longest_palindrome_subsequence("civic") == (5, "civic"))
    print(" * assertion test ok * ")