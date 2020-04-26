"""
Ford-Fulkerson 法を用いた最大フローの算出

増加可能経路を発見し、フローを流し... を限界まで繰り返すのみ。
ポイントはフローを流した際 '逆向きにどのくらい流せるか (押し戻しが許されるか)' も更新するところ。
無向グラフについて。 capacity C で k だけ流したとして順流 / 逆流 = C/C -> C-k/C+k と更新される。
有向グラフについて。                                          C/0 -> C-k/k と更新される。
発見の戦略は色々あるがそれらをひっくるめて Ford-Fulkerson 「法」という。

発見が DFS によるものだと O(V+E) * O(|f*|) = O(E|f*|) (但し f* は最大フローの値)
      BFS              O(V+E) * O(VE) = O(VE^2) 
前者を Ford-Fulkerson algorithm, 後者を Edmonds-Karp algorithm という。
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


def ford_fulkerson(adj_list, start_ind, goal_ind):
    n = len(adj_list)
    adj = [[] for _ in range(n)]
    # 順辺、逆辺をはる
    for i, elm in enumerate(adj_list):
        for j, weight in elm:
            # どちらのエッジからも逆辺への参照を行えるようにしておく
            forward = Edge(i, j, weight, None)
            backward = Edge(j, i, 0, forward)
            forward.rev_edge = backward
            adj[i].append(forward)
            adj[j].append(backward)
    def dfs():
        path = [Edge(None, start_ind, None, None)]    # 擬似エッジ
        visited = [False] * n
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
            print(f"path: {[start_ind]+list(map(lambda x: x.to, p))}, current flow: {flow}")
    

def edmonds_karp(adj_list, start_ind, goal_ind):
    n = len(adj_list)
    adj = [[] for _ in range(n)]
    # 順辺、逆辺をはる
    for i, elm in enumerate(adj_list):
        for j, weight in elm:
            # どちらのエッジからも逆辺への参照を行えるようにしておく
            forward = Edge(i, j, weight, None)
            backward = Edge(j, i, 0, forward)
            forward.rev_edge = backward
            adj[i].append(forward)
            adj[j].append(backward)
    def bfs():
        path = [Edge(None, start_ind, None, None)]    # 擬似エッジ
        q = deque()
        q.append(path)
        visited = [False] * n
        visited[start_ind] = 0
        while q:
            edges = q.popleft()
            u = edges[-1].to
            visited[u] = True
            if u == goal_ind:
                return edges[1:]    # 最初の擬似エッジを取り除く
            for e in adj[u]:
                if not visited[e.to] and e.weight > 0:
                    tmp = edges[:]    # 要素の edge に関しては shallow copy されてほしい
                    tmp.append(e)
                    q.append(tmp)
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
        p = bfs()
        if not p:
            return flow
        else:
            flow += update_flow(p)
            print(f"path: {[start_ind]+list(map(lambda x: x.to, p))}, current flow: {flow}")    

    

if __name__ == "__main__":
    adj_with_weight = (((1, 50), (2, 20), (3, 30)),
                       ((2, 10), (4, 10)),
                       ((6, 40),),
                       ((2, 10), (7, 20)),
                       ((5, 10), (9, 20)),
                       ((1, 30), (2, 20), (6, 10), (9, 10)),
                       ((8, 50),),
                       ((6, 10),),
                       ((7, 20), (9, 50)),
                       (tuple()))
                       
    print("Ford-Fulkerson")
    maximum_flow = ford_fulkerson(adj_with_weight, 0, 8)
    print(maximum_flow)
    """
    path: [0, 1, 2, 6, 8], current flow: 10
    path: [0, 1, 4, 5, 2, 6, 8], current flow: 20
    path: [0, 2, 6, 8], current flow: 40
    path: [0, 3, 2, 5, 6, 8], current flow: 50
    50
    """
    print("\nEdmonds-Karp")
    maximum_flow_2 = edmonds_karp(adj_with_weight, 0, 8)
    print(maximum_flow_2)
    """
    path: [0, 2, 6, 8], current flow: 20
    path: [0, 1, 2, 6, 8], current flow: 30
    path: [0, 3, 2, 6, 8], current flow: 40
    path: [0, 3, 7, 6, 8], current flow: 50
    50
    """
    