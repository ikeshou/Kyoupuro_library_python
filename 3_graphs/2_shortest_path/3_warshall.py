"""
<Algorithm Introduction p.282-288>
Warshall-Floyd 法 (O(V^3), 1 sec だと v~500 とかが限界)
全点対間の最短経路を DP で求める

3次元 DP
dp[k+1][i][j] を 0...k, i, j なる頂点を使用できる時の i~j 最短距離とする (k+1=0 の時は e(i,j))
dp[k+1][i][j] = min(dp[k][i][j], dp[k][i][k+1]+dp[k][k+1][j])
最後に必要なのは dp[V][i][j] 。
上の漸化式をみるに 2 次元 array があれば使いまわしてメモリ節約できる
(最低限 dp[i][j] の新旧二枚のテーブルのメモがあれば壊れないことは自明。
しかし一枚で逐次更新となると dp[k+1][i][j] 更新中に dp[k][i][k], dp[k][k][j] の値を変更してしまわないか？
-> 大丈夫
dp[k+1][i][k+1] = min(dp[k][i][k+1], dp[k][i][k+1] + dp[k][k+1][k+1] (=0)))
                = dp[k][i][k+1]
同様に
dp[k+1][k+1][j] = dp[k][k+1][j]
つまり使い回しの結果 dp[k+1][i][k+1] がすでに dp[k][i][k+1] の参照場所を更新しようとしてしまっていても、実際に更新は行われない (値が等しいので)
"""


from copy import deepcopy

def warshall_floyd(adj_mat_with_weight):
    ' dp[i][j] を見れば全頂点を使用可能な時の i j 最短距離がわかる。最後に dp[i][i] が負になっていたら負サイクルが存在するということ'
    V = len(adj_mat_with_weight)
    # テーブル初期化
    dp = deepcopy(adj_mat_with_weight)
    for i in range(V):
        dp[i][i] = 0
    # 漸化式を解く
    for k in range(1, V+1):
        for i in range(V):
            for j in range(V):
                # new 2d-table # old 2d-table
                dp[i][j] = min(dp[i][j], dp[i][k-1]+dp[k-1][j])
    return dp



if __name__ == "__main__":
    INF = float('inf')
    adj = [[INF, 5, 6, INF, INF, INF, INF, INF, INF, INF],
           [5, INF, INF, INF, 2, INF, INF, INF, INF, INF],
           [6, INF, INF, 2, INF, 4, INF, INF, INF, INF],
           [INF, INF, 2, INF, INF, INF, 1, INF, INF, INF],
           [INF, 2, INF, INF, INF, 3, INF, 7, INF, INF],
           [INF, INF, 4, INF, 3, INF, INF, INF, 1, INF],
           [INF, INF, INF, 1, INF, INF, INF, INF, INF, INF],
           [INF, INF, INF, INF, 7, INF, INF, INF, INF, INF],
           [INF, INF, INF, INF, INF, 1, INF, INF, INF, 1],
           [INF, INF, INF, INF, INF, INF, INF, INF, 1, INF]]
    cost_ij = warshall_floyd(adj)
    for line in cost_ij:
        print(line)
    """
    [0, 5, 6, 8, 7, 10, 9, 14, 11, 12]
    [5, 0, 9, 11, 2, 5, 12, 9, 6, 7]
    [6, 9, 0, 2, 7, 4, 3, 14, 5, 6]
    [8, 11, 2, 0, 9, 6, 1, 16, 7, 8]
    [7, 2, 7, 9, 0, 3, 10, 7, 4, 5]
    [10, 5, 4, 6, 3, 0, 7, 10, 1, 2]
    [9, 12, 3, 1, 10, 7, 0, 17, 8, 9]
    [14, 9, 14, 16, 7, 10, 17, 0, 11, 12]
    [11, 6, 5, 7, 4, 1, 8, 11, 0, 1]
    [12, 7, 6, 8, 5, 2, 9, 12, 1, 0]
    """
    
