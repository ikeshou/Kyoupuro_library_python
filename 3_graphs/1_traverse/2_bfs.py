"""
Breadth First Search
queue による実装
単純な全点探索と、経路内での重複を許さない全経路探索を行うコードを書いた。

0-1 BFS では deque の特性を活かして重みが 0 なら deque の先頭に突っ込もう
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


from collections import deque

visited = [False] * len(adjacent_list)

def bfs_queue_traverse(u):
    # 初期化
    for i in range(len(adjacent_list)):
        visited[i] = False
    queue = deque()
    queue.append(u)    # 距離も保存したかったら queue.append([u, 0]) という形で保存していく
    while queue:
        current = queue.popleft()
        if not visited[current]:
            visited[current] = True
            for v in adjacent_list[current]:
                if not visited[v]:
                    queue.append(v)


# もし高速に処理するなら path_set のような引数も用意して O(1) で含まれているかを判定できるようにする必要があるだろう。
def bfs_queue_path(start, goal, path=None):
    if path is None:
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
    bfs_queue_traverse(0)
    assert all(visited)

    bfs_queue_path(0, 6)
    assert all(visited)
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