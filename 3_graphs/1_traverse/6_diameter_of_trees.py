"""
double sweep により O(V+E) で木の直径 (最大頂点間最短距離) を求める

algorithm
root から DFS を行い最遠点 u を求める
u から DFS を行い、最遠点 v を求める
diameter = dist(u, v)
"""

def diameter(adj, root):
    max_dist = 0
    most_remote_point = -1
    def dfs(u, previous=None, dist=0):
        nonlocal max_dist
        nonlocal most_remote_point
        if max_dist < dist:
            max_dist = dist
            most_remote_point = u
        for v in adj[u]:
            # 木の場合は visited 判定がいらない。自分自身を探索範囲から除けばそれらは全て未探索である。
            if v != previous:
                dfs(v, previous=u, dist=dist+1)
    dfs(root)
    max_dist = 0
    end_point_1 = most_remote_point
    dfs(most_remote_point)
    return (end_point_1, most_remote_point), max_dist



if __name__ == "__main__":
    """
                0
        1               2
    3               4   5   6
     7             8 9     10
      11          12  13
                        14
    という木を仮定する。
    0 の最遠点は 14
    14 の最遠点は 11
    dist(14, 11) = 5 + 4 = 9
    """
    adjacent_list = ((1, 2),
                     (0, 3),
                     (0, 4, 5, 6),
                     (1, 7),
                     (2, 8, 9),
                     (2,),
                     (2, 10),
                     (3, 11),
                     (4, 12),
                     (4, 13),
                     (6,),
                     (7,),
                     (8,),
                     (9, 14),
                     (13,))
    print(diameter(adj=adjacent_list, root=0))    # ((14, 11), 9)
