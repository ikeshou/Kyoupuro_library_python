#!/usr/bin/env python3
"""
number theory algorithms implemented in Python3 for programming competition

is_prime(n):
    O(√n)
    num が素数かどうか判定する

Eratos:
    init(n):
        O(nlglgn) で初期化、num までの素数判定テーブルを作る
    is_prime(n):
        O(1) で素数かどうか判定する
    prime_factorize(n):
        O(√n) (候補の素数を列挙するところが律速) で素因数分解を行う

euclid_gcd(a, b):
    O(lgn)
    a, b の gcd を求める

fibonacci(n):
    O(n)
    n 番目のフィボナッチ数を求める

fibonacci_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n 番目のフィボナッチ数を求める

factorial_gen(n):
    O(n) (すでに計算済みのものは O(1))
    n! を求める

combination(n, r, m):
    O(nlgm) (階乗がすでに計算済みの場合 O(lgm)) (mod の階乗が繰返し二乗法分 O(lgm) かかる)
    nCr (mod m) を求める
"""

# ====prime numbers =====
import math
def is_prime(num):
    """
    >>> is_prime(1000000007)
    True
    """
    assert(num >= 1)
    if num == 2:
        return True
    if num == 1 or num % 2 == 0:    # 下で定数倍高速化できる
        return False
    i = 3
    while i <= int(math.sqrt(num)):
        if i % num == 0:
            return False
        i += 2
    return True    


class Eratos:
    def __init__(self, num):
        assert(num >= 1)
        self.table_max = num
        # self.table[i] は i が素数かどうかを示す (bool)
        self.table = [False if i == 0 or i == 1 else True for i in range(num+1)]
        for i in range(2, int(math.sqrt(num)) + 1):
            if self.table[i]:
                for j in range(i ** 2, num + 1, i):    # i**2 からスタートすることで定数倍高速化できる
                    self.table[j] = False
        # self.table_max 以下の素数を列挙したリスト
        self.prime_numbers = [2] if self.table_max >= 2 else []
        for i in range(3, self.table_max + 1, 2):
            if self.table[i]:
                self.prime_numbers.append(i)
    
    def is_prime(self, num):
        """
        >>> e = Eratos(100)
        >>> [i for i in range(1, 101) if e.is_prime(i)]
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        """
        assert(num >= 1)
        if num > self.table_max:
            raise ValueError('Eratos.is_prime(): exceed table_max({}). got {}'.format(self.table_max, num))
        return self.table[num]
    
    def prime_factorize(self, num):
        """
        >>> e = Eratos(10000)
        >>> e.prime_factorize(6552)
        {2: 3, 3: 2, 7: 1, 13: 1}
        """
        assert(num >= 1)
        if num > self.table_max:
            raise ValueError('Eratos.prime_factorize(): exceed table_max({}). got {}'.format(self.table_max, num))
        factorized_dict = dict()    # 素因数分解の結果を記録する辞書
        candidate_prime_numbers = [i for i in range(2, int(math.sqrt(num)) + 1) if self.is_prime(i)]
        # n について、√n 以下の素数で割り続けると最後には 1 or 素数となる
        # 背理法を考えれば自明 (残された数が √n より上の素数の積であると仮定。これは自明に n を超えるため矛盾)
        for p in candidate_prime_numbers:
            # これ以上調査は無意味
            if num == 1:
                break
            while num % p == 0:
                num //= p
                try:
                    factorized_dict[p]
                except KeyError:
                    factorized_dict[p] = 0
                finally:
                    factorized_dict[p] += 1
        if num != 1:
            factorized_dict[num] = 1
        return factorized_dict
# =======================



# ==== memorizing recursive function =====
def euclid_gcd(a, b):
    """
    ユークリッドの互除法 gcd(a, b) = gcd(b, r) (但し r = a % b)
    >>> euclid_gcd(74, 54)
    2
    """
    a, b = max(a, b), min(a, b)
    if b == 0:
        return a
    return euclid_gcd(b, a%b)


