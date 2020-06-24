import pytest
from random import randint
from mypkg.advanced_data_structures.union_find_tree import UnionFindTree



def test_union_is_same():
    """
    1<=size<=M なるランダムな人数の個別グループを Iteration 回生成。
    毎回 Iteration 回だけ適当に選んだ 2 人を同一グループにまとめることを行い、ナイーブな手法と結果を照らし合わせるストレステストを行う。
    """
    Iteration = 100
    M = 100    # size のマックス値
    for _ in range(Iteration):
        size = randint(1, M)
        naive_grouping = [i for i in range(size)]
        uf = UnionFindTree(size)
        for _ in range(Iteration):
            # 適当に選んだ a, b を同一のグループにまとめる
            a, b = randint(0, size-1), randint(0, size-1)
            group_a, group_b = naive_grouping[a], naive_grouping[b]
            assert (group_a == group_b) == uf.is_same(a, b)
            assert (group_a != group_b) == uf.union(a, b)
            # naive_grouping の方は a のグループを全員 b にする
            for i, elm in enumerate(naive_grouping):
                if elm == group_a:
                    naive_grouping[i] = group_b


def test_akin_num():
    """
    1<=size<=M なるランダムな人数の個別グループを Iteration 回生成。
    毎回 Iteration 回だけ適当に選んだ 2 人を同一グループにまとめることを行い、ナイーブな手法と結果を照らし合わせるストレステストを行う。
    """    
    Iteration = 100
    M = 100    # size のマックス値
    for _ in range(Iteration):
        size = randint(1, M)
        naive_grouping = [i for i in range(size)]
        uf = UnionFindTree(size)
        for _ in range(Iteration):
            a, b = randint(0, size-1), randint(0, size-1)
            group_a, group_b = naive_grouping[a], naive_grouping[b]
            uf.union(a, b)
            for i, elm in enumerate(naive_grouping):
                if elm == group_a:
                    naive_grouping[i] = group_b
        for i in range(size):
            assert uf.akin_num(i) == naive_grouping.count(naive_grouping[i])




if __name__ == "__main__":
    pytest.main(['-v', __file__])
