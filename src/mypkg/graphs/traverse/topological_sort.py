"""
(参考) <Algorighm Introduction p.215-218, p.252-253>
BFS (DFS も可能) を用いて DAG をトポロジカルソートする (O(V+E))
(閉路のない有向グラフについての各有向辺が順方向になるようにソートを行う)
トポロジカルソートが行える (BFS のアルゴリズムについて、ソートずみグラフの頂点数がもとのグラフの頂点数と一致する) ⇄ DAGである ⇄ この有向グラフは閉路がない
(閉路検出だけなら 3 の一部分のようにして DFS で order をふって後退辺検出でもいいけれど)

また、DAG の単一始点最短経路問題 (負辺 OK) を求める問題も、
トポロジカルソート -> その順にコストを緩和 により O(V+E) で計算することが可能！ cf. Bellman-Ford


<algorithm>

BFS
入次数が 0 の頂点があればその頂点をソート後の結果に追加。その頂点と隣接した頂点の入次数を -- するのを繰り返す。
(「トポロジカルソート後の順で、そのノードより前のノードが存在しなかったら、そのノード数の入次数は 0 である」という性質を利用)

DFS
未探索の頂点を選びそこから未訪問の頂点に対し巡回を行い、帰りがけの順で buffer 末尾に追加することを繰り返す。
buffer を反転させる。
(木について preorder 巡回を行った結果がトポロジカルソートずみは真だが、DAG の preorder 巡回の結果が常にそうなるわけではない。
  0
1   2
  3
のようなケースにおいて帰りがけの順 (その頂点の処理が終わった段階で出力する) だと 3 1 2 0 となってくれる。反転して 0 2 1 3
一方 pre order 0 1 3 2 となりダイヤモンド型のグラフにおいて正しく順序が出力されていない。
なお、ここで登場した頂点へと接続する頂点については buffer の末尾にどんどん追加されていくので反転後はしっかり前に位置してくれる。
多分こちら側で DAG の判定は無理な気がする。
DAG -> 正しく DFS でトポロジカルソート可能
だが、
DAG ではないときもぶっ壊れたソート結果を返すので
例えば、
  5  4
0      3  
  1  2
のような閉路のある有向グラフについて DFS すると 5 4 3 2 1 0 -> 反転して 0 1 2 3 4 5 という結果になる。
"""


# verified @ABC139E
from collections import deque
from typing import Sequence, List


def topological_bfs(adj: Sequence[Sequence[int]]) -> List[int]:
    """
    グラフをトポロジカルソートしたときの頂点の並び順を表すリストを返す。この長さが頂点数に一致しない場合は閉路あり。

    Args:
        adj (list): 隣接リスト
    Returns:
        sorted_vertice (list): 有向グラフをトポロジカルソートしたときの頂点の並び順を表すリスト
    """
    n = len(adj)
    dimensions = [0] * n    # 入次数
    for edge in adj:
        for v in edge:
            dimensions[v] += 1
    q = deque()
    for i, dim in enumerate(dimensions):
        if dim == 0:
            q.append(i)
    sorted_vertice = []
    # BFS
    while q:
        top = q.popleft()
        if dimensions[top] != 0:
            break
        sorted_vertice.append(top)
        for v in adj[top]:
            dimensions[v] -= 1
            if dimensions[v] == 0:
                q.append(v)
    return sorted_vertice
        
    

def topological_dfs(adj: Sequence[Sequence[int]]) -> List[int]:
    """
    グラフをトポロジカルソートしたときの index の並び順を表すリストを返す。グラフは DAG であることを仮定している。
    
    Args:
        adj (list): 隣接リスト
    Returns:
        sorted_vertice (list): 有向グラフをトポロジカルソートしたときの頂点の並び順を表すリスト    
    """
    n = len(adj)
    visited = [False] * n    # 複数回 DFS する。前回訪問ずみの頂点を判定し探索先から外す必要がある
    buf = []
    def dfs(current=0):
        visited[current] = True
        for v in adj[current]:
            if not visited[v]:
                dfs(v)
        buf.append(current)    # 帰りがけの順で後ろに追加
    for i in range(n):
        if not visited[i]:
            dfs(i)
    buf.reverse()
    return buf



if __name__ == "__main__":
    adjacent_list = ((1, 3),
                    (3,),
                    (3, 4),
                    tuple(),
                    (5,),
                    tuple())

    bfs_result = topological_bfs(adjacent_list)
    assert(bfs_result == [0, 2, 1, 4, 3, 5])
    assert(len(bfs_result)==len(adjacent_list))    # DAG である
    
    dfs_result = topological_dfs(adjacent_list)
    assert(dfs_result == [2, 4, 5, 0, 1, 3])
    print(" * assertion test ok * ")
    
    
    
