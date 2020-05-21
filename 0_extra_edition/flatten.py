def flatten_with_depth(L, depth=1):
    """
    ネストしたリストである L を depth だけ展開したリストを返す
    depth = 1 の場合 sum(data, []) と同様の挙動となる。その多次元版である。
    
    >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=0)
    [1, 2, [3, [4, 5]]]
    >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=1)
    [1, 2, 3, [4, 5]]
    >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=2)
    [1, 2, 3, 4, 5]

    Args:
        L (list)
        depth (int)
    Returns:
        list
    """
    if depth < 0:
        raise ValueError(f"depth < 0. got {depth}")
    return [elm for item in L for elm in (flatten_with_depth(item, depth-1) if depth != 0 and hasattr(item, '__iter__') else [item])]



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # 深さの指定が実際のネスト数より深くても構わない
    assert(flatten_with_depth([1, 2], depth=0) == [1, 2])
    assert(flatten_with_depth([1, 2], depth=1) == [1, 2])
    assert(flatten_with_depth([1, 2], depth=3) == [1, 2])

    assert(flatten_with_depth([[[1]], [[2]]], depth=0) == [[[1]], [[2]]])
    assert(flatten_with_depth([[[1]], [[2]]], depth=1) == [[1], [2]])
    assert(flatten_with_depth([[[1]], [[2]]], depth=2) == [1, 2])
    print(" * assertion test ok * ")