"""
スライド最小値

<algorithm>
長さ n の数列 L に対し、長さ k の連続部分数列を考える。L[i:i+k] (0<=i<=n-k) に対してこの連続部分数列の最小値を求めたい。
ナイーブに比較演算を行うと O(n * k) 、RMQ をさばくセグ木だと O(nlgn) だが、スライド最小値のアルゴリズムでは O(n) で計算可能。
"""



from collections import deque
from typing import List, Sequence, Union

Num = Union[int, float]


def sliding_minimum_query(L: Sequence[Num], k: int) -> List[Num]:
    """
    O(n) で L[i:i+k] (0<=i<=n-k) の最小値をそれぞれ計算しリストにまとめる

    Args:
        L (sequence): 正の数列
        k (int): 要素数 k の L の連続部分列を考え、その最小値のクエリに答えていく

    Returns:
        list: L の各要素を先頭とする k 連続部分列を考え、その最小値を対応する要素に記録したリスト
    
    Raises:
        ValueError: k < 1 のとき
        IndexError: k > n のとき
    
    Examples:
        >>> sliding_minimum_query([1, 5, 3, 6, 9, 9, 2, 1, 8], 3)
        [1, 3, 3, 6, 2, 1, 1]
    
    Notes:
        Q にはむこう k 個の数列の要素のうち、最小要素, 2 番目の順序統計量, 3 番目の順序統計量... と順に「もとの並び順を尊重して」
        限界まで取っていった時のインデックスが保存される (入るインデックスもその指し示す値も広義単調増加。これらは区間最小値の候補である)
        スライドを行うと一つ数列の要素 x を読み込むことになる。
        現在 Q に残っている要素のうち x 以上のものは不要 (最小が上書きされる)。末尾からそれらを全て pop して x を追加。
        Q の先頭は index が対象範囲から外れている可能性がある。チェックし対象範囲から外れていたら popleft する。
    """
    n = len(L)
    if k < 1:
        raise ValueError(f"sliding_minimum_query(): window size should be >= 1. got {k}")
    if k > n:
        raise IndexError(f"sliding_minimum_query(): window size is greater than the length of sequence. got sequence: {L}, window size: {k}")
    # ans[i] には L[i:i+k] の最小値が保存される
    ans = []
    # 最初の Q (の直前まで、L[0:k-1]に対する処理) を作成しておく
    Q = deque()
    for j in range(k-1):
        while Q and L[Q[-1]] >= L[j]:
            Q.pop()
        Q.append(j)
    # L[0:k] に対する処理、つまり L[k-1] を読みに行くところからスタートする
    for j in range(k-1, n):
        i = j - k + 1
        while Q and L[Q[-1]] >= L[j]:
            Q.pop()
        Q.append(j)
        if Q[0] < i:
            Q.popleft()
        ans.append(L[Q[0]])
    return ans



if __name__ == "__main__":
    L = [1,5,2,4,7,12,14,65,43,8,9,10,0,3,5,7,9,100]
    assert(sliding_minimum_query(L, 4) == [1,2,2,4,7,12,8,8,8,0,0,0,0,3,5])
    assert(sliding_minimum_query(L, 8) == [1,2,2,4,7,0,0,0,0,0,0])

    assert(sliding_minimum_query([1], 1) == [1])
    assert(sliding_minimum_query([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4, 5])
    print(" * assertion test ok *")
