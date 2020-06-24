"""
座標圧縮
参考：https://www.slideshare.net/hcpc_hokudai/za-atsu20170328

注目したい物に対し与えられる座標の範囲が広い時、注目したい量が保存される範囲で座標の範囲を狭める変換を行う。(O(nlgn))

(e.g. 1D) 
- case 1. 長さ n (~10^5) の数列 {a_n} (~10^18) を「要素間の大小関係が保存される範囲で」非負整数へと変換する。
- case 2.  n (~10^5) 個 X の置かれている座標 (~10^18) が与えられる。「置かれていない連続領域の個数が保存される範囲で」それらの座標を非負整数へと変換する。 

(e.g. 2D)
- case 1. n (~10^5) 個の座標 (~10^18, ~10^18) を「点間の大小関係が保存される範囲で」非負整数へと変換する。
- case 2. h * w の領域 (~10^18, ~10^18) のうち、n (~10^5) 個 X の置かれている線分領域 (縦 or 横) が与えられる。「置かれていない連続領域の個数が保存される範囲で」それらの座標を非負整数へと変換する。


<algorithm>
case 1 
ある注目する基底で全入力に対してソートを行い、先頭から順序をふっていく。(一つ前と値が等しい場合は番号は増やさない)
これでもとの値 <-> 順序番号 の対応関係が明らかになった。辞書とかに対応関係を保存すれば OK


case 2
case 1 と同様に処理しようとすると「置かれていない連続領域の個数」が増えてしまったり減ってしまったりする
..X...X..
..XX..X..
..X...X..
.........
......X..
領域は 1 個だったのに
X.X
XXX
X.X
..X
明らかに正しく圧縮されていない

注目する基底で 
線分両端 + 線分両端に対しその右と下にスペーサー点を追加 (自身の線分とかぶるものに対してはスルー) + 左、上端点 
に対しソートを行い圧縮を行うと
.X..X.
.XX.X.
.X..X.
......
....X.
領域を分つために必要な . が潰されることなく、座標圧縮がなされる。


one_dim_zaatsu_order(seq):
    O(nlgn)
    大小関係のみを保持する形で座標圧縮する

one_dim_zaatsu_region(seq, left, right):
    O(nlgn)
    全体領域 [left, right] をもとに、seq の要素のない連続した空白領域の個数を保持する形で座標圧縮する

two_dim_zaatsu_order(seq):
    O(nlgn)
    大小関係の身を保持する形で座標圧縮する

two_dim_zaatsu_region(row, col, left, right, up, down)
    O(nlgn)
    全体領域 D = {(x, y) | left<=x<=right, down<=y<=up} をもとに、row, col で示される直線領域を除いた連続した空白領域の個数を保持する形で座標圧縮する
"""


from typing import Dict, List, Tuple



# verified @ABC036C
def one_dim_zaatsu_order(L: List[int]) -> Tuple[int, Dict[int, int], Dict[int, int]]:
    """
    大小関係のみを保持する形で座標圧縮する (O(nlgn))

    Args:
        L (list): 圧縮したい数列

    Returns:
        new_n (int): 圧縮後の長さ
        compress (dict): 数列の値 -> 圧縮後の番号の辞書
        decompress (dict): 圧縮後の番号 -> 数列の値の辞書
    
    Examples:
        >>> new_n, com, decom = one_dim_zaatsu_order([0, 1, 2, 10**3, 10**5, 4])
        >>> new_n
        6
        >>> com
        {0: 0, 1: 1, 2: 2, 4: 3, 1000: 4, 100000: 5}
        >>> decom
        {0: 0, 1: 1, 2: 2, 3: 4, 4: 1000, 5: 100000}

        XXX.X......X......X......
        が
        XXXXXX
        へと圧縮される
    """
    compress, decompress = dict(), dict()
    arranged = sorted(set(L))
    for i, elm in enumerate(arranged):
        compress[elm] = i
        decompress[i] = elm
    return len(arranged), compress, decompress


