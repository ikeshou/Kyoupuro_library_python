"""
<Algorithm Introduction vol.2 p.34>
最長増加部分列問題 (Longest Increase Subsequence, LIS)

ある配列 L について広義単調増加となる部分列を考える。
O(n^2) でその最長のものを 1 つ求め長さも計算する問題
O(nlgn) でその長さのみを計算する問題
"""


def calc_LongestIncreaseSubsequence(L):
    """
    L について広義単調増加となる部分列を考える。
    O(n^2) でその最長のものを 1つ 求め長さも計算する。
        - 定式化
        - dp[i] = (L[i] を末尾とする増加部分列の長さの最大値)
        - previous_ind[i] = (L[i] を末尾とする増加部分列の一つ前のインデックス。存在しない場合は None)
        - dp[0] = 1
        - dp[i] = max(dp[j] such that 0<=j<i-1 and L[j]<=L[i], 1)

    Args:
        L (list)
    Returns:
        dp (list)
        previous_ind (list) 
    """
    n = len(L)
    dp = [1] * n
    previous_ind = [None] * n
    for i in range(1, n):
        dp[i] = 1
        for j in range(i):
            if L[j] <= L[i] and dp[i] < dp[j] + 1:    # 狭義単調増加の時は L[j] < L[i] and ... にする
                dp[i] = dp[j] + 1
                previous_ind[i] = j
    return dp, previous_ind


def reconstruct_LIS(L, dp, previous_ind):
    """
    L, dp, previous_ind より最長増加部分列を 1 つ復元する
    """
    n = len(dp)
    if n == 0:
        return []
    buf = []
    ind = -1
    maximum = -float('inf')
    for i in range(n):
        if dp[i] > maximum:
            ind, maximum = i, dp[i]
    while ind is not None:
        buf.append(L[ind])
        ind = previous_ind[ind]
    return list(reversed(buf))



from bisect import bisect_left, bisect_right
def calc_LIS_size(L):
    """
    L について広義単調増加となる部分列を考える。
    O(nlgn) でその最長の長さのみを計算する。(具体的な LIS の再構築ができないというトレードオフあり)
        - 定式化
        - dp は一次元配列で使い回すことを考える (更新するべきところが各ループで高々一箇所しかないので)
        - dp[l-1]_i = (Ai までを使えるとき、増加部分列の長さ l の時の取りうる数列の末尾の最小値) とする
        - dp[l-1]_0 の初期値は inf
        - dp[l-1]_i は dp_i-1 に対し bisect_right(dp_i-1, Ai) を行い、得たインデックスに Ai を入れたもの
            - その性質より dp[l]_i は常に単調増加となる
            - 末尾の最小値が Ai を超えているようなものについては Ai を追加して IS を作ることはできぬ
            - 以下となる最初のものについては末尾に追加することにより、サイズを +1 増やして今までより末尾の要素の小さい IS を作ることができる
    Args:
        L (list)
    Returns:
        max_length (int)
    """
    n = len(L)
    dp = [float('inf')] * n
    for i in range(n):
        dp[bisect_right(dp, L[i])] = L[i]    # 狭義単調増加の時はここを bisect_left にする
        # print(dp)
    
    max_length = 0
    for i, elm in enumerate(dp):
        if elm == float('inf'):
            break
        # dp[i] までは少なくとも実数値が入っていた。長さ i + 1 の増加部分列に関しては末尾の要素を考えることができていた
        max_length = i + 1
    return max_length
            



if __name__ == "__main__":
    L = [1, 4, -2, -3, 5, 0]
    dp, prev_ind = calc_LongestIncreaseSubsequence(L)
    assert(max(dp) == 3)
    assert(dp == [1, 2, 1, 1, 3, 2])
    assert(reconstruct_LIS(L, dp, prev_ind) == [1, 4, 5])

    # for an empty list
    assert(calc_LongestIncreaseSubsequence([]) == ([], []))
    # length = 1
    assert(calc_LongestIncreaseSubsequence([7]) == ([1], [None]))
    # length = 2
    assert(calc_LongestIncreaseSubsequence([1, 2]) == ([1, 2], [None, 0]))
    assert(calc_LongestIncreaseSubsequence([2, 1]) == ([1, 1], [None, None]))
    # same value
    assert(calc_LongestIncreaseSubsequence([1, 1]) == ([1, 2], [None, 0]))


    assert(calc_LIS_size([1, 4, -2, -3, 5, 0]) == 3)
    assert(calc_LIS_size([1, 3, 5, 2, 4, 6]) == 4)
    assert(calc_LIS_size([]) == 0)
    assert(calc_LIS_size([7]) == 1)
    assert(calc_LIS_size([1, 2]) == 2)
    assert(calc_LIS_size([2, 1]) == 1)
    assert(calc_LIS_size([1, 1]) == 2)

    print(" * assertions test ok * ")