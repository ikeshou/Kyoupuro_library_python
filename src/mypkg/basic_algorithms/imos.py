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
        """
        [0, size-1] 区間を作成する
        """
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
        >>> im = Imos1D(10)
        >>> im.add(2, 5, 1)
        >>> im.total()
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
        """
        buf = self.table[:-1]    # 余分な最後の一マスを省く
        for i in range(1, self.size):
            buf[i] += buf[i-1]
        return buf



class Imos2D:
    def __init__(self, h: int, w: int):
        """
        [0, h-1] * [0, w-1] グリッドを作成する
        """
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
        >>> im = Imos2D(3, 3)
        >>> im.add(1, 2, 1, 2, 5)
        >>> im.total()
        [[0, 0, 0], [0, 5, 5], [0, 5, 5]]
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
    import doctest
    doctest.testmod()