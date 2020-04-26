"""
Ford-Fulkerson method を用いて二部グラフの最大マッチングを求める
超入口、超出口を用意して各辺を容量 1 と見なして最大フローを流すのみ

二部グラフの最大マッチングを求めるアルゴリズムを用いて
二部グラフの
最小辺被覆問題 (選んだ辺の両端の頂点を集めることができる。このとき、全ての頂点をカバーできるような最小の辺集合は何か？)
最小点被覆問題 (選んだ頂点から伸びる全ての辺を集めることができる。このとき、全ての辺をカバーできるような最小の頂点集合は何か？)
最大安定点問題 (その集合のどの 2 頂点も直接辺で結ばれていないような最大の頂点集合は何か？) <- 実は最小点被覆集合の補集合だけど
を解くことができる
"""


from collections import deque

class Edge:
    def __init__(self, here, to, weight, rev_edge):
        self.here = here
        self.to = to
        self.weight = weight
        self.rev_edge = rev_edge    # 逆辺への参照

    def __repr__(self):
        return f"|{self.here}->{self.to}({self.weight})|"


def bipartite_max_matching(adj_list):
    """
    偶数ノードと奇数ノードで二部グラフが構成されているとする
    偶数ノードから奇数ノードへ向かう辺を集めた隣接リストが渡されるので、超入口と出口を追加し、辺を接続し、逆辺も Edge クラスで張った形の隣接リストを作成。
    最大流を求めて最大マッチングを計算する
    """
    n = len(adj_list)
    adj = [[] for _ in range(n+2)]
    # 順辺、逆辺をはる
    for i, elm in enumerate(adj_list):
        for j in elm:
            # 0-index のノードを 1-index 風に変更
            # どちらのエッジからも逆辺への参照を行えるようにしておく
            forward = Edge(i+1, j+1, 1, None)
            backward = Edge(j+1, i+1, 0, forward)
            forward.rev_edge = backward
            adj[i+1].append(forward)
            adj[j+1].append(backward)
    # 超入口、出口を作成し辺をはる
    start_ind = 0
    for i in range(0, n, 2):
        # 0-index のノードを 1-index 風に変更
        forward = Edge(start_ind, i+1, 1, None)
        backward = Edge(i, start_ind, 0, forward)
        forward.rev_edge = backward
        adj[start_ind].append(forward)
        adj[i+1].append(backward)
    goal_ind = n + 1
    for i in range(1, n, 2):
        # 0-index のノードを 1-index 風に変更
        forward = Edge(i+1, goal_ind, 1, None)
        backward = Edge(goal_ind, i+1, 0, forward)
        forward.rev_edge = backward
        adj[i+1].append(forward)
        adj[goal_ind].append(backward)
    print(adj) #kesu
    def dfs():
        path = [Edge(None, start_ind, None, None)]    # 擬似エッジ
        visited = [False] * (n+2)
        visited[start_ind] = 0
        while path:
            previous_e = path[-1]
            u = previous_e.to
            visited[u] = True
            if u == goal_ind:
                return path[1:]    # 最初の擬似エッジを取り除く
            for e in adj[u]:
                if not visited[e.to] and e.weight > 0:
                    path.append(e)
                    break
            else:
                path.pop()
    def update_flow(path):
        maximum_flow = float('inf')
        for e in path:
            maximum_flow = min(maximum_flow, e.weight)
        for e in path:
            e.weight -= maximum_flow    # エッジクラスは参照で渡されているので adj にも変更が反映される
            e.rev_edge.weight += maximum_flow    # どれくらい押し戻せるかが更新される
        return maximum_flow
    # main loop
    flow = 0
    while True:
        # for e in adj:
        #     print(e)
        p = dfs()
        if not p:
            return flow
        else:
            flow += update_flow(p)
            print(f"path: {list(map(lambda x: x.to - 1, p))[:-1]}, current flow: {flow}")


if __name__ == "__main__":
    adjacent_list = ((1,),    # 0->
                     tuple(),
                     (1, 9),    # 2->
                     tuple(),
                     (1, 3, 5, 9),    # 4->
                     tuple(),
                     (5, 7, 9),    # 6->
                     tuple(),
                     (9,),    # 8->
                     tuple())
    max_match = bipartite_max_matching(adjacent_list)
    print(max_match)
    """
    path: [0, 1], current flow: 1
    path: [2, 9], current flow: 2
    path: [4, 3], current flow: 3
    path: [6, 5], current flow: 4
    4
    """
