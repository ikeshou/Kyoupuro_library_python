"""
<Algorithm Introduction p.254-259>
Dijkstra 法 O((E+V)lgV) (頂点を回るときに最小のものを取り出していくのに VlgV, cost の更新で ElgV)
負辺を含まぬ重みつきグラフについて、ある頂点から他の頂点までの最短コストを貪欲に計算する
"""

from heapq import heappush, heappop
class PQueueMin:
    def __init__(self):
        self.pq = []    # 第一要素に cost、第二要素に ind が来る様にする
    
    def push(self, ind, cost):
        heappush(self.pq, [cost, ind])
    
    def pop(self):
        cost, ind = heappop(self.pq)
        return [ind, cost]

    def is_empty(self):
        return len(self.pq)==0



def dijkstra(adj_with_weight, start=0):
    V = len(adj_with_weight)
    cost = [float('inf')] * V
    cost[start] = 0
    fixed = [False] * V
    pq = PQueueMin()
    # 最初は始点が必ずコスト最小。pq に突っ込む
    pq.push(start, cost[start])
    while not pq.is_empty():
        # 現段階で最短のコストとなっている頂点を選択
        u, cost_of_u = pq.pop()
        fixed[u] = True
        for v, weight_of_uv in adj_with_weight[u]:
            if not fixed[v] and cost[v] > cost_of_u + weight_of_uv:
                cost[v] = cost_of_u + weight_of_uv
                pq.push(v, cost[v])
    return cost




if __name__ == "__main__":
    #                             to weight
    adjacent_list_with_weight = (((1, 5), (2, 6)),
                                 ((0, 5), (4, 2)),
                                 ((0, 6), (3, 2), (5, 4)),
                                 ((2, 2), (6, 1)),
                                 ((1, 2), (5, 3), (7, 7)),
                                 ((2, 4), (4, 3), (8, 1)),
                                 ((3, 1),),
                                 ((4, 7),),
                                 ((5, 1), (9, 1)),
                                 ((8, 1),))
    cost = dijkstra(adjacent_list_with_weight)
    print(cost)    # [0, 5, 6, 8, 7, 10, 9, 14, 11, 12]