"""
(参考) <Algorithm Introduction vol.2 p.296-315>
Ford-Fulkerson 法を用いた最大フローの算出

<algorithm>
増加可能経路を発見し、フローを流し... を限界まで繰り返すのみ。
ポイントはフローを流した際 '逆向きにどのくらい流せるか (押し戻しが許されるか)' も更新するところ。
無向グラフについて。 capacity C で k だけ流したとして順流 / 逆流 = C/C -> C-k/C+k と更新される。
有向グラフについて。                                           C/x -> C-k/x+k と更新される。(逆辺がない場合 x = 0)
発見の戦略は色々あるがそれらをひっくるめて Ford-Fulkerson 「法」という。

発見が DFS によるものだと O(V+E) * O(|f*|) = O(E|f*|) (但し f* は最大フローの値)
      BFS              O(V+E) * O(VE) = O(VE^2) 
前者を Ford-Fulkerson algorithm, 後者を Edmonds-Karp algorithm という。

verified @ABC010D
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
    
    # 逆平行有向グラフの作成
    FF = FordFulkerson(len(adj_with_weight))
    for i in range(len(adj_with_weight)):
        for j, cap in adj_with_weight[i]:
            FF.add_edge(i, j, cap)
    
    # print で capacity 0 の逆辺は表示されない
    print(FF)
    """
    |0->1(50)|, |0->2(20)|, |0->3(30)|, |1->2(10)|, |1->4(10)|, |2->6(40)|, |3->2(10)|, |3->7(20)|, 
    |4->5(10)|, |4->9(20)|, |5->1(30)|, |5->2(20)|, |5->6(10)|, |5->9(10)|, |6->8(50)|, |7->6(10)|, 
    |8->7(20)|, |8->9(50)|    
    """

    # 二回実験するのでグラフの初期状態を保存しておく
    g = FF.reserve_state()

    print("Ford-Fulkerson")
    maximum_flow = FF.ford_fulkerson(0, 8)
    print(maximum_flow)
    print('')
    """
    path: [0, 1, 2, 6, 8], current flow: 10
    path: [0, 1, 4, 5, 2, 6, 8], current flow: 20
    path: [0, 2, 6, 8], current flow: 40
    path: [0, 3, 2, 5, 6, 8], current flow: 50
    50
    """

    # 時を巻き戻す
    FF.restore_state(g)

    print("Edmonds-Karp")
    maximum_flow_2 = FF.edmonds_karp(0, 8)
    print(maximum_flow_2)
    """
    path: [0, 2, 6, 8], current flow: 20
    path: [0, 1, 2, 6, 8], current flow: 30
    path: [0, 3, 2, 6, 8], current flow: 40
    path: [0, 3, 7, 6, 8], current flow: 50
    50
    """
    