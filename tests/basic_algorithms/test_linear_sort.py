import pytest
from random import randint
from mypkg.basic_algorithms.linear_sort import counting_sort, counting_sort_destructive, radix_sort



def test_counting_sort_all():
    """
    最大長さが M である、 0 ~ max_num をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか、組み込みの sorted() を用いて調べるストレステストを行う。
    """
    with pytest.raises(ValueError):
        counting_sort([-1, 1, 2, 3], 3)    # lt 0
    with pytest.raises(ValueError):
        counting_sort([0, 1, 2, 3], 2)    # gt k
    
    # empty
    assert (counting_sort([], 0) == [])
    
    # without key function
    Iteration = 100
    M = 100
    max_num = 100
    for _ in range(Iteration):
        size = randint(1, M)
        buf = [randint(0, max_num) for _ in range(size)]
        sorted_buf = sorted(buf)
        assert counting_sort(buf, max_num) == sorted_buf
        counting_sort_destructive(buf, max_num)
        assert buf == sorted_buf
    
    # with key function
    func = lambda x: x % 50
    for _ in range(Iteration):
        size = randint(1, M)
        buf = [randint(0, max_num) for _ in range(size)]
        sorted_buf = sorted(buf, key=func)
        assert counting_sort(buf, max_num, key=func) == sorted_buf
        counting_sort_destructive(buf, max_num, key=func)
        assert buf == sorted_buf
    


def test_radix_sort():
    """
    最大長さが M である、 0 ~ max_num をとる数列を Iteration 回生成する。
    それぞれについて結果が正しいか、組み込みの sorted() を用いて調べるストレステストを行う。
    """    
    # empty
    empty = []
    radix_sort(empty)
    assert empty == []

    Iteration = 100
    M = 100
    max_num = 100
    for _ in range(Iteration):
        size = randint(1, M)
        bucket_bit_size = randint(1, 16)
        buf = [randint(0, max_num) for _ in range(size)]
        sorted_buf = sorted(buf)
        radix_sort(buf, bucket_bit_size)
        assert(buf == sorted_buf)




if __name__ == "__main__":
    pytest.main(['-v', __file__])
