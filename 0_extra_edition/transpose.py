def transpose(L_2d):
    """
    二次元リスト L_2d を転置したリストを返す
    
    >>> transpose([[1, 2], [3, 4], [5, 6]])
    [[1, 3, 5], [2, 4, 6]]
    """
    return [list(elm) for elm in zip(*L_2d)]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # for an empty list. shape (n, 0) -> 1d empty list
    assert(transpose([[]]) == [])
    assert(transpose([[], []]) == [])
    assert(transpose([[], [], []]) == [])
    # shape (1, 1) -> (1, 1)
    assert(transpose([[1]]) == [[1]])
    # shape (1, 2) -> (2, 1)
    assert(transpose([[1, 2]]) == [[1], [2]])
    # shape (2, 1) -> (1, 2)
    assert(transpose([[1], [2]]) == [[1, 2]])
    # shape (2, 3) -> (3, 2)
    assert(transpose([[1, 2, 3], [-1, -2, -3]]) == [[1, -1], [2, -2], [3, -3]])
    print(" * assertion test ok * ")

