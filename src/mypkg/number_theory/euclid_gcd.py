"""
組み込みの math.gcd() はユークリッドの互除法で実装されている

euclid_gcd(a, b):
    O(lg(a + b))
    a, b の gcd を求める

ext_gcd(a, b):
    O(lg(a + b))
    ax + by = d (=gcd(a, b)) なる x, y, d を求める
"""


def euclid_gcd(a: int, b: int) -> int:
    """
    O(lg(a + b)) でユークリッドの互除法により gcd(a, b) を計算

    Args:
        a, b (int)
    Returns:
        int: gcd(a, b)
    Examples:
        >>> euclid_gcd(74, 54)
        2
    Note:
        gcd(a, b) = gcd(b, r) である (但し r = a % b とする)
        a, b に負の値が指定された場合 gcd(abs(a), abs(b)) が返る (math.gcd と同じ)
    """
    def _gcd(a: int, b: int) -> int:
        if b == 0:
            return a
        return _gcd(b, a % b)
    
    a, b = abs(a), abs(b)
    a, b = max(a, b), min(a, b)
    return _gcd(a, b)



def euclid_ext_gcd(a: int, b: int) -> int:
    """
    O(lg(max(a, b))) で拡張ユークリッドの互除法により ax + by = d (=gcd(a, b)) なる x, y, d を求める

    Args:
        a, b (int)
    Returns:
        x, y, d (int): ax + by = d (=gcd(a, b)) なる x, y, d
    Examples:
        >>> euclid_ext_gcd(111, 33)
        (12, -44, 3)
    Note:
        ユークリッド互除法と同様に式変形を行う (以下 a > b > 0 とする)
        ax + by = d
        a = qb + r として
        (qb + r)x + by = d
        b(qx + y) + rx = d
        s = qx + y, x = t として
        bs + rt = d
        係数は (a, b) -> (b, r) と変化していく。最終的には (gcd, 0) となる。解 (s, t) = (1, 0).
        (s, t) が定まったら再帰的に (x, y) を復元することができる。
        s = qx + y, x = t <=> x = t, y = s - qt
    """
    def _ext_gcd(a: int, b: int) -> int:
        if b == 0:
            return (1, 0, a)
        q, r = divmod(a, b)
        s, t, d = _ext_gcd(b, r)
        x, y = t, s - q * t
        return x, y, d
    
    # abs(a) < abs(b) の場合は交換する。解の x, y を入れ替えれば辻褄があう
    swapped = (abs(a) < abs(b))
    if swapped:
        a, b = b, a
    # 負の場合は正に変換して計算をする。解の x, y の符号を反転すれば辻褄があう
    sign_x = 1 if a >= 0 else -1
    sign_y = 1 if b >= 0 else -1
    a, b = abs(a), abs(b)
    x, y, d = _ext_gcd(a, b)
    if swapped:
        return sign_y * y, sign_x * x, d
    else:
        return sign_x * x , sign_y * y, d