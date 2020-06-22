"""
いもす法

<algorithm>
1 次元
ある一次元空間 (N) のある範囲全体に値の加減算を行うクエリを考える (Q)。最後に処理結果を出力することが求められる時、ナイーブに更新を行うと O(N*Q) + O(N) = O(N*Q) かかる。
入口と出口のみ記録することで O(Q) + O(N) = O(N+Q) に落とすことができる。
([l,r] に +a するなら [l] に +a, [r+1] に -a と記録しておく。最後の走査時に各要素にこのメモの累積和を足して行けば良い)

2 次元
ある二次元空間 (H*W) のある範囲全体に値の加減算を行うクエリを考える (Q)。最後に処理結果を出力することが求められる時、ナイーブに更新を行うと O(H*W*Q) + O(H*W) = O(H*W) かかる。
入口と出口のみ記録することで O(Q) + O(H*W) = O(H*W+Q) に落とすことができる。
([[l, u], [r, d]] に +a するなら [l, u] に +a, [r+1, u] に -a, [l, d+1] に -a, [r+1, d+1] に +a と記録しておく。最後の走査時に各要素にこのメモの累積和を足して行けば良い)
"""


from typing import List, Union

Num = Union[int, float]



class Imos1D:
    def __init__(self, size: int):
        self.size = size
        self.table = [0] * (size + 1)    # 区間の端の処理を省くための一マス
    
    def add(self, i: int, j: int, num: Num) -> None:
        """
        O(1) で [i, j] 区間に num の加算処理を行う
        """
        if i > j:
            raise ValueError(f"Imos1D.add(): [i, j] shold be i <= j. got i: {i}, j: {j}")
        if not (0 <= i < self.size and 0<= j < self.size):
            raise IndexError(f"Imos1D.add(): i, j should be 0 <= i, j < {self.size}. got i: {i}, j: {j}")
        self.table[i] += num
        self.table[j+1] -= num
    
    def total(self) -> List[Num]:
        """
        O(n) で累積和処理を行い、結果を保存したリストを返す
        """
        buf = self.table[:-1]    # 余分な最後の一マスを省く
        for i in range(1, self.size):
            buf[i] += buf[i-1]
        return buf



class Imos2D:
    def __init__(self, h: int, w: int):
        self.h = h
        self.w = w
        self.grid = [[0] * (w+1) for _ in range(h+1)]    # 区間の端の処理を省くための一マス
    
    def add(self, sx: int, tx: int, sy: int, ty: int, num: Num) -> None:
        """
        O(1) で {(x, y) | sx <= x <= tx, sy <= y <= ty} 領域に num の加算処理を行う
        """
        if sx > tx or sy > ty:
            raise ValueError(f"Imos2D.add(): [sx, tx], [sy, ty] shold be sx <= tx and sy <= ty. got sx: {sx}, sy: {sy}, tx: {tx}, ty: {ty}")
        if not (0 <= sx < self.h and 0 <= tx < self.h and 0 <= sy < self.w and 0 <= ty < self.w):
            raise IndexError(f"Imos2D.add(): sx, tx, sy, ty should be 0 <= sx, tx < {self.h} and 0 <= sy, ty <= {self.w}. got sx: {sx}, sy: {sy}, tx: {tx}, ty: {ty}")
        self.grid[sx][sy] += num
        self.grid[tx+1][sy] -= num
        self.grid[sx][ty+1] -= num
        self.grid[tx+1][ty+1] += num
    
    def total(self) -> List[List[Num]]:
        """
        O(h * w) で累積和処理を行い、結果を保存した 2 次元リストを返す
        """
        buf = [[self.grid[i][j] for j in range(self.w)] for i in range(self.h)]
        for i in range(1, self.h):
            for j in range(self.w):
                buf[i][j] += buf[i-1][j]
        for i in range(self.h):
            for j in range(1, self.w):
                buf[i][j] += buf[i][j-1]
        return buf




if __name__ == "__main__":
    N = 10
    # l, r, num -> [l, r) に +num する
    command = ((0, 4, 1),
               (4, 5, 2),
               (7, 9, 3),
               (6, 8, 4),
               (2, 6, 5))
    one_dim_imos = Imos1D(N)
    for l, r, num in command:
        one_dim_imos.add(l, r, num)
    assert(one_dim_imos.total() == [1, 1, 6, 6, 8, 7, 9, 7, 7, 3])


    
    H, W = 5, 5
    # (l, u), (r, d), num -> [(l, u), (r, d)) に +num する
    command = (((0, 0), (0, 0), 1),
               ((0, 3), (3, 4), 2),
               ((2, 3), (2, 4), 3),
               ((1, 1), (3, 3), 4),
               ((0, 0), (4, 0), 5))
    two_dim_imos = Imos2D(H, W)
    for p, q, num in command:
        l, u = p
        r, d = q
        two_dim_imos.add(l, r, u, d, num)
    assert(two_dim_imos.total() == [[6, 0, 0, 2, 2],
                                    [5, 4, 4, 6, 2],
                                    [5, 4, 4, 9, 5],
                                    [5, 4, 4, 6, 2],
                                    [5, 0, 0, 0, 0]])
    
    print(" * assertion test ok * ")
            
