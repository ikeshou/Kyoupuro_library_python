#!/usr/bin/env python3
"""
いもす法

1D imos
ある一次元空間 (N) のある範囲全体に値の加減算を行うクエリを考える (Q)。最後に処理結果を出力することが求められる時、ナイーブに更新を行うと O(N*Q) + O(N) = O(N*Q) かかる。
入口と出口のみ記録することで O(Q) + O(N) = O(N+Q) に落とすことができる。
([l,r] に +a するなら [l] に +a, [r+1] に -a と記録しておく。最後の走査時に各要素にこのメモの累積和を足して行けば良い)

2D imos
ある二次元空間 (H*W) のある範囲全体に値の加減算を行うクエリを考える (Q)。最後に処理結果を出力することが求められる時、ナイーブに更新を行うと O(H*W*Q) + O(H*W) = O(H*W) かかる。
入口と出口のみ記録することで O(Q) + O(H*W) = O(H*W+Q) に落とすことができる。
([[l, u], [r, d]] に +a するなら [l, u] に +a, [r+1, u] に -a, [l, d+1] に -a, [r+1, d+1] に +a と記録しておく。最後の走査時に各要素にこのメモの累積和を足して行けば良い)
"""


if __name__ == "__main__":
    N = 10
    L = [0] * (N + 1)
    # l, r, num -> [l, r) に +num する
    command = ((0, 5, 1),
               (4, 6, 2),
               (7, 10, 3),
               (6, 9, 4),
               (2, 7, 5))
    for l, r, num in command:
        L[l] += num
        L[r] -= num
    print('1D imos')
    accumulatation_sum = 0
    for i in range(N):
        accumulatation_sum += L[i]
        L[i] = accumulatation_sum
    print(*L)
    # 1 1 6 6 8 7 9 7 7 3 -3
    print('')
    
    H = 5
    W = 5
    L = [[0] * (W+1) for _ in range(H+1)]
    # (l, u), (r, d), num -> [(l, u), (r, d)) に +num する
    command = (((0, 0), (1, 1), 1),
               ((0, 3), (4, 5), 2),
               ((2, 3), (3, 5), 3),
               ((1, 1), (4, 4), 4),
               ((0, 0), (5, 1), 5))
    for p, q, num in command:
        l, u = p
        r, d = q
        L[l][u] += num
        L[r][u] -= num
        L[l][d] -= num
        L[r][d] += num
    for i in range(H):
        accumulatation_sum = 0
        for j in range(W):
            accumulatation_sum += L[i][j]
            L[i][j] = accumulatation_sum
    for j in range(W):
        accumulatation_sum = 0
        for i in range(H):
            accumulatation_sum += L[i][j]
            L[i][j] = accumulatation_sum

    print('2D imos')
    for i in range(H):
        print(*L[i][:-1])
    """
    6 0 0 2 2
    5 4 4 6 2
    5 4 4 9 5
    5 4 4 6 2
    5 0 0 0 0    
    """
            
