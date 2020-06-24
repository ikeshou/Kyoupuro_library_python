"""
行列累乗

いわゆる繰り返し二乗法の行列バージョン。 DP において多項式計算のみの漸化式が複数立つことがある。
それを行列式の形で表すことで、行列累乗の形で一般項を表せる。
(m, m) 行列同士の積 1 回あたりスカラー乗算は O(m^3) 行われるので、第 k 項の計算は O(m^3 * lgk) かかることになる
m <= 400 くらいまでは入る

(e.g.)
a_i+1 = 2 * a_i + b_i
b_i+1 = 2 * a_i + 2 * b_i + 2 * c_i
c_i+1 =           b_i     + 2 * c_i
などの漸化式は
[a_i+1,   [[2, 1, 0],   [a_i,
 b_i+1, =  [2, 2, 2], ○  b_i,
 c_i+1]    [0, 1, 2]]    c_i]
という形で表現可能。( ○ は行列積)
[a_n,   [[2, 1, 0], n   [a_0,
 b_n, =  [2, 2, 2],   ○  b_0,
 c_n]    [0, 1, 2]]      c_0]
これは上記のような行列累乗の形で一般項を表せる。
"""

def my_pow(a, k, mod):
    if k == 0:
        return 1
    if k % 2 == 0:
        return (my_pow(a, k // 2, mod) ** 2) % mod
    else:
        return (my_pow(a, k - 1, mod) * a) % mod
    


def mat_mul(A, B, mod):
    """
    mod を法として AB を計算する（行列積）。スカラー乗算の回数は a * b * c 回。

    Args:
        A (list): a * b 行列
        B (list): b * c 行列
        mod (int)
    Returns:
        result (list): a * c 行列
    """
    assert(len(A[0]) == len(B))
    a, b, c = len(A), len(A[0]), len(B[0])
    result = [[0] * c for _ in range(a)]
    for i in range(a):
        for j in range(c):
            for k in range(b):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result
    


def mat_pow(A, k, mod):
    """
    mod を法として A^k を計算する。行列累乗を用いるため計算量は O(m^3 * lgk)

    Args:
        A (list): m * m 行列
        k (int): k >= 1
        mod (int)
    Returns:
        result (list): m * m 行列
    """
    assert(len(A) == len(A[0]))
    m = len(A)
    if k == 0:
        return [[0 if j != i else 1 for j in range(m)] for i in range(m)]    # 単位行列
    if k % 2 == 0:
        tmp = mat_pow(A, k // 2, mod)
        return mat_mul(tmp, tmp, mod)
    else:
        return mat_mul(mat_pow(A, k - 1, mod), A, mod)


def mat_pow_fibonacci(n, mod):
    """
    第 n 番目の fibonacci 数 (mod) を O(lgn) で計算する
    F0 = 0
    F1 = 1
    Fn+2 = Fn+1 + Fn (n>=0)
    なる漸化式を行列積の形で表すと
    [Fn+2, = [[1, 1], [Fn+1,
     Fn+1]    [1, 0]]  Fn]
    累乗の形にすると (n>=1)
    [Fn,  = [[1, 1],n-1 [F1,
     Fn-1]   [1, 0]]     F0]
    
    Args:
        n (int): 0<=n<=10^16
        mod (int)
    Returns:
        int
    """
    if n == 0:
        return 0
    matrix = mat_pow([[1, 1], [1, 0]], n - 1, mod)
    result = mat_mul(matrix, [[1], [0]], mod)    # [[Fn], [Fn-1]]
    return result[0][0]


if __name__ == "__main__":
    import numpy as np
    import time
    mod = 10 ** 9 + 7
    assert(mat_mul([[0, 1],[2, 3]], [[0, 1, 2], [3, 4, 5]], mod) == [[3, 4, 5], [9, 14, 19]])
    assert(mat_pow([[1, 0], [0, 1]], 10**5, mod) == [[1, 0], [0, 1]])
    assert(mat_pow([[2, 0], [0, 3]], 10**5, mod) == [[pow(2, 10**5, mod), 0], [0, pow(3, 10**5, mod)]])
    assert(mat_pow([[1, 1], [1, 0]], 20, mod) == (np.matrix([[1, 1], [1, 0]]) ** 20 % mod).tolist())
    
    L = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for i in range(11):
        assert(mat_pow_fibonacci(i, mod) == L[i])
    assert(mat_pow_fibonacci(100, mod) == 687995182)
    
    print(" * assertion test ok * ")

