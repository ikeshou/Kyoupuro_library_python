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

class BucketRAQ_RSQ:
    """
    区間に対する変更クエリ、区間に対する質問クエリ (Range Add Query, Range Sum Query)
    bucket_add, bucket_sum を用意すれば良さそう
    RAQ を O(lgn) でさばくために...
        bucket が含まれる場合は bucket_add に、はみ出ている部分は生データに記録
        (含まれる場合、はみ出ている場合共に) bucket_sum も更新
    RSQ を O(lgn) でさばくために...
        bucket が含まれる場合は対応する bucket_sum を、はみ出ている部分は生データを参照したいが...
        はみ出ている生データは更新がスキップされている可能性がある。bucket_add を見て記録があればこの bucket 全要素に変更を伝播させる。bucket_add 記録をなくす。その上で参照。
    """
    def __init__(self, L):
        self.size = len(L)
        self.chunk = math.ceil(math.sqrt(self.size))    # 何個ごとに bucket として分割されるか。ceil を取っているのでこれだけ上位の箱を用意すれば十分
        self.data = L        
        self.bucket_add = [None] * self.chunk
        self.bucket_sum = [sum(self.data[self._child_left_close(parent_ind):self._child_right_open(parent_ind)]) for parent_ind in range(self.chunk)]
    
    def _parent(self, data_ind):
        return math.ceil((data_ind + 1) / self.chunk) - 1
    
    def _child_left_close(self, bucket_ind):
        return bucket_ind * self.chunk
    
    def _child_right_open(self, bucket_ind):
        return min((bucket_ind + 1) * self.chunk, self.size)
    
    def range_add(self, l, r, num):
        '[l,r), つまり L[l], ..., L[r-1] に num を足す'
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
                if self.bucket_add[bucket_ind] is None:
                    self.bucket_add[bucket_ind] = 0
                self.bucket_add[bucket_ind] += num
                self.bucket_sum[bucket_ind] += (num * (self._child_right_open(bucket_ind) - self._child_left_close(bucket_ind)))
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                for i in range(max(l, x), min(r, y)):
                    self.data[i] += num
                key = self.bucket_add[bucket_ind]
                if key is not None:
                    self.bucket_add[bucket_ind] = None
                    for i in range(self._child_left_close(bucket_ind), self._child_right_open(bucket_ind)):
                        self.data[i] += key
                self.bucket_sum[bucket_ind] = sum(self.data[self._child_left_close(bucket_ind):self._child_right_open(bucket_ind)])
        
    def summation(self, l, r):
        '[l,r), つまり L[l]+...+L[r-1] を計算する'
        ans = 0
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
                ans += self.bucket_sum[bucket_ind]
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                key = self.bucket_add[bucket_ind]
                if key is not None:
                    self.bucket_add[bucket_ind] = None
                    for i in range(self._child_left_close(bucket_ind), self._child_right_open(bucket_ind)):
                        self.data[i] += key
                for i in range(max(l, x), min(r, y)):
                    ans += self.data[i]
        return ans





if __name__ == "__main__":
    bucket_5 = BucketRAQ_RSQ([0] * 22)    # 22 -> 5+5+5+5+2
    assert(bucket_5.bucket_add == [None,None,None,None,None])
    assert(bucket_5.bucket_sum == [0,0,0,0,0])
    bucket_5.range_add(1,10,1)
    assert(bucket_5.bucket_add == [None,1,None,None,None])
    assert(bucket_5.bucket_sum == [4,5,0,0,0])
    bucket_5.range_add(7,17,2)
    assert(bucket_5.bucket_add == [None,None,2,None,None])
    assert(bucket_5.bucket_sum == [4,11,10,4,0])
    assert(bucket_5.summation(0,22) == 29)

    print(" * assertion test ok *")
