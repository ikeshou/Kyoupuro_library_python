"""
平方分割
参考：https://kujira16.hateblo.jp/entry/2016/12/15/000000

セグ木が 2 分木 1+lgn 段 (n = power of 2 とした) で区間の計算結果を保持していたのに対し、平方分割では √n 分木 1+1 段で区間の計算結果を保持する。
前処理はセグ木同様に O(n), 区間に対するクエリの処理は O(√n) である。計算量は多少増えるがキャッシュヒットしやすいので実は定数倍程度しか重くならないらしい。

多段構成でないため区間に対するクエリなどが捌きやすい。
区間に対する変更などは完全に覆われた平方分割されたブロックに対しては O(1) で処理を済ますことにより (補助データとか使って頑張る)、 高々ブロックは O(√n) 個なので O(√n)
はみ出たものに対しては一つ一つ O(1) で処理を行うことで O(2√n) = O(√n)
トータルで O(√n) で捌くことができた。
ポイントは
区間クエリのうち完全に含まれた bucket に対しては O(1) で処理を行えること
区間クエリのうちはみ出た 1 つ 1 つのクエリに対しては O(1) で処理を行えること
単体クエリの場合、自身と包含する bucket を O(lgn) で処理できること


* case study *
RSQ: 1 点に対する変更、区間に対する和
RMQ: 1 点に対する変更、区間に対する最小値
RAQ: 区間に対する変更 (add)、1 点に対する値
RUQ: 区間に対する変更 (update)、1 点に対する値
RAQ_RSQ: 区間に対する変更 (add)、区間に対する和
"""


import math


class BucketRUQ:
    '区間に対する変更クエリ、一点に対する質問クエリ (Range Update Query)'
    def __init__(self, L):
        self.size = len(L)
        self.chunk = math.ceil(math.sqrt(self.size))    # 何個ごとに bucket として分割されるか。ceil を取っているのでこれだけ上位の箱を用意すれば十分
        self.bucket_updated = [None] * self.chunk    # range_update のクエリに対し、bucket が完全に含まれているものに対してはここで記録を引き受ける
        self.data = L
    
    def _parent(self, data_ind):
        return math.ceil((data_ind + 1) / self.chunk) - 1
    
    def _child_left_close(self, bucket_ind):
        return bucket_ind * self.chunk
    
    def _child_right_open(self, bucket_ind):
        return min((bucket_ind + 1) * self.chunk, self.size)
    
    def range_update(self, l, r, num):
        '[l,r), つまり L[l],...,L[r-1] を num に変更する'
        for bucket_ind in range(self.chunk):
            # 現在の bucket の管轄範囲は [x, y)
            x = self._child_left_close(bucket_ind)
            y = self._child_right_open(bucket_ind)
            if r <= x:
                break
            if y <= l:
                continue
            # 対象区間が bucket を包み込んでいる時
            if l <= x and y <= r:
                self.bucket_updated[bucket_ind] = num
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                # 先に updated の変更を伝播させて未処理の update は存在しないようにしておく (そうしないと過去の updated で今回の部分的な変更が上書きされちゃう)
                key = self.bucket_updated[bucket_ind]
                if key is not None:
                    self.bucket_updated[bucket_ind] = None
                    for data_ind in range(self._child_left_close(bucket_ind), self._child_right_open(bucket_ind)):
                        self.data[data_ind] = key
                for i in range(max(l, x), min(r, y)):
                    self.data[i] = num
    
    def get(self, i):
        'L[i] を得る'
        return self.bucket_updated[self._parent(i)] if self.bucket_updated[self._parent(i)] else self.data[i]


if __name__ == "__main__":
    bucket_4 = BucketRUQ([0,0,0,0,0,0,0,0])    # 8 -> 3+3+2
    assert(bucket_4.bucket_updated == [None,None,None])
    bucket_4.range_update(0,4,1)
    assert(bucket_4.bucket_updated == [1,None,None])
    assert(bucket_4.data == [0,0,0,1,0,0,0,0])
    bucket_4.range_update(3,7,2)
    assert(bucket_4.bucket_updated == [1,2,None]) 
    assert(bucket_4.data == [0,0,0,1,0,0,2,0])    # data[3] は 1 が残っているが updated の方に 2 が入っているので上書きされたも同然
    assert(bucket_4.get(0) == 1)
    assert(bucket_4.get(3) == 2)
    assert(bucket_4.get(5) == 2)
    bucket_4.range_update(1,9,3)
    assert(bucket_4.bucket_updated == [None,3,3])    # 部分的にかぶっている部分の変更は予め伝播される
    assert(bucket_4.data == [1,3,3,1,0,0,2,0])
    assert(bucket_4.get(7) == 3)
    print(" * assertion test ok *")
