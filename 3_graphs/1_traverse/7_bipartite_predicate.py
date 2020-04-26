"""
DFS により二部グラフ判定を行う (O(V+E))

algorithm
二色 (B, R とする) を用意。ある頂点を B に彩色し、隣接頂点は異なる色で彩色していく。探索途中で色が矛盾する場合は二部グラフでないとわかる。
"""


def bipartite_predicate(adj):
    n = len(adj)
    start = 0
    color = [None] * n
    color[start] = True
    stack = [start]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if color[v] is None:
                color[v] = not color[u]
                stack.append(v)
            elif color[v] == color[u]:
                return False
    return True


if __name__ == "__main__":
    adj_1 = ((1, 3),
             (0, 2, 4),
             (1, 5),
             (0, 4),
             (1, 3, 5),
             (2, 4))
    """
    0--1--2
    |  |  |
    3--4--5
    二部グラフである
    """             
    assert(bipartite_predicate(adj_1) == True)

    adj_2 = ((1, 3),
             (0, 2, 4),
             (1, 4),
             (0, 4),
             (1, 3))
    """
    0--1--2
    |  | /
    3--4
    二部グラフではない
    """
    assert(bipartite_predicate(adj_2) == False)

    adj_3 = ((1, 2, 3),
             (0, 4),
             (0,),
             (0, 4),
             (1, 3))
    """
    0--1
    |＼  ＼
    2  3---4  
    二部グラフである
    """
    assert(bipartite_predicate(adj_3) == True)

    print(" * assertion test ok * ")


