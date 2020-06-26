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



class BucketRAQ:
    """ 1 点に対する質問クエリ、区間に対する加算クエリ (Range Add Query)"""

    def __init__(self, total_size, chunk_size=512):
        if total_size < chunk_size:
            raise ValueError(f"BucketRAQ.__init__(): chunk size should be <= total_size. got total: {total_size}, chunk: {chunk_size}")
        self.size = total_size    # 列の長さ
        self.chunk_size = chunk_size    # 何個ごとに bucket として分割されるか
        self.chunk_num = (total_size + chunk_size - 1) // chunk_size    # bucket の個数
        self.bucket_add = [0] * self.chunk_num
        self.data = [0] * self.size
    

    def _parent(self, data_ind):
        """データインデックスからバケットのインデックスを得る"""
        return data_ind // self.chunk_size
    
    def _child(self, bucket_ind):
        """バケットインデックスから管轄データのインデックス範囲 [l, r) を得る"""
        l = bucket_ind * self.chunk_size
        r = min((bucket_ind + 1) * self.chunk_size, self.size)
        return l, r
    
    
    def build(self, L):
        """ O(n) で初期配列 L に対応したバケットを構築する"""
        for i, num in enumerate(L):        
            self.data[i] = num
    
    
    def range_add(self, l, r, num):
        ' O(lgn) で [l,r) の区間に num を足す'
        if not (0 <= l <= r <= self.size):
            raise IndexError(f"Bucket_RAQ.range_add(): invalid slices (0 <= l <= r <= {self.size} is required). got l: {l}, r: {r}")
        for bucket_ind in range(self.chunk_num):
            # 現在の bucket の管轄範囲は [i, j)
            i, j = self._child(bucket_ind)
            if r <= i:
                break
            if j <= l:
                continue
            # 対象区間が bucket を包み込んでいる時
            if l <= i and j <= r:
                self.bucket_add[bucket_ind] += num
            # 部分的にかぶっている時、現在のバケットに含まれている対象区間の部分区間のみ計算する
            else:
                for data_ind in range(max(l, i), min(r, j)):
                    self.data[data_ind] += num


    def get(self, i):
        ' O(1) で L[i] を得る'
        return self.bucket_add[self._parent(i)] + self.data[i]



