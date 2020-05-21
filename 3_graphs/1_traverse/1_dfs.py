"""
Depth First Search
再帰による実装と stack による実装
単純な全点探索と、経路内での重複を許さない全経路探索を行うコードを書いた。
"""

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
elapsed_time = 0
time_stamp = [[0, 0] for _ in range(len(adjacent_list))]    # [first_visited, finished_visiting]

def dfs_recursive_traverse(u, recursive=False):
    """ 
    再帰を用いた DFS で全頂点を訪問する。最初に訪れた時間と、その頂点からの隣接頂点を全てコンプリートした時間を記録する。
    隣接リストを用いた実装なので、初期化に O(v) + 辺の探索に O(E) で O(V+E)
    訪問が目的なので「過去一度でもその頂点を訪問したか」に注目する。
    第一引数 u が現在地を表し、関数呼び出しがその頂点へ進むことと対応する。
    """
    global elapsed_time
    # 初期化
    if not recursive:
        for i in range(len(adjacent_list)):
            elapsed_time = 0
            visited[i] = False
            time_stamp[i][0] = 0
    # 彩色をし、タイムスタンプを押す
    visited[u] = True
    elapsed_time += 1
    time_stamp[u][0] = elapsed_time
    print(f"({u}", end=" ")    # 訪れたときの出力
    for v in adjacent_list[u]:
        if not visited[v]:
            dfs_recursive_traverse(v, recursive=True)    # その頂点へ進む -> その頂点の隣接頂点が周り済みになると戻ってくる。  
    # タイムスタンプを押す
    elapsed_time += 1
    time_stamp[u][1] = elapsed_time
    print(f"{u})", end=" ")    # 訪れたときの出力
    


def dfs_stack_traverse(u):
    """ 
    stack を用いた DFS で全頂点を訪問する。最初に訪れた時間と、その頂点からの隣接頂点を全てコンプリートした時間を記録する。
    隣接リストを用いた実装なので、初期化に O(v) + 辺の探索に O(E) で O(V+E)
    訪問が目的なので「過去一度でもその頂点を訪問したか」に注目する。
    stack の top が現在地を表し、stack につむことがその頂点へ進むことと対応する。
    """
    global elapsed_time
    # 初期化
    for i in range(len(adjacent_list)):
        elapsed_time = 0
        visited[i] = False
        time_stamp[i][0] = 0
        time_stamp[i][1] = 0
    # 彩色をし、タイムスタンプを押す
    visited[u] = True
    elapsed_time += 1
    time_stamp[u][0] = elapsed_time
    print(f"({u}", end=" ")    # 訪れたときの出力
    stack = [u]
    while len(stack) != 0:
        current = stack[-1]
        for v in adjacent_list[current]:
            if not visited[v]:
                stack.append(v)    # その頂点へ進むために stack につむ
                # 彩色をし、タイムスタンプを押す
                visited[v] = True
                elapsed_time += 1
                time_stamp[v][0] = elapsed_time
                print(f"({v}", end=" ")    # 訪れたときの出力
                break
        else:
            stack.pop()    # その頂点は隣接頂点を周りずみ。一つ前へ戻る。
            elapsed_time += 1
            time_stamp[current][1] = elapsed_time
            print(f"{current})", end=" ")



def dfs_recursive_path(start, goal, path=None):
    """
    再帰を用いた DFS で start から goal までの (頂点の重複を許さない) 全経路を探索する。
    全経路を探索したいので「今の経路でその頂点を訪れているか」に注目する。
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


def dfs_stack_path(start, goal):
    """
    stack を用いた DFS で start から goal までの (頂点の重複を許さない) 全経路を探索する。
    全経路を探索したいので「今の経路でその頂点を訪れているか」に注目する。
    """
    stack = [[start]]
    while stack:
        current_path = stack.pop()
        u = current_path[-1]
        print(current_path)
        if u == goal:
            print(f"->found! {current_path}")
        else:
            for v in reversed(adjacent_list[u]):
                if v not in current_path:
                    tmp = current_path[:]
                    tmp.append(v)
                    stack.append(tmp)



if __name__ == "__main__":
    dfs_recursive_traverse(0)    # (0 (1 (2 (4 (3 (5 5) 3) (6 6) 4) 2) 1) 0) 
    print("")
    print(time_stamp)    # [[1, 14], [2, 13], [3, 12], [5, 8], [4, 11], [6, 7], [9, 10]]
    assert all(visited)
    print("")
    
    dfs_stack_traverse(0)    # (0 (1 (2 (4 (3 (5 5) 3) (6 6) 4) 2) 1) 0) 
    print("")
    print(time_stamp)    # [[1, 14], [2, 13], [3, 12], [5, 8], [4, 11], [6, 7], [9, 10]]
    assert all(visited)
    print("")

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
