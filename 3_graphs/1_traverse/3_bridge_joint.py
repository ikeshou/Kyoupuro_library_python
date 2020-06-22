"""
(参考) <Algorithm Introduction p.222-223>
無向グラフについて DFS と lowlink を用いて橋と関節点を求める (O(V+E))

橋 (bridge): 取り除くと連結成分が増える辺
関節点 (articulation point): 取り除くと連結成分が増える頂点 (接続辺も取り除く)


<algorithm>
order[u] は頂点を訪れた順番
    DFS 木において根から葉の方向にかけて大きくなる
    必ず後退辺は order 大 -> order 小を結ぶ
lowlink[u] は u から 1. DFS 木の辺を根から葉へ 0 回以上進む 2. 後退辺を葉から根へ 0-1 回だけ進む によりたどり着ける頂点での order の最小値
    u を根とする DFS 部分木において、後退辺による接続を許した時たどりつける一番根に近い頂点の order を表している
    lowlink によりサイクル検出が可能となる

ある辺 uv が橋 <=> order(u) < lowlink(v)
    後退辺を無視した時 uv をカットすると v を根とする DFS 部分木 + 残りの DFS 部分木に分かれる
    v から u 側の DFS 部分木へ後退辺が伸びていれば uv は橋ではない
    lowlink(v) は v から後退辺による接続を許した時たどりつける一番根に近い頂点の order を表しているので、lowlink(v) <= order(u) なら後退辺接続されている
    故に order(u) < lowlink(v) で橋の判定が可能
ある点 u (根以外) が関節点 <=> for any v adjacent to u order(u) <= lowlink(v)
    根の場合子供が複数いたら関節点
    それ以外の頂点の場合、子供 v が後退辺により u の先祖と接続していたら u を削除しても到達可能である
    全ての子供についてこれが成立していれば関節点
    故に all v adjacent to u lowlink(v) < order(u)
    逆に any v adjacent to u order(u) <= lowlink(v) で関節点の判定が可能



二重連結成分分解 (bi-connected components decomposition)
橋以外のエッジでつながっている頂点グループをひとかたまりと見た縮約グラフを考える。
もとのグラフの橋のみが縮約グラフにおけるエッジとなる。
二重連結成分分解後は木構造となる。
"""

from typing import Sequence, Set, List, Tuple


def bridge_detect(adj: Sequence[Sequence[int]], start: int=0) -> Tuple[List[List[int]], List[Set[int]]]:
    """
    O(V+E) で橋を検出する

    Args:
        adj (list): 隣接リスト
        start (int): 開始頂点を示すインデックス

    Returns:
        bridge (list): 橋を示すリスト。edge(u, v) が橋である時 (u, v) がこのリストに追加される。u は DFS木において v の親に当たる。 (edge(v, u) は bridge に含まれない)
        cycle_graph (list): cycle_graph[i] には i と '直接つながる' 二重連結成分が set で入っているリスト
    """
    n = len(adj)
    order = [-1] * n
    lowlink = [-1] * n
    cnt = -1
    bridge = []
    cycle_graph = [set() for _ in range(n)]
    def dfs(u, parent=-1):
        nonlocal cnt    # order をふる用。再起呼び出しでのインクリメントが呼び出しもとでも反映されて欲しい
        cnt += 1
        order[u] = cnt
        lowlink[u] = cnt
        for v in adj[u]:
            # 親
            if v == parent:
                continue
            # 未訪問
            if order[v] == -1:
                dfs(v, parent=u)
                lowlink[u] = min(lowlink[u], lowlink[v])
            # v は訪問ずみだが、DFS 木の親でない。uv は後退辺
            else:
                lowlink[u] = min(lowlink[u], order[v])
            # bridge detection
            if order[u] < lowlink[v]:
                bridge.append((u, v))
            # for bi-connected components decomposition
            else:
                cycle_graph[u].add(v)
                cycle_graph[v].add(u)
    dfs(start)
    return bridge, cycle_graph
    

