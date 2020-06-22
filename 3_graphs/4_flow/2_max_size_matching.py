"""
(参考) <Algorithm Introduction vol.2 p.315-318>
二部グラフの最大マッチング問題

<algorithm>
超入口、超出口を用意して各辺を容量 1 と見なして最大フローを流すのみ

二部グラフの最大マッチングを求めるアルゴリズムを用いて
二部グラフの
最小辺被覆問題 (選んだ辺の両端の頂点を集めることができる。このとき、全ての頂点をカバーできるような最小の辺集合は何か？)
最小点被覆問題 (選んだ頂点から伸びる全ての辺を集めることができる。このとき、全ての辺をカバーできるような最小の頂点集合は何か？)
最大安定点問題 (その集合のどの 2 頂点も直接辺で結ばれていないような最大の頂点集合は何か？) <- 実は最小点被覆集合の補集合だけど
を解くことができる

verified @AtCoder ABC091_C
"""


from collections import deque
from copy import deepcopy
from typing import Sequence, List, Union, Any

Num = Union[int, float]


class Edge:
    def __init__(self, here: int, to: int, capacity: Num, is_rev: bool, rev_edge: Any):
        self.here = here
        self.to = to
        self.capacity = capacity
        self.is_rev = is_rev    # 最初に張られた時逆辺か否か, bool 型
        self.rev_edge = rev_edge    # 対応する逆辺への参照, Edge 型

    def __repr__(self) -> str:
        return f"|{self.here}->{self.to}({self.capacity})|"



class FordFulkerson:
    """
    逆平行辺を含まない有向グラフに対し、start_ind から goal_ind までに流せる最大流量を計算したい。
    <algorithm>
    増加可能経路を発見し、フローを流し... を限界まで繰り返す。
    ポイントはフローを流した際 '逆向きにどのくらい流せるか (押し戻しが許されるか)' も更新するところ。
    有向グラフについて。 capacity C で k だけ流したとして順流 / 逆流 = C/0 -> C-k/k と更新される。
    """
    def __init__(self, num_of_v: int):
        self.num_of_v = num_of_v    # 頂点数
        self.graph = [[] for _ in range(num_of_v)]   # 隣接する頂点のインデックスの代わりに Edge を収納した隣接リスト
    
    def __repr__(self) -> str:
        return ', '.join([str(e) for i in range(self.num_of_v) for e in self.graph[i] if not e.is_rev])
    
    def add_edge(self, here: int, to: int, capacity: Num) -> None:
        """
        here から to へ容量 capacity の有向辺をはる。
        その際、to から here への初期容量 0 の逆辺も同時にはる。
            - なお、逆平行辺を含まない有向グラフを仮定しているため to から here へ新たに有向辺がはられることは無いと仮定している。
              もし逆平行辺を含む場合は予めユーザーが here と to の間に新たに 2 つノードを設けるなどして、含まない等価なネットワークとなるよう工夫する必要がある。
                                        ↗︎ <s> ↘︎
                <u> <=> <v>    を    <u>       <v>  へ書き換える
                                        ↖︎ <t> ↙︎
            - 入口、出口のノードを複数にしたい場合は超入口、超出口なる架空のノードを用意して複数の入口、出口へ capacity が inf の辺をはる。

        Args:
            here (int)
            to (int)
            capacity (number)
        """
        forward = Edge(here, to, capacity, is_rev=False, rev_edge=None)
        backward = Edge(to, here, 0, is_rev=True, rev_edge=forward)
        forward.rev_edge = backward
        self.graph[here].append(forward)
        self.graph[to].append(backward)
    
    def reserve_state(self) -> None:
        """最大フローの計算では Edge の capacity は順次書き換えられる。後で初期状態に戻す必要がある場合は予め self.graph のディープコピーを取り出しておく。"""
        return deepcopy(self.graph)
    
    def restore_state(self, graph_state) -> None:
        """ reserve_state() により取り出した graph_state の状態へ、フローネットワークを restore する。"""
        self.graph = graph_state
    
    def ford_fulkerson(self, start_ind: int, goal_ind: int) -> Num:
        """
        増加可能経路を DFS により発見する。
        O(V+E) * O(|f*|) = O(E|f*|) (但し f* は最大フローの値) 
        """
        total_flow = 0
        while True:
            p = self._dfs(start_ind, goal_ind)
            if not p:
                return total_flow
            else:
                total_flow += self._update_flow(p)
                print(f"path: {[start_ind]+list(map(lambda x: x.to, p))}, current flow: {total_flow}")    # 提出時にはコメントアウトする
    
    def edmonds_karp(self, start_ind: int, goal_ind: int) -> Num:
        """
        増加可能経路を BFS により発見する。
        O(V+E) * O(VE) = O(VE^2) 
        """
        total_flow = 0
        while True:
            p = self._bfs(start_ind, goal_ind)
            if not p:
                return total_flow
            else:
                total_flow += self._update_flow(p)
                print(f"path: {[start_ind]+list(map(lambda x: x.to, p))}, current flow: {total_flow}")    # 提出時にはコメントアウトする
        
    def _dfs(self, start_ind: int, goal_ind: int) -> List[Edge]:
        """
        capacity > 0 の辺のみ連結していると見なした有向グラフについて、start_ind ~ goal_ind の経路を DFS で一つ発見して返す
        進むたびに頂点を stack に積む代わりに、Edge を stack に積んでいる。
        """
        path = [Edge(None, start_ind, None, is_rev=False, rev_edge=None)]    # 擬似エッジ
        visited = [False] * self.num_of_v
        visited[start_ind] = True
        while path:
            previous_e = path[-1]   # 最後に通った辺
            u = previous_e.to    # 現在地
            visited[u] = True
            if u == goal_ind:
                return path[1:]    # 最初の擬似エッジを取り除く
            for e in self.graph[u]:
                if not visited[e.to] and e.capacity > 0:
                    path.append(e)
                    break
            else:
                path.pop()    # 新たにいくところが無くなったら戻る
    
    def _bfs(self, start_ind: int, goal_ind: int) -> List[Edge]:
        """
        capacity > 0 の辺のみ連結していると見なした有向グラフについて、start_ind ~ goal_ind の経路を BFS で一つ発見して返す
        頂点を enqueue する代わりに、Edge を enqueue している。
        """
        path = [Edge(None, start_ind, None, is_rev=False, rev_edge=None)]    # 擬似エッジ
        q = deque()
        q.append(path)
        visited = [False] * self.num_of_v
        while q:
            edges = q.popleft()
            u = edges[-1].to
            visited[u] = True
            if u == goal_ind:
                return edges[1:]    # 最初の擬似エッジを取り除く
            for e in self.graph[u]:
                if not visited[e.to] and e.capacity > 0:
                    tmp = edges[:]    # 要素の edge に関しては shallow copy されてほしい
                    tmp.append(e)
                    q.append(tmp)
    
    def _update_flow(self, path: List[Edge]) -> Num:
        """ Edge のリストである path において、最大フローを流し capacity を更新する。流したフローを返す。 """
        maximum_flow = float('inf')
        for e in path:
            maximum_flow = min(maximum_flow, e.capacity)    # capacity のボトルネックを発見し更新する
        for e in path:
            e.capacity -= maximum_flow    # エッジクラスは参照で渡されているので adj にも変更が反映される
            e.rev_edge.capacity += maximum_flow    # どれくらい押し戻せるかが更新される
        return maximum_flow




