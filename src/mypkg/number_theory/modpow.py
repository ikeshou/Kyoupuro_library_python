"""
組み込みの pow() はユークリッドの互除法で実装されている

pow(a, r, m):
    O(lgr)
    整数 a, r に対し a ** r (mod m) を求める
"""


def modpow(a, r, mod):
    """
    O(lgr) で a ** r (mod m) を求める
    Args:
        a, r, mod (int): r >= 0, mod > 0
    Returns:
        int
    Examples:
        >>> modpow(2, 10000, 10**9+7)
        905611805
    """
    assert r >= 0 and mod > 0
    if r == 0:
        return 1
    if r % 2 == 0:
        return (modpow(a, r//2, mod) ** 2) % mod
    else:
        return(modpow(a, r-1, mod) * a) % mod



if __name__ == "__main__":
    import doctest
    doctest.testmod()