def articulation_detect(adj: Sequence[Sequence[int]], start: int=0) -> List[int]:
    """
    O(V+E) で関節点を検出する

    Args:
        adj (list): 隣接リスト
        start (int): 開始頂点を示すインデックス

    Returns:
        articulation (list): 関節点である頂点のリスト
    """
    n = len(adj)
    order = [-1] * n
    lowlink = [-1] * n
    cnt = -1
    articulation = []
    def dfs(u, parent=-1):
        nonlocal cnt    # order をふる用。再起呼び出しでのインクリメントが呼び出しもとでも反映されて欲しい
        cnt += 1
        order[u] = cnt
        lowlink[u] = cnt
        for v in adj[u]:
            # 親
            if v == parent:
                continue
            # 未訪問
            if order[v] == -1:
                dfs(v, parent=u)
                lowlink[u] = min(lowlink[u], lowlink[v])
            # v は訪問ずみだが、DFS 木の親でない。uv は後退辺
            else:
                lowlink[u] = min(lowlink[u], order[v])
        # articulation detection
        if u == start and len(adj[u]) > 1:
            articulation.append(u)
        elif any(map(lambda v: order[u] <= lowlink[v], filter(lambda x: x!=parent, adj[u]))):
            articulation.append(u)
    dfs(start)
    return articulation


def contract_from_cycle(bridge: List[List[int]], cycle_graph: List[Set[int]]) -> Tuple[List[int], List[List[int]]]:
    """
    O(V+E) で二重連結成分分解を行う

    Args:
        bridge (list): 橋を示すリスト。edge(u, v) が橋である時 (u, v) がこのリストに追加される
        cycle_graph (list): cycle_graph[i] には i と '直接つながる' 二重連結成分が set で入っているリスト
        
    Returns:
        vertex_to_group_num (list): vertex_to_group_num[i] には i がどのグループ番号で表されるグループに属するかが int で入っているリスト
        bi_connected (list): 二重連結成分ごとにグルーピングを行った時、そのグループ番号で表現された隣接リスト
    """
    n = len(cycle_graph)
    visited = [False] * n
    vertex_to_group_num = [-1] * n
    def dfs(u, group_num):
        ' u と同じ二重連結成分に属する頂点全てに num なるグルーピングを施す。'
        visited[u] = True
        vertex_to_group_num[u] = group_num
        for v in cycle_graph[u]:
            if not visited[v]:
                dfs(v, group_num)
    # 実際に二重連結成分単位でグルーピング
    cnt = -1
    for u in range(n):
        if not visited[u]:
            cnt += 1
            dfs(u, cnt)
    # そのグループ番号を新たなノードだとみなしたときの隣接リストを作る
    bi_connected = [[] for _ in range(cnt + 1)]
    for u, v in bridge:
        bi_connected[vertex_to_group_num[u]].append(vertex_to_group_num[v])
        bi_connected[vertex_to_group_num[v]].append(vertex_to_group_num[u])
    return vertex_to_group_num, bi_connected
    


if __name__ == "__main__":
    adjacent_list = ((1, 5),
                    (0, 2, 3, 4),
                    (1,),
                    (1, 4),
                    (3, 1),
                    (0, 6, 9),
                    (5, 7, 8),
                    (6,),
                    (6, 9),
                    (5, 8))

    bridge, cycle_graph = bridge_detect(adjacent_list, start=0)
    assert(bridge == [(1, 2), (0, 1), (6, 7), (0, 5)])
    assert(cycle_graph == [set(), {3, 4}, set(), {1, 4}, {1, 3}, {9, 6}, {8, 5}, set(), {9, 6}, {8, 5}])
    vertex_to_group_num, bi_connected = contract_from_cycle(bridge, cycle_graph)
    assert(vertex_to_group_num == [0, 1, 2, 1, 1, 3, 3, 4, 3, 3])
    assert(bi_connected == [[1, 3], [2, 0], [1], [4, 0], [3]])
    articulation = articulation_detect(adjacent_list, start=0)
    assert(articulation == [1, 6, 5, 0])
    print(" * assertion test ok * ")