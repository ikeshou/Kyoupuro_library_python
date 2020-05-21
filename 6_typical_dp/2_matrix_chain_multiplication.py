"""
連鎖行列積問題

n 個の行列の連鎖 A1A2A3A4...An が与えられた時、スカラー乗算の回数が最小となる最適な括弧付けを考え乗算回数を答える
    Ai = (pi-1 * pi 型行列) とする
    (a * b 行列) (b * c 行列) のスカラー乗算回数は a * b * c

愚直に異なる括弧付けの個数を列挙すると 
P(n) = 1 (n=1)
       Σ(k=1 to n-1) P(k)P(n-k) (n>=2)
であり、これは Ω(2^n) である。
部分構造最適性をうまく使うことにより二次元 DP によって O(n^3) で計算することができる。
"""


def matrix_chain_order(n, p):
    """
    n 個の行列の連鎖 <A1A2A3...An> が与えられた時、スカラー乗算の回数が最小となる最適な括弧付けを考え乗算回数を O(n^3) で答える
        - なお、Ai = (pi-1 * pi 型行列) とする
        - (a * b 行列) (b * c 行列) のスカラー乗算回数は a * b * c で計算できる
        - 定式化
        - dp[i][i] = 0
        - dp[i][j] = min(dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j] (i<=∀k<=j-1))
        - 連鎖長 l = j - i の各ケースを計算するには < l の全てのケースの計算が終わっている必要がある
    
    Args:
        n (int): 行列の個数
        p (list): 各行列の shape を記録したリスト
    Returns:
        dp (list): dp[i][j] = (Ai...Aj を最適な括弧付けで計算した時のスカラー乗算回数) (1 <= i <= j)
        reconstruct (list): reconstruct[i][j] = (Ai...Aj を (Ai...Ax)(Ax+1...Aj) と計算するのが最適な時の x) (1 <= i <= j + 1)
    """
    if n != len(p) - 1:
        raise ValueError(f"n should be eq to len(p) - 1. perherps failed in generating p list? got n:{n} p:{p}")
    
    dp = [[None] * (n + 1) for _ in range(n + 1)]
    reconstruct = [[None] * (n + 1) for _ in range(n + 1)]
    
    # (Ai) はすでに最適な括弧付けずみ。乗算回数 0
    for i in range(1, n + 1):
        dp[i][i] = 0
    
    # l は連鎖の長さ
    for l in range(2, n + 1):
        # (Ai...Aj) の最適な括弧付けで計算した時のスカラー乗算回数
        for i in range(1, n - l + 2):
            j = i + l - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                # (Ai...Ak)(Ak+1...Aj) と分割する場合
                cost = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    reconstruct[i][j] = k
    return dp, reconstruct
    

def print_optimal_parentheses(table, i, j, recursive=False):
    """
    reconstruct テーブルをもとに <Ai...Aj> の最適な括弧付けの方法を出力する
    """
    assert(1 <= i <= j)
    if i == j:
        print(f"A{i}", end='')
    else:
        print("(", end='')
        print_optimal_parentheses(table, i, table[i][j], recursive=True)
        print_optimal_parentheses(table, table[i][j] + 1, j, recursive=True)
        print(")", end='')
    if not recursive:
        print('')


if __name__ == "__main__":
    # A1=(30*35), A2=(35*15), A3=(15*5), A4=(5*10), A5=(10*20), A6=(20*25) とする
    p = [30, 35, 15, 5, 10, 20, 25]
    dp, reconstruct = matrix_chain_order(6, p)
    assert(dp[1][6] == 15125)
    
    
    import pprint
    pprint.pprint(dp)
    print('')
    """
    [[None, None, None, None, None, None, None],
    [None, 0, 15750, 7875, 9375, 11875, 15125],
    [None, None, 0, 2625, 4375, 7125, 10500],
    [None, None, None, 0, 750, 2500, 5375],
    [None, None, None, None, 0, 1000, 3500],
    [None, None, None, None, None, 0, 5000],
    [None, None, None, None, None, None, 0]]
    """
    print_optimal_parentheses(reconstruct, 1, 6)    # ((A1(A2A3))((A4A5)A6))