def bipartite_max_matching(adj_list: Sequence[Sequence[int]], left_indices: Sequence[int], right_indices: Sequence[int], ford_fulkerson: bool=True) -> Num:
    """
    [left_indices] + [right_indices] なる頂点集合で (無向) 二部グラフが構成されているとする
    隣接リストが渡されるので、超入口と超出口を追加し、left から right へと有向辺 (capacity 1) を接続し、逆辺 (capacity 0) もはった有向グラフを構築する。
    Ford Fulkerson 法を用いて最大流を求めることで最大マッチングを計算できる。

    Args:
        adj_list (list): 隣接リスト
        left_indices (list): (無向) 二部グラフの片側の頂点集合 (0-index 表記)
        right_indices (list): (無向) 二部グラフのもう片側の頂点集合 (0-index 表記)
        ford_fulkerson (bool): True の時は最大フローを ford_fulkerson アルゴリズムで、False の時は edmonds_karp アルゴリズムで求める
    Returns:
        max_size_matching (int)
    """
    n, l, r = len(adj_list), len(left_indices), len(right_indices)
    if n != l + r:
        raise RuntimeError(f"bipartite_max_matching(): the number of vertice mismatched. num of vertice: {n}, left: {l}, right: {r}")
    ff = FordFulkerson(n + 2)    # 超入口と超出口分
    # 順辺、逆辺をはる
    for i in left_indices:
        for j in adj_list[i]:
            ff.add_edge(i+1, j+1, 1)    # 超入口分 1 だけ増やし 1-index 風になる
    # 超入口、出口を作成し capacity 1 で辺をはる
    super_entrance = 0
    for j in left_indices:
        ff.add_edge(super_entrance, j+1, 1)
    super_exit = n + 1
    for i in right_indices:
        ff.add_edge(i+1, super_exit, 1)
    # 最大流を求める
    return ff.ford_fulkerson(super_entrance, super_exit) if ford_fulkerson else  ff.edmonds_karp(super_entrance, super_exit)




if __name__ == "__main__":
    adjacent_list = ((1,),    # 0->
                     (0, 2, 4),
                     (1, 9),    # 2->
                     (4, ),
                     (1, 3, 5, 9),    # 4->
                     (4, 6),
                     (5, 7, 9),    # 6->
                     (6, ),
                     (9,),    # 8->
                     (2, 4, 6, 8))
    max_match = bipartite_max_matching(adjacent_list, left_indices=(0,2,4,6,8), right_indices=(1,3,5,7,9))
    print(max_match)
    """
    path: [0, 1], current flow: 1
    path: [2, 9], current flow: 2
    path: [4, 3], current flow: 3
    path: [6, 5], current flow: 4
    4
    """
