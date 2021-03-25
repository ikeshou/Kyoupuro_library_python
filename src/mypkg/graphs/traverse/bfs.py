"""
(参考) <Algorithm Introduction vol.2 p.200-p.207>
Breadth First Search
- queue による実装
- 単純な全点探索と、(経路内での重複を許さない) 全経路探索

0-1 BFS では deque の特性を活かして重みが 0 なら deque の先頭に突っ込もう
"""

from typing import List
from collections import deque


def bfs_queue_traverse(start: int, adj: List[List[int]], visited: List[bool]) -> None:
    """
    queue を用いた BFS で全頂点を訪問する。初期化に O(V) + 辺の探索に O(E) で O(V+E)
    訪問が目的なので「過去一度でもその頂点を訪問したか」を visited リストを用いて管理する。
    """
    q = deque()
    q.append(start)    # 距離も保存したかったら q.append([start, 0]) という形で保存していく
    while q:
        u = q.popleft()
        if not visited[u]:    # start ~ u において最短パスが複数ある場合 q に u が複数回つまれうる。効率化のために visited チェックが必要。
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    q.append(v)



def bfs_queue_path(start: int, goal: int) -> None:
    """
    queue を用いた BFS で start から goal までの (頂点の重複を許さない) 全経路を探索する。
    全経路を探索したいので「今の経路でその頂点を訪れているか」に注目する。

    Note:
        current_path に含まれるかの判定および current_path のコピーの構築に O(n) かかるため、頂点数の多いグラフに対し適用不可 
        path は最悪全経路分のメモリを使用する
    """
    path = deque([[start]])
    while path:
        current_path = path.popleft()
        current = current_path[-1]
        print(current_path)
        if current == goal:
            print(f"->found! {current_path}")
        else:
            for v in adjacent_list[current]:
                if not v in current_path:
                    tmp = current_path[:]
                    tmp.append(v)
                    path.append(tmp)



if __name__ == "__main__":
    """
    0--2--4--6
    |  |  |
    `--1--3--5
    """
    adjacent_matrix = ((0, 1, 1, 0, 0, 0, 0),
                       (1, 0, 1, 1, 0, 0, 0),
                       (1, 1, 0, 0, 1, 0, 0),
                       (0, 1, 0, 0, 1, 1, 0),
                       (0, 0, 1, 1, 0, 0, 1),
                       (0, 0, 0, 1, 0, 0, 0),
                       (0, 0, 0, 0, 1, 0, 0))

    adjacent_list = ((1, 2),
                    (0, 2, 3),
                    (0, 1, 4),
                    (1, 4, 5),
                    (2, 3, 6),
                    (3,),
                    (4,))

    visited = [False] * len(adjacent_list)
    bfs_queue_traverse(0, adjacent_list, visited)
    assert all(visited)


    bfs_queue_path(0, 6)
    """
    [0]
    [0, 1]
    [0, 2]
    [0, 1, 2]
    [0, 1, 3]
    [0, 2, 1]
    [0, 2, 4]
    [0, 1, 2, 4]
    [0, 1, 3, 4]
    [0, 1, 3, 5]
    [0, 2, 1, 3]
    [0, 2, 4, 3]
    [0, 2, 4, 6]
    ->found! [0, 2, 4, 6]
    [0, 1, 2, 4, 3]
    [0, 1, 2, 4, 6]
    ->found! [0, 1, 2, 4, 6]
    [0, 1, 3, 4, 2]
    [0, 1, 3, 4, 6]
    ->found! [0, 1, 3, 4, 6]
    [0, 2, 1, 3, 4]
    [0, 2, 1, 3, 5]
    [0, 2, 4, 3, 1]
    [0, 2, 4, 3, 5]
    [0, 1, 2, 4, 3, 5]
    [0, 2, 1, 3, 4, 6]
    ->found! [0, 2, 1, 3, 4, 6]    
    """