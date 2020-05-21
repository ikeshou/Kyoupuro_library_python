"""
<Algorithm Introduction p..218-221>
強連結成分分解 Strongly connected composition decomposision (O(N+M))

有向グラフ G=(V,E) の任意の頂点 u,v について u~>v, v~>u なるパスが存在するときそのグラフは強連結である。
そういった成分の極大を強連結成分という。
強連結成分分解の結果、もとの有向グラフは DAG になる。


algorithm
DFS(G) を行い、帰りがけの順の順序をメモ
その降順をもとに DFS(transpose(G)) を行う。各 DFS が停止するごとに強連結成分が生成される。生成される順は DAG のトポロジカル順となる。
"""


def scc(graph, rgraph):
    """
    graph, rgraph をもとに強連結成分ごとのグルーピングを行う。
    グループ番号は 0 から始まり、その順が強連結成分分解後の DAG におけるトポロジカル順序を表す。
    グループ数、グループ番号を各頂点に対し記したリストを返す。
    Args:
        graph (list): 隣接リスト
        rgraph (list): 有向辺を逆に繋いだグラフの隣接リスト
    Returns:
        group_numbers (int): トータルのグループ (強連結成分) 数
        vertex_to_group_num (list): vertex_to_group_num[i] には i がどのグループ番号で表されるグループに属するかが int で入っているリスト
    """
    n = len(graph)
    order = []
    visited = [False] * n
    def dfs(current=0):
        visited[current] = True
        for v in graph[current]:
            if not visited[v]:
                dfs(v)
        order.append(current)
    vertex_to_group_num = [0] * n
    def rdfs(u, group_num):
        visited[u] = True
        vertex_to_group_num[u] = group_num
        for v in rgraph[u]:
            if not visited[v]:
                rdfs(v, group_num)
    # DFS the graph and memorize the end time of visiting for each node
    for i in range(n):
        if not visited[i]:
            dfs(i)
    # DFS the transposed graph
    cnt = -1
    visited = [False] * n    # 再初期化
    order.reverse()    # 訪問終了時刻が遅いものから
    for j in order:
        if not visited[j]:
            cnt += 1
            rdfs(j, cnt)
    # 0 ... cnt までがグループ番号として使用されている。
    return cnt+1, vertex_to_group_num
            
    
def contract_from_group(graph, group_num, vertex_to_group_num):
    """
    Args:
        graph (list): 隣接リスト
        group_num (int): トータルのグループ (強連結成分) 数
        vertex_to_group_num (list): vertex_to_group_num[i] には i がどのグループ番号で表されるグループに属するかが int で入っているリスト
    Returns:
        DAG (list): DAG[k] にはグループ番号 k から辺が伸びているグループの番号の set が入っているリスト
        strongly_connected (list): strongly_connected[k] にはグループ番号 k の強連結成分内の頂点のリストが入っているリスト
    """
    n = len(graph)  
    DAG = [set() for _ in range(group_num)]
    strongly_connected = [[] for _ in range(group_num)]
    for u in range(n):
        for v in graph[u]:
            if vertex_to_group_num[u] != vertex_to_group_num[v]:
                DAG[vertex_to_group_num[u]].add(vertex_to_group_num[v])
            else:
                strongly_connected[vertex_to_group_num[u]].append(v)
    return DAG, strongly_connected



if __name__ == "__main__":
    adjacent_list = [[1,],
                     [2, 4, 5],
                     [3, 6],
                     [2, 7],
                     [0, 5],
                     [6,],
                     [5, 7],
                     [7,]]
    reverse_adj_list = [[] for _ in range(len(adjacent_list))]
    for i, elm in enumerate(adjacent_list):
        for j in elm:
            reverse_adj_list[j].append(i)
    
    # main program
    group_num, vertex_to_group_num = scc(adjacent_list, reverse_adj_list)
    assert(group_num == 4)
    assert(vertex_to_group_num == [0, 0, 1, 1, 0, 2, 2, 3])
    
    DAG, strongly_connected = contract_from_group(adjacent_list, group_num, vertex_to_group_num)
    assert(DAG == [{1, 2}, {2, 3}, {3}, set()])
    assert(strongly_connected == [[1, 4, 0], [3, 2], [6, 5], [7]])

    print(" * assertion test ok * ")

