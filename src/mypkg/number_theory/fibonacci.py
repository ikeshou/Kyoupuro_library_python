"""
フィボナッチ数列


fibonacci(n):
    O(n)
    n 番目のフィボナッチ数を求める

fibonacci_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n 番目のフィボナッチ数を求める
"""


from typing import Generator


# ==== memorizing recursive function =====
def fibonacci(n: int, a: int=1, b: int=0) -> int:
    """
    O(n) で n (1 始まり) 番目のフィボナッチ数を求める

    Args:
        n (int)
        a (int)
        b (int)
        
    Returns:
        int: n 番目のフィボナッチ数

    Examples:
        >>> fibonacci(10)
        55

    Note:
        (0), 1, 1, 2, 3, 5, 8, 13, ...
        と考える。最初 a は 1 を b は 0 を指す。これが再帰の度に一つずつ進んでいく。
        第一引数 x は n - x 回再帰を回ったことを表し、第二引数 a は n - x + 1 番目の fibonacci のメモ、第三引数 b は n - x 番目の fibonacci のメモとなっている。
        x = 1 となった段階で a が n 番目の fibonacci 数を指していることになるのでこれを返せば良い。
    """
    if n == 1:
        return a
    return fibonacci(n - 1, a + b, a)



# ==== generator ====
def fibonacci_gen() -> Generator[int, int, None]:
    """
    >>> g = fibonacci_gen()
    >>> next(g)
    >>> g.send(1)
    1
    >>> g.send(10)
    55
    >>> g.send(9)    # just refer the table
    34
    """
    fibo_memo = [0, 1, 1]    # i 番目の fibonacci 数が fibo_memo[i] に入るようにする
    ind = yield
    while True:
        if len(fibo_memo)-1 < ind:
            for i in range(len(fibo_memo), ind+1):
                fibo_memo.append(fibo_memo[i-1]+fibo_memo[i-2])
        ind = yield fibo_memo[ind]    # send メソッドで generator に計算して欲しい値を送り込むことを想定



if __name__ == "__main__":
    import doctest
    doctest.testmod()