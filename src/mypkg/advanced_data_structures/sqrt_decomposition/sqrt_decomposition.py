#!/usr/bin/env python3
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
RSQ: 1 点に対する変更、区間に対する和をそれぞれ O(1), O(lgn) で処理できる
RMQ: 1 点に対する変更、区間に対する最小値をそれぞれ O(lgn), O(lgn) で処理できる
RAQ: 区間に対する変更 (add)、1 点に対する値をそれぞれ O(lgn), O(1) で処理できる
RUQ: 区間に対する変更 (update)、1 点に対する値をそれぞれ O(lgn), O(lgn) で処理する
RAQ_RSQ: 区間に対する変更 (add)、区間に対する和をそれぞれ O(lgn), O(lgn) で処理できる
"""

import math
class BucketRSQ:
    '1 点に対する変更クエリ、区間に対する質問クエリ (Range Sum Query)'
    def __init__(self, L):
        self.size = len(L)
        self.chunk = math.ceil(math.sqrt(self.size))    # 何個ごとに bucket として分割されるか。ceil を取っているのでこれだけ上位の箱を用意すれば十分
        self.bucket_sum = [0] * self.chunk
        self.data = [0] * self.size
        for ind, elm in enumerate(L):
            self._add(ind, elm)
    
    def _parent(self, data_ind):
        return math.ceil((data_ind + 1) / self.chunk) - 1
    
    def _child_left_close(self, bucket_ind):
        return bucket_ind * self.chunk
    
    def _child_right_open(self, bucket_ind):
        return min((bucket_ind + 1) * self.chunk, self.size)
    
    def _add(self, i, x):
        'L[i] に x を足す'
        self.data[i] += x
        self.bucket_sum[self._parent(i)] += x
    
    def update(self, i, x):
        'L[i] を x に変更する'
        diff = x - self.data[i]
        self._add(i, diff)
    
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
                for i in range(max(l, x), min(r, y)):
                    ans += self.data[i]
        return ans


class BucketRMQ:
    '1 点に対する変更クエリ、区間に対する質問クエリ (Range Minimum Query)'
    def __init__(self, L):
        self.size = len(L)
        self.chunk = math.ceil(math.sqrt(self.size))    # 何個ごとに bucket として分割されるか。ceil を取っているのでこれだけ上位の箱を用意すれば十分
        self.bucket_min = [0] * self.chunk
        self.data = L
        for bucket_ind in range(self.chunk):
            self.bucket_min[bucket_ind] = min(self.data[self._child_left_close(bucket_ind):self._child_right_open(bucket_ind)])
    
    def _parent(self, data_ind):
        return math.ceil((data_ind + 1) / self.chunk) - 1
    
    def _child_left_close(self, bucket_ind):
        return bucket_ind * self.chunk
    
    def _child_right_open(self, bucket_ind):
        return min((bucket_ind + 1) * self.chunk, self.size)
    
    def update(self, i, x):
        'L[i] を x に変更する'
        self.data[i] = x
        bucket_ind = self._parent(i)
        self.bucket_min[bucket_ind] = min(self.data[self._child_left_close(bucket_ind):self._child_right_open(bucket_ind)])
    
    def minimum(self, l, r):
        '[l,r), つまり min(L[l], ..., L[r-1]) を計算する'
        ans = float('inf')
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
                ans = min(ans, self.bucket_min[bucket_ind])
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                for i in range(max(l, x), min(r, y)):
                    ans = min(ans, self.data[i])
        return ans


class BucketRAQ:
    '区間に対する変更クエリ、一点に対する質問クエリ (Range Add Query)'
    def __init__(self, L):
        self.size = len(L)
        self.chunk = math.ceil(math.sqrt(self.size))    # 何個ごとに bucket として分割されるか。ceil を取っているのでこれだけ上位の箱を用意すれば十分
        self.bucket_add = [0] * self.chunk    # range_add のクエリに対し、bucket が完全に含まれているものに対してはここで記録を引き受ける
        self.data = L
    
    def _parent(self, data_ind):
        return math.ceil((data_ind + 1) / self.chunk) - 1
    
    def _child_left_close(self, bucket_ind):
        return bucket_ind * self.chunk
    
    def _child_right_open(self, bucket_ind):
        return min((bucket_ind + 1) * self.chunk, self.size)
    
    def range_add(self, l, r, num):
        '[l,r), つまり L[l],...,L[r-1] に num を足す'
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
                self.bucket_add[bucket_ind] += num
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                for i in range(max(l, x), min(r, y)):
                    self.data[i] += num   

    def get(self, i):
        'L[i] を得る'
        return self.bucket_add[self._parent(i)] + self.data[i]
    


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
    bucket_1 = BucketRSQ([1,3,2,6,7,4,3,0,8,4,3,5,9,2,1])    # 15 -> 4+4+4+3
    assert(bucket_1.bucket_sum == [12,14,20,12])
    bucket_1.update(7,2)
    assert(bucket_1.bucket_sum == [12,16,20,12])
    assert(bucket_1.summation(2,9) == 32)
    assert(bucket_1.summation(0,1) == 1)
    assert(bucket_1.summation(1,3) == 5)
    print("BucketRSQ test passed.")

    bucket_2 = BucketRMQ([1,3,2,6,7,4,3,0,8,4,3,5,9,2,1])    # 15 -> 4+4+4+3
    assert(bucket_2.bucket_min == [1,0,3,1])
    bucket_2.update(9,1)
    assert(bucket_2.bucket_min == [1,0,1,1])
    assert(bucket_2.minimum(6,14) == 0)
    assert(bucket_2.minimum(0,1) == 1)
    assert(bucket_2.minimum(1,3) == 2)
    print("BucketRMQ test passed.")

    bucket_3 = BucketRAQ([1,3,2,6,7,4,3,0,8,4,3,5,9,2,1])    # 15 -> 4+4+4+3
    assert(bucket_3.bucket_add == [0,0,0,0])
    bucket_3.range_add(0,6,1)
    assert(bucket_3.bucket_add == [1,0,0,0])
    assert(bucket_3.data == [1,3,2,6,8,5,3,0,8,4,3,5,9,2,1])
    bucket_3.range_add(8,12,2)
    assert(bucket_3.bucket_add == [1,0,2,0])
    assert(bucket_3.data == [1,3,2,6,8,5,3,0,8,4,3,5,9,2,1])
    assert(bucket_3.get(4) == 8)
    assert(bucket_3.get(10) == 5)
    print("BucketRAQ test passed")

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
    print("BucketRUQ test passed.")

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
    print("BucketRAQ_RSQ test passed.")

    print(" * assertion test ok *")
