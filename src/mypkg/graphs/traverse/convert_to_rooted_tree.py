"""
根付き木表現への変換
木の隣接リストを、辺を親 -> 子のエッジのみに限定した隣接リストへ変換する
BFS でも DFS でも OK
"""


from collections import deque
from typing import Sequence, List


def convert_to_rooted_tree(adj: Sequence[Sequence[int]], root: int) -> List[List[int]]:
    """
    O(V+E) で木の隣接リストを、辺を親 -> 子のエッジのみに限定した隣接リストへ変換する

    Args:
        adj (list): 木の隣接リスト
        root (int): 根のインデックス
    Returns:
        tree_adj (list): 根付き木の隣接リスト (親 -> 子のエッジのみ)
    """
    n = len(adj)
    tree_adj = [[] for _ in range(n)]
    visited = [False] * n
    q = deque()
    q.append(root)
    while q:
        u = q.popleft()
        if not visited[u]:
            visited[u] = True
            for v in adj[u]:
                if not visited[v]:
                    q.append(v)
                    tree_adj[u].append(v)
    return tree_adj



if __name__ == "__main__":
    adj_line = ((1,),
                (0, 2),
                (1, 3,),
                (2, 4,),
                (3,))
    assert(convert_to_rooted_tree(adj_line, 0) == [[1], [2], [3], [4], []])
    assert(convert_to_rooted_tree(adj_line, 1) == [[], [0, 2], [3], [4], []])

    adj_star = ((1, 2, 3, 4),
                (0,),
                (0,),
                (0,),
                (0,))
    assert(convert_to_rooted_tree(adj_star, 0) == [[1, 2, 3, 4], [], [], [], []])
    assert(convert_to_rooted_tree(adj_star, 3) == [[1, 2, 4], [], [], [0], []])

    adj_complete_binary = ((1, 2), 
                           (0, 3, 4),
                           (0, 5, 6),
                           (1,),
                           (1,),
                           (2,),
                           (2,))
    assert(convert_to_rooted_tree(adj_complete_binary, 0) == [[1, 2], [3, 4], [5, 6], [], [], [], []])
    assert(convert_to_rooted_tree(adj_complete_binary, 5) == [[1], [3, 4], [0, 6], [], [], [2], []])
    print(" * assertion test ok * ")