def one_dim_zaatsu_region(L: List[int], left: int, right: int) -> Tuple[int, Dict[int, int], Dict[int, int]]:
    """
    全体領域をもとに、L の要素のない連続した空白領域の個数を保持する形で座標圧縮する (O(nlgn))

    Args:
        L (list): 圧縮したい数列
        left (int): 全体の領域の始点
        right (int): 全体の領域の終点

    Returns:
        new_n (int): 圧縮後の長さ
        compress (dict): 数列の値 -> 圧縮後の番号の辞書
        decompress (dict): 圧縮後の番号 -> 数列の値の辞書
    
    Examples:
        >>> new_n, com, decom = one_dim_zaatsu_region([0, 1, 2, 10**3, 10**5, 4], left=0, right=10**6)
        >>> new_n
        10
        >>> com
        {0: 0, 1: 1, 2: 2, 4: 4, 1000: 6, 100000: 8}
        >>> decom
        {0: 0, 1: 1, 2: 2, 4: 4, 6: 1000, 8: 100000}
        
        XXX.X......X......X......
        が
        XXX.X.X.X.
        へと圧縮される
    """
    compress, decompress = dict(), dict()
    # 右側に spacer を追加しているので右端点は追加しなくて良い。左端点と各点の一つ右の点を追加する。なお、この spacer が範囲内かはチェック
    point_with_spacer = set([left]) | set(L) | set([elm + 1 for elm in L if elm + 1 <= right])
    point_set = set(L)
    for i, elm in enumerate(sorted(point_with_spacer)):
        if elm in point_set:
            compress[elm] = i
            decompress[i] = elm
    return len(point_with_spacer), compress, decompress



class TwoDimZaatsu:
    def __init__(self, compress_x, compress_y, decompress_x, decompress_y):
        self.compress_x = compress_x
        self.compress_y = compress_y
        self.decompress_x = decompress_x
        self.decompress_y = decompress_y
    def compress(self, i, j):
        return [self.compress_x[i], self.compress_y[j]]
    def decompress(self, i, j):
        return [self.decompress_x[i], self.decompress_y[j]]



def two_dim_zaatsu_order(L: List[int]) -> Tuple[int, int, TwoDimZaatsu]:
    """
    大小関係のみを保持する形で座標圧縮する (O(nlgn))

    Args:
        L (list): 圧縮したい二次元座標の数列

    Returns:
        new_x (int): 圧縮後の x 座標軸上の区間長
        new_y (int): 圧縮後の y 座標軸上の区間長
        TwoDimZaatsu: compress(i, j) により座標から圧縮後の番号のペアを、decompress(i, j) により圧縮後の番号のペアから座標を得ることができる
    
    Examples:
        >>> point_list = [(0,0), (10,20), (100,5), (1000,1000), (50,1000), (10**4,500), (10**5,10**5)]
        >>> new_x, new_y, zaatsu = two_dim_zaatsu_order(point_list)
        >>> new_x
        7
        >>> new_y
        6
        >>> zaatsu.compress_x
        {0: 0, 10: 1, 50: 2, 100: 3, 1000: 4, 10000: 5, 100000: 6}
        >>> zaatsu.compress_y
        {0: 0, 5: 1, 20: 2, 500: 3, 1000: 4, 100000: 5}
        >>> zaatsu.decompress_x
        {0: 0, 1: 10, 2: 50, 3: 100, 4: 1000, 5: 10000, 6: 100000}
        >>> zaatsu.decompress_y
        {0: 0, 1: 5, 2: 20, 3: 500, 4: 1000, 5: 100000}
        >>> zaatsu.compress(50, 1000)
        [2, 4]
        >>> tmp = [[True] * new_x for _ in range(new_y)]
        >>> for x, y in point_list: tmp[zaatsu.compress(x, y)[1]][zaatsu.compress(x, y)[0]] = False
        >>> for line in tmp: print(*list(map(lambda cell: '.' if cell else 'X', line)))
        X . . . . . .
        . . . X . . .
        . X . . . . .
        . . . . . X .
        . . X . X . .
        . . . . . . X

        のように圧縮される。元は以下。
        X . . . . . . . . . . . . . . .
        . . . . . . . X . . . . . . . .
        . . X . . . . . . . . . . . . .
        . . . . . . . . . . . . X . . .
        . . . . X . . . . X . . . . . .
        . . . . . . . . . . . . . . . X

        完全に各行各列に X が存在するようになっていることからも (大小関係を保つ範囲で) 限界まで圧縮がなされていることがわかる。    
    """
    compress_x, compress_y, decompress_x, decompress_y = dict(), dict(), dict(), dict()
    L_x = sorted(set([elm[0] for elm in L]))
    L_y = sorted(set([elm[1] for elm in L]))
    for i, elm in enumerate(L_x):
        compress_x[elm] = i
        decompress_x[i] = elm
    for j, elm in enumerate(L_y):
        compress_y[elm] = j
        decompress_y[j] = elm
    return len(L_x), len(L_y), TwoDimZaatsu(compress_x, compress_y, decompress_x, decompress_y)