def fibonacci(n, a=1, b=0):
    """
    (0), 1, 1, 2, 3, 5, 8, 13, ...
    と考える。最初 a は 1 を b は 0 を指す。これが再帰の度に一つずつ進んでいく。
    第一引数 x は n - x 回再帰を回ったことを表し、第二引数 a は n - x + 1 番目の fibonacci のメモ、第三引数 b は n - x 番目の fibonacci のメモとなっている。
    x = 1 となった段階で a が n 番目の fibonacci 数を指していることになるのでこれを返せば良い。
    >>> fibonacci(10)
    55
    """
    if n == 1:
        return a
    return fibonacci(n-1, a+b, a)
# ========================================


# ==== generator ====
def fibonacci_gen():
    """
    >>> g = fibonacci_gen()
    >>> next(g)
    >>> g.send(1)
    1
    >>> g.send(2)
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


def factorial_gen():
    """
    >>> g = factorial_gen()
    >>> next(g)
    >>> g.send(5)
    120
    >>> g.send(10)
    3628800
    >>> g.send(9)    # just refer the table
    362880
    """
    fact_memo = [1]    # i! が fact_memo[i] に入るようにする
    ind = yield
    while True:
        if len(fact_memo)-1 < ind:
            for i in range(len(fact_memo), ind+1):
                fact_memo.append(i * fact_memo[i-1])
        ind = yield fact_memo[ind]    # # send メソッドで generator に計算して欲しい値を送り込むことを想定
# ===================


# ===== combination with mod =======
FACT_MOD = [1, 1]    # i! % mod が FACT_MOD(i) に登録される
def combination(n, r, mod):
    """
    フェルマーの小定理 
    a ^ p-1 ≡ 1 (mod p)
    a ^ p-2 ≡ 1/a (mod p) (逆元)
    nCr = (n!) / ((n-r)! * r!) だが、mod p の世界ではこの分母を逆元を用いて計算しておくことが可能
    
    >>> m = 1000000007
    >>> combination(10, 5, m)
    252
    >>> combination(100, 50, m)
    538992043
    """
    needed_slots = n - (len(FACT_MOD) - 1)
    if needed_slots > 0:
        for _ in range(needed_slots):
            FACT_MOD.append((len(FACT_MOD) * FACT_MOD[-1]) % mod)
    numerator = FACT_MOD[n]
    denominator = (FACT_MOD[n-r] * FACT_MOD[r]) % mod
    # pow はすでに繰り返し二乗法で効率的に実装されている
    return (numerator * pow(denominator, mod-2, mod)) % mod
# ==================================    



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # check the corner cases!
    assert(is_prime(1) == False)
    assert(is_prime(2) == True)
    assert(is_prime(3) == True)

    e_1 = Eratos(1)
    assert(e_1.is_prime(1) == False)
    assert(e_1.prime_numbers == [])
    assert(e_1.prime_factorize(1) == {})
    e_2 = Eratos(2)
    assert(e_2.is_prime(1) == False)
    assert(e_2.is_prime(2) == True)
    assert(e_2.prime_numbers == [2])
    assert(e_2.prime_factorize(1) == {})
    assert(e_2.prime_factorize(2) == {2: 1})
    e_3 = Eratos(3)
    assert(e_3.is_prime(1) == False)
    assert(e_3.is_prime(2) == True)
    assert(e_3.is_prime(3) == True)
    assert(e_3.prime_numbers == [2, 3])
    assert(e_3.prime_factorize(1) == {})
    assert(e_3.prime_factorize(2) == {2: 1})
    assert(e_3.prime_factorize(3) == {3: 1})   

    assert(combination(1, 0, 10**9+7) == 1)
    assert(combination(100, 0, 10**9+7) == 1)
    assert(combination(1, 1, 10**9+7) == 1)
    assert(combination(100, 1, 10**9+7) == 100)

    print(" * assertion test ok * ")