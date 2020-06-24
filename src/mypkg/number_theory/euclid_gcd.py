"""
組み込みの math.gcd() はユークリッドの互除法で実装されている

euclid_gcd(a, b):
    O(lg(max(a, b)))
    a, b の gcd を求める
"""


def euclid_gcd(a: int, b: int) -> int:
    """
    O(lg(max(a, b))) でユークリッドの互除法により gcd(a, b) を計算

    Args:
        a, b (int)
    Returns:
        int: gcd(a, b)
    Examples:
        >>> euclid_gcd(74, 54)
        2
    Note:
        gcd(a, b) = gcd(b, r) である (但し r = a % b とする)
        a, b に負の値が指定された場合 gcd(abs(a), abs(b)) が変える (math.gcd と同じ)
    """
    a, b = abs(a), abs(b)
    a, b = max(a, b), min(a, b)
    if b == 0:
        return a
    return euclid_gcd(b, a % b)