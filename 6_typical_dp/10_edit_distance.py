"""
編集距離 (レーベンシュタイン距離)

ある文字列 s, t が存在する (|s|=n, |t|=m)。 s に対し以下の操作を最小回数行い t へと変更する時の操作回数を編集距離という。(diff コマンドはこれらしい)
置換 (replace): 文字列の中の一文字を別な文字に置き換える
挿入 (insert): 文字列に一文字を挿入する
削除 (delete): 文字列から一文字を削除する
"""


def levenshtein_distance(s, t):
    """
    s に対し以下の操作を最小回数行い t へと変更する時の操作回数 (編集距離) を O(n) で求める
    置換 (replace): 文字列の中の一文字を別な文字に置き換える
    挿入 (insert): 文字列に一文字を挿入する
    削除 (delete): 文字列から一文字を削除する
    
        - 定式化
        - 上記 3 つのパターンを場合わけして比較するのみ (s を t に近づけたい！)
        - dp[0][j] = j, dp[i][0] = i
                                                s[i]をt[j]へ置換   s[i]削除    s[i+1]にt[j]挿入
        - dp[i+1][j+1] = (s[i] == t[j] のとき) min(dp[i][j], dp[i][j+1]+1, dp[i+1][j]+1)
                         (s[i] != t[j] のとき) min(dp[i][j]+1, dp[i][j+1]+1, dp[i+1][j]+1)

    Args:
        s (str)
        t (str)
    Returns:
        dp (list): dp[i][j] = (s[:i] と t[:j] の ld)
    """
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(n):
        for j in range(m):
            if s[i] == t[j]:
                dp[i+1][j+1] = min(dp[i][j], dp[i][j+1]+1, dp[i+1][j]+1)
            else:
                dp[i+1][j+1] = min(dp[i][j]+1, dp[i][j+1]+1, dp[i+1][j]+1)
    return dp


if __name__ == "__main__":
    assert(levenshtein_distance("algorithm", "altruistric")[9][11] == 7)
    assert(levenshtein_distance("moo", "moo")[3][3] == 0)
    assert(levenshtein_distance("acac", "acm")[4][3] == 2)
    assert(levenshtein_distance("hoge", "")[4][0] == 4)
    assert(levenshtein_distance("", "piyo")[0][4] == 4)
    assert(levenshtein_distance("", "")[0][0] == 0)
    print(" * assertion test ok * ")
    