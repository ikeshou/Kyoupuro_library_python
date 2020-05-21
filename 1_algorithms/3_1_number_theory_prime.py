#!/usr/bin/env python3
"""
number theory algorithms implemented in Python3 for programming competition

is_prime(n):
    O(√n)
    num が素数かどうか判定する

Eratos:
    __init__(n):
        O(nlglgn) で初期化、num までの素数判定テーブルを作る
    is_prime(n):
        O(1) で素数かどうか判定する
    prime_factorize(n):
        O(√n) (候補の素数を列挙するところが律速) で素因数分解を行う
    enum_divisor(n):
        O(√n) (約数は一方のペアが必ず√n以下である) で小さい順に約数の列挙を行う
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


import math
class Eratos:
    def __init__(self, num):
        """
        O(nlglgn) で num までの素数判定テーブルを作る
        >>> e = Eratos(10)
        >>> e.table
        [False, False, True, True, False, True, False, True, False, False, False]
        """
        assert(num >= 1)
        self.table_max = num
        # self.table[i] は i が素数かどうかを示す (bool)
        self.table = [False if i == 0 or i == 1 else True for i in range(num+1)]
        for i in range(2, int(math.sqrt(num)) + 1):
            if self.table[i]:
                for j in range(i ** 2, num + 1, i):    # i**2 からスタートすることで定数倍高速化できる
                    self.table[j] = False
    
    def is_prime(self, num):
        """
        O(1) で素数判定を行う
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
        O(√n) で素因数分解を行う
        >>> e = Eratos(10000)
        >>> e.prime_factorize(6552)
        {2: 3, 3: 2, 7: 1, 13: 1}
        """
        assert(num >= 1)
        if int(math.sqrt(num)) > self.table_max:
            raise ValueError('Eratos.prime_factorize(): exceed prime table size. got {}'.format(num))
        # 素因数分解の結果を記録する辞書        
        factorized_dict = dict()
        candidate_prime_numbers = [i for i in range(2, int(math.sqrt(num)) + 1) if self.is_prime(i)]
        # n について、√n 以下の素数で割り続けると最後には 1 or 素数となる
        # 背理法を考えれば自明 (残された数が √n より上の素数の積であると仮定。これは自明に n を超えるため矛盾)
        for p in candidate_prime_numbers:
            if num == 1:    # これ以上調査は無意味
                break
            if num % p == 0:
                cnt = 0
                while num % p == 0:
                    num //= p
                    cnt += 1
                factorized_dict[p] = cnt
        if num != 1:
            factorized_dict[num] = 1
        return factorized_dict
    
    def enum_divisor(self, num):
        """
        O(√n) で約数列挙を行う
        >>> e = Eratos(10000)
        >>> e.enum_divisor(4)
        [1, 2, 4]
        >>> e.enum_divisor(19)
        [1, 19]
        >>> e.enum_divisor(100)
        [1, 2, 4, 5, 10, 20, 25, 50, 100]
        """
        divisor_small = []
        divisor_large = []
        for i in range(1, int(math.sqrt(num)) + 1):
            if num % i == 0:
                divisor_small.append(i)
                if i != num // i:
                    divisor_large.append(num // i)
        divisor_large.reverse()
        return divisor_small + divisor_large
# =======================



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # check the corner cases!
    assert(is_prime(1) == False)
    assert(is_prime(2) == True)
    assert(is_prime(3) == True)

    e_1 = Eratos(1)
    assert(e_1.is_prime(1) == False)
    assert(e_1.prime_factorize(1) == {})
    e_2 = Eratos(2)
    assert(e_2.is_prime(1) == False)
    assert(e_2.is_prime(2) == True)
    assert(e_2.prime_factorize(1) == {})
    assert(e_2.prime_factorize(2) == {2: 1})
    e_3 = Eratos(3)
    assert(e_3.is_prime(1) == False)
    assert(e_3.is_prime(2) == True)
    assert(e_3.is_prime(3) == True)
    assert(e_3.prime_factorize(1) == {})
    assert(e_3.prime_factorize(2) == {2: 1})
    assert(e_3.prime_factorize(3) == {3: 1})

    print(" * assertion test ok * ")
