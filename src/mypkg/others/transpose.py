from typing import TypeVar, List, Union, Sequence
T = TypeVar('T')

def transpose(L_2d: Sequence[Sequence[T]]) -> List[List[T]]:
    """
    二次元シーケンス L_2d を転置したリストを返す
    
    Args:
        L_2d (sequence)
    Returns:
        list: L_2d を転置したリスト
    Raises:
        TypeError: L_2d の shape が (n, m) (n >= 1 and m >= 1) で表されないとき
    Examples:
        >>> transpose([[1, 2], [3, 4], [5, 6]])
        [[1, 3, 5], [2, 4, 6]]
    """
    if not (hasattr(L_2d, '__iter__') and hasattr(L_2d[0], '__iter__')):
        raise TypeError(f"transpose(): argument should be two-dim sequence. got {L_2d}")
    if not (len(L_2d) >= 1 and len(L_2d[0]) >= 1):
        raise TypeError(f"transpose(): argument shape should be (n, m) (n >= 1, m >= 1). got {L_2d}")
    return [list(elm) for elm in zip(*L_2d)]



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    assert(transpose([[1]]) == [[1]])    # shape (1, 1) -> (1, 1)
    assert(transpose([[1, 2]]) == [[1], [2]])    # shape (1, 2) -> (2, 1)
    assert(transpose([[1], [2]]) == [[1, 2]])    # shape (2, 1) -> (1, 2)
    assert(transpose([[1, 2, 3], [-1, -2, -3]]) == [[1, -1], [2, -2], [3, -3]])    # shape (2, 3) -> (3, 2)

    print(" * assertion test ok * ")