from itertools import chain
def two_dim_zaatsu_region(row: List[List[int]], col: List[List[int]], sx: int, tx: int, sy: int, ty: int) -> Tuple[int, int, TwoDimZaatsu]:
    """
    全体領域 (D:{(x,y)|sx<=x<=tx, sy<=y<=ty}) をもとに、L の要素の存在しない連続した空白領域の個数を保持する形で座標圧縮する (O(nlgn))

    Args:
        row (list): 領域を x 軸方向に塗りつぶす線分の (始点, 終点) を記録したリスト
        col (list): 領域を y 軸方向に塗りつぶす線分の (始点, 終点) を記録したリスト
        left, right, up, down (int): 領域の端の点

    Returns:
        new_x (int): 圧縮後の x 座標軸上の区間長
        new_y (int): 圧縮後の y 座標軸上の区間長
        TwoDimZaatsu: compress(i, j) により座標から圧縮後の番号のペアを、decompress(i, j) により圧縮後の番号のペアから座標を得ることができる
    
    Examples:
        >>> row = [[[0,3], [5,3]], [[0,7], [9,7]], [[5,9], [5,9]]]
        >>> col = [[[3,0], [3,9]], [[8,0], [8,4]], [[9,5], [9,9]]]
        >>> new_x, new_y, zaatsu = two_dim_zaatsu_region(row, col, 0, 9, 0, 9)
        >>> zaatsu.compress(8,4)
        [5, 2]
        >>> zaatsu.compress(5, 9)
        [3, 6]
        >>> tmp = [[True] * new_x for _ in range(new_y)]
        >>> _fill_compressed_grid_for_doctest(row, col, zaatsu, tmp)
        >>> for line in tmp: print(*list(map(lambda cell: '.' if cell else 'X', line)))
        . X . . . X .
        X X X X . X .
        . X . . . X .
        . X . . . . X
        X X X X X X X
        . X . . . . X
        . X . X . . X

        のように圧縮される。元は以下。
        . . . X . . . . X .
        . . . X . . . . X .
        . . . X . . . . X .
        X X X X X X . . X .
        . . . X . . . . X .
        . . . X . . . . . X
        . . . X . . . . . X
        X X X X X X X X X X 
        . . . X . . . . . X
        . . . X . X . . . X
        空白領域を犠牲にしない範囲で最大限圧縮がなされている。    
    """
    compress_x, compress_y, decompress_x, decompress_y = dict(), dict(), dict(), dict()
    # 点の羅列の形に flatten し、point_set を生成
    point_set = set(map(tuple, sum(row, []) + sum(col, [])))
    # x_point_with_spacer について。row については start[0], end[0], end[0] + 1 (範囲内なら), col については (start[0]=)end[0], end[0] + 1 (範囲内なら) を追加したい。
    # col の start[0], end[0] などは同じ値が重複してメモられた上で set となる過程で潰されるが、すっきりするのでまとめて書いてしまっている
    x_point_with_spacer = set([sx]) | set(sum([[start[0], end[0], end[0] + 1] if end[0] + 1 <= tx else [start[0], end[0]] for start, end in chain(row, col)], []))
    y_point_with_spacer = set([sy]) | set(sum([[start[1], end[1], end[1] + 1] if end[1] + 1 <= ty else [start[1], end[1]] for start, end in chain(row, col)], []))
    L_x = sorted(x_point_with_spacer)
    L_y = sorted(y_point_with_spacer)
    for i, x in enumerate(L_x):
        for j, y in enumerate(L_y):
            if (x, y) in point_set:
                compress_x[x] = i
                decompress_x[i] = x
                compress_y[y] = j
                decompress_y[j] = y
    return len(L_x), len(L_y), TwoDimZaatsu(compress_x, compress_y, decompress_x, decompress_y)
    


def _fill_compressed_grid_for_doctest(row: List[List[int]], col: List[List[int]], zaatsu: TwoDimZaatsu, grid: List[List[bool]]) -> None:
    """
    doctest 用の関数
    grid は座標圧縮後の架空の座標である (True で初期化されている)
    もとの塗り潰しコマンド row, col および座標圧縮オブジェクト zaatsu をもとに grid の塗り潰される領域を False で上書きする
    """
    for start, end in row:
        assert(start[1] == end[1])
        changed_start_x, changed_start_y = zaatsu.compress(start[0], start[1])
        changed_end_x, changed_end_y = zaatsu.compress(end[0], end[1])
        assert(changed_start_y == changed_end_y)
        for j in range(changed_start_x, changed_end_x + 1):
            grid[changed_start_y][j] = False
    for start, end in col:
        assert(start[0] == end[0])
        changed_start_x, changed_start_y = zaatsu.compress(start[0], start[1])
        changed_end_x, changed_end_y = zaatsu.compress(end[0], end[1])
        assert(changed_start_x == changed_end_x)
        for i in range(changed_start_y, changed_end_y + 1):
            grid[i][changed_start_x] = False
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()