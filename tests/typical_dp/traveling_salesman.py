"""
巡回セールスマン問題 (Travelling Salesman Problem, TSP)

都市の集合と各2都市間の移動コストが与える。全ての都市をちょうど一度ずつ巡り出発地に戻る巡回路 (ハミルトン閉路) のうちで総移動コストが最小のものを求める
"""


def solve_TSP(dist_mat):
    """
    巡回セールスマン問題 (Travelling Salesman Problem, TSP)
    各2都市間の移動コストを記した隣接行列 dist_mat が与えられる。
    全ての都市をちょうど一度ずつ巡り出発地に戻る巡回路 (ハミルトン閉路) のうちで総移動コストが最小のものを求める

    愚直に全列挙すると頂点 0 をスタートとして (n-1)! 通り
    現在地 v とする。今、ある頂点集合 S (現在地 v 含む) を通って v にいるとき、過去にどう S を通ってきたかは今後の探索に影響を及ぼさない！
    （いずれも今後に訪れるべき頂点集合は {U \ S} であり探索経路は共通である）
    うまくこれをメモすれば計算量を削減可能。
    
    頂点集合を 0 ~ 2^n - 1 の bit により表現する。
    dp[S][v] = (ある頂点集合 S (現在地 v 含む) を通って v にいるときの最小コスト) とすると、
    dp[0][v] = inf if v != 0 else 0
    dp[S][v] = inf if v not in S else min(dp[{S\v}][u] + dist_mat[u][v] for u adjacent to v)

    Args:
        dist_mat (list):  (重みつき有向 / 無向グラフの隣接行列表現。自身との距離は 0, 非連結な頂点間距離は inf。2<=n<=15, 0<=w<=1000)
    Returns:
        min_cost (int)
        hamilton_path (list): 0 から始まり各頂点を一周して 0 に戻ってくる頂点の履歴
    """
    n = len(dist_mat)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    previous = [[None] * n for _ in range(1 << n)]
    dp[0][0] = 0
    for S in range(1, 1<<n):
        for v in range(n):
            if S & (1<<v):
                for u in range(n):
                    if dp[S][v] > dp[S - (1<<v)][u] + dist_mat[u][v]:
                        dp[S][v] = dp[S - (1<<v)][u] + dist_mat[u][v]
                        previous[S][v] = u
    # 経路の復元
    visited = (1 << n) - 1
    min_cost = dp[visited][0]
    hamilton_path = [0]
    current = 0
    while visited:
        prev_ind = previous[visited][current]
        hamilton_path.append(prev_ind)
        visited -= (1 << current)
        current = prev_ind
    hamilton_path.reverse()
    return min_cost, hamilton_path




if __name__ == "__main__":
    # https://www.slideshare.net/hcpc_hokudai/advanced-dp-2016 (p.6)
    I = float('inf')
    dist_mat = ((0, 3, I, 4, I),
                (I, 0, 5, I, I),
                (4, I, 0, 5, I),
                (I, I, I, 0, 3),
                (7, 6, I, I, 0))
    min_cost, hamilton_path = solve_TSP(dist_mat)
    assert(min_cost == 22)
    assert(hamilton_path == [0, 3, 4, 1, 2, 0])
    print(" * assertion test ok * ")
