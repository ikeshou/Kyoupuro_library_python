from typing import Any, Sequence, List

def flatten_with_depth(L: Sequence[Any], depth: int=1) -> List[Any]:
    """
    ネストしたリストである L を depth だけ展開したリストを返す。
    depth = 1 の場合 sum(data, []) と同様の挙動となる。この関数はその多次元版である。
    depth が実際のネストより深い場合は限界まで展開を行う。
    
    Args:
        L (list)
        depth (int)

    Returns:
        list

    Raises:
        ValueError: depth < 0 のとき  
        
    Examples:
        >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=0)
        [1, 2, [3, [4, 5]]]
        >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=1)
        [1, 2, 3, [4, 5]]
        >>> flatten_with_depth([1, 2, [3, [4, 5]]], depth=5)
        [1, 2, 3, 4, 5]
    """
    if depth < 0:
        raise ValueError(f"flattern_with_depth(): depth should be >= 0. got {depth}")
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