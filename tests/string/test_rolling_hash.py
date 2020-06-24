import pytest
from random import randint
import os
from mypkg.string.rolling_hash import RollingHash



def test_rolling_hash_covid():
    # どうせだし新型コロナウイルスの塩基配列でも見るか
    genome = ""
    file_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/coronavirus2_wuhan_hu_1_genome.txt")
    with open(file_path) as f:
        for _ in range(4):
            f.readline()
        for line in f.readlines():
            genome += ''.join(line.split()[1:])
    rolling = RollingHash(genome)
    pattern = "tt gtgcagaatg aattctcgta actacatagc acaa".replace(' ', '')    # この塩基配列は pseudoknot stem-loop らしい
    # print(f"let's search '{pattern}' that represents a pseudoknot stem-loop!'")
    for i, j in rolling.find_all(pattern):
        assert i == 29608 and j == 29644
        # print(f" * pattern matched with genome[{i}:{j}] *")    # * pattern matched with genome[29608:29644] *



def test_rolling_hash_find_all():
    """
    長さ 10 ** 3 である a - e からなるランダム文字を Iteration 回生成し、それぞれについて部分文字列 (最大長 10 程度) のランダム検索クエリを Iteration 回投げる。
    毎回愚直に区間が正しいか判定を行うストレステストを行う。
    """
    Iteration = 10
    M = 10 ** 3
    for _ in range(Iteration):
        S = ''.join([chr(randint(0, 4) + ord('a')) for _ in range(M)])
        rolling = RollingHash(S)
        for _ in range(Iteration):
            sub_len = randint(1, 10)
            substring = ''.join([chr(randint(0, 25) + ord('a')) for _ in range(sub_len)])
            got = list(rolling.find_all(substring))
            expected = []
            for i in range(M - sub_len + 1):
                if S[i:i+sub_len] == substring:
                    expected.append((i, i+sub_len))
            assert got == expected




if __name__ == "__main__":
    import doctest
    doctest.testmod()

