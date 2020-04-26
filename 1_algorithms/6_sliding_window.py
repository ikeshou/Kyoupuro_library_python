#!/usr/bin/env python3
"""
スライド最小値

長さ n の数列 a_1, a_2, ..., a_n に対し、長さ k の部分数列 a_i, a_(i+1), ..., a_(i+k-1) を考える。
1 <= i <= n-k+1 に対してこの部分数列の最小値 b_i を求めたい。
ナイーブに比較演算を行うと O(n) * O(k) かかるが、スライド最小値のアルゴリズムにより、これを O(n) に落とすことができる。
(RMQ をさばく segment tree だと O(nlgn))

(0-index)
deque Q を用意する。
Q にはむこう k 個の数列の要素のうち、最小要素, 2 番目の順序統計量, 3 番目の順序統計量... と順に 'もとの並び順を尊重して' 限界まで取っていった時のインデックスが保存されているとする。 
(入るインデックスもその指し示す値も広義単調増加)
当然 Q の先頭がこのクエリの答えとなる。
スライドにより Q の先頭が落ちてもむこう k-1 個の最小要素が先頭に存在してくれる。
    窓のスライドの際いかにこの Q を管理するか？ (ループ不変条件を維持するか？)
    -> スライドを行うと一つ数列の要素 x を読み込むことになる。現在 Q に残っている要素のうち x 以上のものは不要 (最小が上書きされる)。末尾からそれらを全て pop して x を追加。
       Q の先頭は index が対象範囲から外れている可能性がある。チェックし対象範囲から外れていたら popleft する。
"""


from collections import deque

def sliding_minimum_query(L, k):
    """
    Args:
        L (list): 正の数列
        k (int)
    Returns:
        list: L の各要素を先頭とする k 部分列を考え、その最小値を対応する要素に記録したリスト
    """
    n = len(L)
    if k > n:
        raise IndexError(f"window size is greater than the length of sequence. got sequence: {L}, window size: {k}")
    ans = []
    Q = deque()
    for j in range(k):
        while Q and L[Q[-1]] >= L[j]:
            Q.pop()
        Q.append(j)
    # L が空の時に Q は空になりうることに注意 (コーナーケース)
    if Q:
        ans.append(L[Q[0]])
    for j in range(k, n):
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
    assert(sliding_minimum_query([], 0) == [])
    print(" * assertion test ok *")
