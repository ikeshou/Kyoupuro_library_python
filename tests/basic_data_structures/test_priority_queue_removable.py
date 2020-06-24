import pytest
from random import randint
from operator import itemgetter
from itertools import count
from mypkg.basic_data_structures.priority_queue_removable import RemovablePQueue


def test_removable_pqueue_handmade():
    """
    実装メソッドが機能するか最低限調べる。
    """
    # test for min pqueue
    P = RemovablePQueue(max_pqueue=False)
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    for i in range(len(L)):
        P.add_task(L[i], len(L)-i)
    
    assert not P.empty()
    P.remove_task('moo')
    P.remove_task('bow')
    P.remove_task('wow')
    P.remove_task('cow')
    P.remove_task('baaaa')

    with pytest.raises(ValueError):
        P.remove_task('moo')
    with pytest.raises(ValueError):
        P.remove_task('non-existent-key')

    buf = []
    while not P.empty():
        buf.append(P.pop_task()[0])
    assert buf == ['roar', 'cheep', 'caw', 'oink', 'tweet', 'meow']

    # test for max pqueue
    Q = RemovablePQueue(max_pqueue=True)
    for i in range(len(L)):
        Q.add_task(L[i], i)
    
    assert not Q.empty()
    Q.remove_task('moo')
    Q.remove_task('bow')
    Q.remove_task('wow')
    Q.remove_task('cow')
    Q.remove_task('baaaa')

    with pytest.raises(ValueError):
        Q.remove_task('moo')
    with pytest.raises(ValueError):
        Q.remove_task('non-existent-key')

    buf = []
    while not Q.empty():
        buf.append(Q.pop_task()[0])
    assert buf == ['roar', 'cheep', 'caw', 'oink', 'tweet', 'meow']




def test_removable_pqueue_min():
    """
    (task, priority) でエントリを追加、取り出し、覗き見、削除を最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最小のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 40
    for _ in range(Iteration):
        pq = RemovablePQueue(max_pqueue=False)
        L = []
        cnt = count()
        for _ in range(M):
            dice = randint(0, 3)
            # push する
            if pq.empty() or dice == 0:
                task_id = next(cnt)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_id, task_pr)
                L.append((task_id, task_pr))
                L.sort(key=itemgetter(1))
            # pop する
            elif dice == 1:
                task_id, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove((task_id, task_pr))
            # peek する
            elif dice == 2:
                task_id, task_pr = pq.peek()
                assert task_pr == L[0][1]
            # remove する
            else:
                ind = randint(0, len(L) - 1)
                pq.remove_task(L[ind][0])
                del L[ind]
                


def test_removable_pqueue_max():
    """
    (task, priority) でエントリを追加、取り出し、覗き見、削除を最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最大のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 40
    for _ in range(Iteration):
        pq = RemovablePQueue(max_pqueue=True)
        L = []
        cnt = count()
        for _ in range(M):
            dice = randint(0, 3)
            # push する
            if pq.empty() or dice == 0:
                task_id = next(cnt)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_id, task_pr)
                L.append((task_id, task_pr))
                L.sort(key=itemgetter(1), reverse=True)
            # pop する
            elif dice == 2:
                task_id, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove((task_id, task_pr))
            # peek する
            elif dice == 2:
                task_id, task_pr = pq.peek()
                assert task_pr == L[0][1]                
            # remove する
            else:
                ind = randint(0, len(L) - 1)
                pq.remove_task(L[ind][0])
                del L[ind]







if __name__ == "__main__":
    pytest.main(['-v', __file__])
