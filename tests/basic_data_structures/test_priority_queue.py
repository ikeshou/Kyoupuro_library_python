import pytest
from random import randint
from operator import itemgetter
from mypkg.basic_data_structures.priority_queue import PQueueMin, PQueueMax


def test_pqueue_min_handmade():
    """
    実装メソッドが機能するか最低限調べる。    
    """
    P = PQueueMin()
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for elm in L:
        P.add_task(elm, randint(1, 100))
    assert not P.empty()
    tmp = list(map(lambda x: x[2], sorted(P.pq)))
    buf = []
    while not P.empty():
        buf.append(P.pop_task()[0])
    assert tmp == buf



def test_pqueue_max_handmade():
    """
    実装メソッドが機能するか最低限調べる。    
    """
    Q = PQueueMax()
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for elm in L:
        Q.add_task(elm, randint(1, 100))
    assert not Q.empty()
    tmp = list(map(lambda x: x[2], sorted(Q.pq)))    # すでに priority は負になっている
    buf = []
    while not Q.empty():
        buf.append(Q.pop_task()[0])
    assert tmp == buf



def test_pqueue_min():
    """
    (task, priority) でエントリを追加することを最大 M 回、取り出すことを最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最小のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 20
    for _ in range(Iteration):
        pq = PQueueMin()
        L = []
        for _ in range(M):
            # push する
            if pq.empty() or randint(0, 1) == 0:
                task_num = randint(0, 100)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_num, task_pr)
                L.append((task_num, task_pr))
                L.sort(key=itemgetter(1))
            # pop する
            else:
                task_num, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove((task_num, task_pr))


def test_pqueue_max():
    """
    (task, priority) でエントリを追加することを最大 M 回、取り出すことを最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最大のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 20
    for _ in range(Iteration):
        pq = PQueueMax()
        L = []
        for _ in range(M):
            # push する
            if pq.empty() or randint(0, 1) == 0:
                task_num = randint(0, 100)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_num, task_pr)
                L.append((task_num, task_pr))
                L.sort(key=itemgetter(1), reverse=True)
            # pop する
            else:
                task_num, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove((task_num, task_pr))




if __name__ == "__main__":
    pytest.main(['-v', __file__])
