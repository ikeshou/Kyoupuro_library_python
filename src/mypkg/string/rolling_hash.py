"""
ローリングハッシュ
参考：https://qiita.com/keymoon/items/11fac5627672a6d6a9f6

文字列 S の長さ n, マッチング箇所を探したいパターン文字列 P の長さ m とする。
文字列の高速なパターンマッチングを行うアルゴリズム
(前処理に O(n)、全区間の候補に対して O(n)、区間を指定されたときの一致判定に O(1))
(ナイーブに S の各文字を先頭にパターンマッチを行っていくと全区間の候補に対して O(n * m) 、区間を指定されたときの一致判定に O(m)。)

m 個文字が入る窓を 1 文字ずつスライドさせているので共通部分は m-1 個あるのにそれを調べ直しているところが非効率的である。
各文字を数値へと変換し、base 進数表記がなされていると考え、このハッシュ値が一致したかどうかでパターンマッチングを行う。
するとスライドに伴う再計算は O(1) で可能 (最上位の桁を落とす & 残りのものを桁シフトする & 新しく最下位の桁に一文字読み込む)。
これだけで全区間の候補 (s[0:m] to s[(n-m):n]) に対して O(n) が実現できるが...区間を指定されれたとき (s[k:(l+k)] について |T| = l なる新たな T と一致性を調べたいなど) に O(l) かかる。

工夫
h(s[0:k]) = Σ(0...k-1) s[i]*(base)^(k-1-i)
s の各接頭辞についてハッシュを計算しておけば
h(s[i:j]) = h(s[0:j]) - (h(s[0:i]) * (base)^(j-i))
で計算できる。(区間和を高速で計算するために累積和の形でデータを保持するというやつ)

mod の話
base を対象文字の個数 + 1 にでもして 1, 2, ..., 文字の個数 とふり計算すれば良さそうだが... (0 から振るのはダメ)
a-z で 36 個。|s| = O(10^5) とかだと 36^(10^5) で 10^100000 とかになる (無理)
なので衝突をできるだけ回避可能な大きな素数を mod として選び、その数を法とした値で管理する。
独立に N 個の値をとる変数があったときどれかが一致する確率が 50 % を超えるのに必要な変数の個数は約 √N 個であるから (誕生日のパラドックス)、
10^5 個のハッシュ計算で半分以上の確率でかぶらないようにするには 10^10 個の値をハッシュ関数が生成しうるようにする必要がある。32 bit 整数では足りないので 64 bit 整数で mod を用意する。
なお、hack によるロリハ撃墜を避けるために base をランダム生成する戦略を取っている。


verified @ABC141E
"""


from random import randint
from typing import List, Iterator, Tuple


class RollingHash:
    def __init__(self, s: str):
        self.s = s    # パターン探索を行われる側の文字列
        self.size = len(s)
        self.hashmod = 2 ** 64 - 1
        self.base = randint(2 ** 10, 2 ** 11)
        self.hash_list = self._make_rolling_hash_list()

    def _make_rolling_hash_list(self) -> List[int]:
        """
        累積文字列のハッシュ値を記録したテーブルの作成を行う (O(n))
        """
        hash_list = [0] * (self.size + 1)    # [h(s[0:0]), h(s[0:1]), h(s[0:2]), h(s[0:3]), ..., h(s[0:size])]
        prev = 0
        for i in range(1, self.size + 1):
            hash_num = (prev * self.base + ord(self.s[i-1])) % self.hashmod
            hash_list[i] = hash_num
            prev = hash_num
        return hash_list

    def calc_str_hash(self, pattern: str) -> int:
        """
        文字列パターンのハッシュ値の計算を行う (O(L))
        Args:
            pattern (str)
        Returns:
            hash_num (int)
        """
        length = len(pattern)
        hash_num = 0
        for i in range(length):
            hash_num = (hash_num + ord(pattern[i]) * pow(self.base, length - 1 - i, self.hashmod)) % self.hashmod
        return hash_num
    
    def calc_interval_hash(self, i: int, j: int) -> int:
        """
        s[i:j] のハッシュ値の計算を行う (O(1))
        Args:
            i (int): 左の閉区間
            j (int): 右の開区間
        Returns:
            hash_ium (int)
        """
        return (self.hash_list[j] - self.hash_list[i] * pow(self.base, j - i, self.hashmod)) % self.hashmod
    
    def match_predict_with_interval(self, hashed_pattern: int, i: int, j: int) -> bool:
        """
        [i,j), つまり s[i:j] が hashed_pattern と一致するかどうかを判定する (O(1))
        pattern ではなく hashed_pattern であることに注意。
        Args:
            hashed_pattern (int): self.calc_str_hash() で計算された文字列のハッシュ値
            i (int): 左の閉区間
            j (int): 右の開区間
        Returns:
            bool
        """
        if i > j:
            raise IndexError(f'interval should be [i, j) (i <= j). got i: {i} and j: {j}')
        if not isinstance(hashed_pattern, int) or not 0 <= hashed_pattern <= self.hashmod - 1:
            raise ValueError(f'argument must be hashed_pattern (positive integer that is less than {self.hashmod}). got {hashed_pattern}')
        return hashed_pattern == self.calc_interval_hash(i, j)
    
    def find_all(self, target_s: str) -> Iterator[Tuple[int]]:
        """
        target_s と一致する [i,j) つまり s[i:j] を O(n) で探索する

        >>> rolling = RollingHash('abcgbabcgbabcbabcagcabcabgc')
        >>> iter = rolling.find_all('abc')
        >>> print(list(iter))
        [(0, 3), (5, 8), (10, 13), (14, 17), (20, 23)]

        Args:
            target_s (str): s から一致する区間を探索したいターゲットパターン
        Returns:
            iter: マッチした全ての s[i:j] について、 (i, j) のタプルを返すようなイテレータ
        """
        n = len(target_s)
        hashed_target_s = self.calc_str_hash(target_s)
        ans = []
        for i in range(self.size - n + 1):
            if self.match_predict_with_interval(hashed_target_s, i, i + n):
                ans.append((i, i+n))
        return iter(ans)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
