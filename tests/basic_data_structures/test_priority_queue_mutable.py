import pytest
from random import randint, shuffle
from operator import itemgetter
from itertools import count
from mypkg.basic_data_structures.priority_queue_mutable import OriginalPQueue


def test_original_pqueue_handmade():
    """
    実装メソッドが機能するか最低限調べる。
    """
    # test for min pqueue
    L = ['moo', 'meow', 'bow', 'wow', 'cow', 'tweet', 'oink', 'caw', 'cheep', 'roar', 'baaaa']
    pr = list(range(1, len(L) + 1))
    
    for _ in range(100):
        shuffle(pr)

        P = OriginalPQueue(max_pqueue=False)

        for i in range(len(L)):
            P.add_task(L[i], pr[i])
        
        assert not P.empty()
        assert P.size == len(L)
        P.task_change_key('moo', 0)
        assert P.pop_task()[0] == 'moo'

        tmp = list(map(lambda x: x[2], sorted(P.pq)))
        buf = []
        while not P.empty():
            buf.append(P.pop_task()[0])
        assert tmp == buf
    
    # test for max pqueue
    for _ in range(100):
        Q = OriginalPQueue(max_pqueue=True)

        for i in range(len(L)):
            Q.add_task(L[i], pr[i])
        
        assert not Q.empty()
        assert Q.size == len(L)
        Q.task_change_key('moo', 1000)
        assert Q.pop_task()[0] == 'moo'

        tmp = list(map(lambda x: x[2], sorted(Q.pq, reverse=True)))
        buf = []
        while not Q.empty():
            buf.append(Q.pop_task()[0])
        assert tmp == buf



def test_original_pqueue_min():
    """
    (task, priority) でエントリを追加、取り出し、覗き見、優先度を変更を最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最小のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 40
    for _ in range(Iteration):
        pq = OriginalPQueue(max_pqueue=False)
        L = []
        cnt = count()
        for _ in range(M):
            dice = randint(0, 3)
            # push する
            if pq.empty() or dice == 0:
                task_id = next(cnt)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_id, task_pr)
                L.append([task_id, task_pr])    # priority を変更するのでリストで追加
                L.sort(key=itemgetter(1))
            # pop する
            elif dice == 1:
                task_id, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove([task_id, task_pr])
            # peek する
            elif dice == 2:
                task_id, task_pr = pq.peek()
                assert task_pr == L[0][1]
            # change_key する
            else:
                ind = randint(0, len(L) - 1)
                new_priority = randint(-10000, 10000)
                pq.task_change_key(L[ind][0], new_priority)
                L[ind][1] = new_priority
                L.sort(key=itemgetter(1))
                


def test_original_pqueue_max():
    """
    (task, priority) でエントリを追加、取り出し、覗き見、削除を最大 M 回行うことを全 Iteration 回繰り返す。
    それぞれについて取り出した結果が現在 priority が最大のものになっているか愚直に判定するストレステストを行う。
    """
    Iteration = 100
    M = 40
    for _ in range(Iteration):
        pq = OriginalPQueue(max_pqueue=True)
        L = []
        cnt = count()
        for _ in range(M):
            dice = randint(0, 3)
            # push する
            if pq.empty() or dice == 0:
                task_id = next(cnt)
                task_pr = randint(-10000, 10000)
                pq.add_task(task_id, task_pr)
                L.append([task_id, task_pr])    # priority を変更するのでリストで追加
                L.sort(key=itemgetter(1), reverse=True)
            # pop する
            elif dice == 2:
                task_id, task_pr = pq.pop_task()
                # L の先頭と priority が一致していれば OK
                assert task_pr == L[0][1]
                L.remove([task_id, task_pr])
            # peek する
            elif dice == 2:
                task_id, task_pr = pq.peek()
                assert task_pr == L[0][1]                
            # change_key する
            else:
                ind = randint(0, len(L) - 1)
                new_priority = randint(-10000, 10000)
                pq.task_change_key(L[ind][0], new_priority)
                L[ind][1] = new_priority
                L.sort(key=itemgetter(1), reverse=True)





if __name__ == "__main__":
    pytest.main(['-v', __file__])
