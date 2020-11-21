"""
(参考) <Algorithm Introduction vol.2 p.208-p.215>
Depth First Search

- 再帰による実装と stack による実装
- 単純な全点探索と、(経路内での重複を許さない) 全経路探索
"""

from typing import List, Union


def dfs_recursive_traverse(start: int, adj: List[List[int]], visited: List[bool]) -> None:
    """ 
    再帰を用いた DFS で全頂点を訪問する。初期化に O(V) + 辺の探索に O(E) で O(V+E)
    訪問が目的なので「過去一度でもその頂点を訪問したか」を visited リストを用いて管理する。
    _dfs の第一引数 u が現在地を表し、_dfs 関数呼び出しがその頂点へ進むことと対応する。
    
    Note:
        - 再帰によるスタックオーバフローが (手元の環境だと) 生じることに留意。
        - stack を用いた DFS の方が高速であることに留意。
        - for の _dfs のあとに u を出力すれば、その頂点を訪れる（戻る）たびに出力するようにできる。
    """
    def _dfs(u: int):
        visited[u] = True
        print(f"({u}", end=" ")    # 初めて訪れた時の出力
        for v in adj[u]:
            if not visited[v]:
                _dfs(v)    # その頂点へ進む -> その頂点の隣接頂点が周り済みになると戻ってくる。  
        print(f"{u})", end=" ")    # その頂点は隣接頂点を周りずみ
    _dfs(start)
    


def dfs_stack_traverse(start: int, adj: List[List[int]], visited: List[bool], state: List[int]) -> None:
    """ 
    stack を用いた DFS で全頂点を訪問する。初期化に O(V) + 辺の探索に O(E) で O(V+E)
    訪問が目的なので「過去一度でもその頂点を訪問したか」を visited リストを用いて管理する。
    stack の top が現在地を表し、stack につむことがその頂点へ進むことと対応する。
    
    state[i] は頂点 i を訪れた際 adj[i] のうち処理した頂点数を管理するために用いる。([0] * n で初期化)
    (state を用いずに inner while を for v in adj[u] で各頂点を見ると、訪問済みの頂点を何度も見るため O(V * E))
    (「戻ってきた時に」途中経過から隣接リストを走査したい)

    
    Note:
        - 訪問順が頂点の番号順でなくてよいなら、現在地 u を得る際 pop し inner while で break せず stack に積みきる。
        - while ループの冒頭で stack top を出力すると DFS traverse でその頂点を訪れる（戻る）たびに出力するようにできる。
          (A から B, C, D へ辺が伸びている場合、A -> B -> A -> C -> A -> D -> A という変遷を辿るため)
    """
    visited[start] = True
    print(f"({start}", end=" ")    # 初めて訪れたときの出力
    stack = [start]
    while stack:
        u = stack[-1]
        while state[u] < len(adj[u]):
            v = adj[u][state[u]]
            state[u] += 1
            if not visited[v]:
                stack.append(v)    # その頂点へ進むために stack につむ
                visited[v] = True
                print(f"({v}", end=" ")    # 初めて訪れたときの出力
                break
        else:
            stack.pop()    # その頂点は隣接頂点を周りずみ。一つ前へ戻る。
            print(f"{u})", end=" ")



def dfs_recursive_path(start:int, goal: int, path: Union[List, None]=None):
    """
    再帰を用いた DFS で start から goal までの (頂点の重複を許さない) 全経路を探索する。
    全経路を探索したいので「今の経路でその頂点を訪れているか」に注目する。

    Note:
        path に含まれるかの判定に O(n) かかるため、頂点数の多いグラフに対し適用不可
    """
    if path is None:
        path = [start]
    u = path[-1]
    print(path)
    if u == goal:
        print(f"->found! {path}")
    else:
        for v in adjacent_list[u]:
            if v not in path:
                path.append(v)
                dfs_recursive_path(start, goal, path)
                path.pop()


def dfs_stack_path(start: int, goal: int) -> None:
    """
    stack を用いた DFS で start から goal までの (頂点の重複を許さない) 全経路を探索する。
    全経路を探索したいので「今の経路でその頂点を訪れているか」に注目する。

    Note:
        path に含まれるかの判定および path のコピーの構築に O(n) かかるため、頂点数の多いグラフに対し適用不可
        stack は最悪全経路分のメモリを使用する
    """
    stack = [[start]]
    while stack:
        current_path = stack.pop()
        u = current_path[-1]
        print(current_path)
        if u == goal:
            print(f"->found! {current_path}")
        else:
            for v in reversed(adjacent_list[u]):    # 再帰 DFS なら最初に訪れる隣接頂点が最後にスタックに積まれるパスに含まれて欲しい
                if v not in current_path:
                    tmp = current_path[:]
                    tmp.append(v)
                    stack.append(tmp)



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
    dfs_recursive_traverse(0, adjacent_list, visited)    # (0 (1 (2 (4 (3 (5 5) 3) (6 6) 4) 2) 1) 0) 
    assert all(visited)
    print("")
    

    visited = [False] * len(adjacent_list)
    state = [0] * len(adjacent_list)
    dfs_stack_traverse(0, adjacent_list, visited, state)    # (0 (1 (2 (4 (3 (5 5) 3) (6 6) 4) 2) 1) 0) 
    assert all(visited)
    print("\n")
    

    dfs_recursive_path(0, 6)
    print("")
    dfs_stack_path(0, 6)
    print("")
    """
    [0]
    [0, 1]
    [0, 1, 2]
    [0, 1, 2, 4]
    [0, 1, 2, 4, 3]
    [0, 1, 2, 4, 3, 5]
    [0, 1, 2, 4, 6]
    ->found! [0, 1, 2, 4, 6]
    [0, 1, 3]
    [0, 1, 3, 4]
    [0, 1, 3, 4, 2]
    [0, 1, 3, 4, 6]
    ->found! [0, 1, 3, 4, 6]
    [0, 1, 3, 5]
    [0, 2]
    [0, 2, 1]
    [0, 2, 1, 3]
    [0, 2, 1, 3, 4]
    [0, 2, 1, 3, 4, 6]
    ->found! [0, 2, 1, 3, 4, 6]
    [0, 2, 1, 3, 5]
    [0, 2, 4]
    [0, 2, 4, 3]
    [0, 2, 4, 3, 1]
    [0, 2, 4, 3, 5]
    [0, 2, 4, 6]
    ->found! [0, 2, 4, 6]
    """
