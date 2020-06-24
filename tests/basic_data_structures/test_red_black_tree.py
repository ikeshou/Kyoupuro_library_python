import pytest
from random import randint
from math import ceil, log2
from collections import defaultdict
from mypkg.basic_data_structures.red_black_tree import RED, BLACK, Vertex, RedBlcakTree



def test_red_black_tree_handmade():
    """
    実装メソッドが最低限機能するか、ノードの色がシミュレーション通りに配色されるか気合で調べる。
    """

    rb_tree = RedBlcakTree()
    assert(str(rb_tree) == '[]')
    assert(len(rb_tree) == 0)
    assert(rb_tree.inorder_traverse() == [])
    assert(rb_tree.preorder_traverse() == [])
    assert(rb_tree.postorder_traverse() == [])
    
    # check the insert() method
    rb_tree.insert(1)
    """
                    1(b)    
    """
    assert(len(rb_tree) == 1)
    assert(rb_tree.root.col == BLACK)
    assert(rb_tree.inorder_traverse() == [1])

    rb_tree.insert(2)
    """
                    1(b)
                                2(r)    
    """
    assert(len(rb_tree) == 2)
    assert(rb_tree.root.col == BLACK)
    assert(rb_tree.root.r.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 2])    

    rb_tree.insert(3)
    """
                    2(b)
        1(b)                     3(b)    
    """
    assert(len(rb_tree) == 3)
    assert(rb_tree.root.col == BLACK)
    assert(rb_tree.root.l.col == BLACK)
    assert(rb_tree.root.r.col == BLACK)
    assert(rb_tree.inorder_traverse() == [1, 2, 3])    
    assert(rb_tree.preorder_traverse() == [2, 1, 3])
    assert(rb_tree.postorder_traverse() == [1, 3, 2])

    rb_tree.insert(2)
    """
                    2(b)
        1(b)                     3(b)
                            2(r)    
    """
    assert(len(rb_tree) == 4)
    assert(rb_tree.root.r.l.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 2, 2, 3])
    assert(rb_tree.preorder_traverse() == [2, 1, 3, 2])
    assert(rb_tree.postorder_traverse() == [1, 2, 3, 2])

    rb_tree.insert(1)
    """
                    2(b)
        1(b)                     3(b)
             1(r)            2(r)
    """
    assert(len(rb_tree) == 5)
    assert(rb_tree.root.l.r.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3])    
    assert(rb_tree.preorder_traverse() == [2, 1, 1, 3, 2])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 3, 2])
    
    rb_tree.insert(4)
    """
                    2(b)
        1(b)                     3(b)
             1(r)            2(r)     4(r)    
    """
    assert(len(rb_tree) == 6)
    assert(rb_tree.root.r.r.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4])    
    assert(rb_tree.preorder_traverse() == [2, 1, 1, 3, 2, 4])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 4, 3, 2])

    rb_tree.insert(7)
    """
                    2(b)
        1(b)                     4(r)
             1(r)            3(b)     7(b)
                           2(r)    
    """
    assert(len(rb_tree) == 7)
    assert(rb_tree.root.r.r.col == BLACK)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 7])    
    assert(rb_tree.preorder_traverse() == [2, 1, 1, 4, 3, 2, 7])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 3, 7, 4, 2])

    rb_tree.insert(6)
    """
                    2(b)
        1(b)                     4(r)
             1(r)            3(b)     7(b)
                           2(r)      6(r)    
    """
    assert(len(rb_tree) == 8)
    assert(rb_tree.root.r.r.l.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 6, 7])    
    assert(rb_tree.preorder_traverse() == [2, 1, 1, 4, 3, 2, 7, 6])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 3, 6, 7, 4, 2])    

    rb_tree.insert(5)
    """
                    4(b)
        2(b)                     6(b)
    1(b)      3(b)           5(b)     7(b)
      1(r)   2(r)    
    """
    assert(len(rb_tree) == 9)
    assert(rb_tree.root.r.l.col == BLACK)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 5, 6, 7])    
    assert(rb_tree.preorder_traverse() == [4, 2, 1, 1, 3, 2, 6, 5, 7])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 3, 2, 5, 7, 6, 4])

    rb_tree.insert(5)
    """
                    4(b)
        2(b)                     6(b)
    1(b)      3(b)           5(b)     7(b)
      1(r)   2(r)              5(r)    
    """
    assert(len(rb_tree) == 10)
    assert(rb_tree.root.r.l.r.col == RED)
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 5, 5, 6, 7])    
    assert(rb_tree.preorder_traverse() == [4, 2, 1, 1, 3, 2, 6, 5, 5, 7])
    assert(rb_tree.postorder_traverse() == [1, 1, 2, 3, 2, 5, 5, 7, 6, 4])

    rb_tree.insert(8)
    """
                    4(b)
        2(b)                     6(b)
    1(b)      3(b)           5(b)     7(b)
      1(r)   2(r)              5(r)     8(r)    
    """
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8])

    rb_tree.insert(9)
    """
                    4(b)
        2(b)                     6(b)
    1(b)      3(b)           5(b)     8(r)
      1(r)   2(r)              5(r)  7(b)9(b)      
    """
    assert(rb_tree.inorder_traverse() == [1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9])

    rb_tree.insert(0)
    """
                     4(b)
         2(b)                     6(b)
     1(b)      3(b)           5(b)     8(r)
    0(r)1(r)  2(r)              5(r)  7(b)9(b)       
    """
    assert(rb_tree.inorder_traverse() == [0, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9])


    # check the find(), min_node(), max_node(), successor(), predecessor() method
    assert(rb_tree.find(6).val == 6)
    assert(rb_tree.find(1000) == -1)
    assert(rb_tree.min_node().val == 0)
    assert(rb_tree.min_node(rb_tree.find(6)).val == 5)
    assert(rb_tree.max_node(rb_tree.find(2)).val == 3)
    assert(rb_tree.successor(rb_tree.find(2)).val == 2)
    assert(rb_tree.predecessor(rb_tree.find(6)).val == 5)
    

    # check the delete() method
    rb_tree.delete(rb_tree.find(6))
    """
    ただの削除だと
                     4(b)
         2(b)                     7(b)
     1(b)      3(b)           5(b)     8(r)
    0(r)1(r)  2(r)              5(r)   y 9(b)
    となる。これを rb_delete_fix すると (case 1-4)
                     4(b)
         2(b)                     7(b)
     1(b)      3(b)           5(b)     8(b)
    0(r)1(r)  2(r)              5(r)     9(r)
    となるはず。        
    """
    assert(len(rb_tree) == 12)
    assert(rb_tree.root.r.r.col == BLACK)
    assert(rb_tree.root.r.r.r.col == RED)
    assert(rb_tree.preorder_traverse() == [4, 2, 1, 0, 1, 3, 2, 7, 5, 5, 8, 9])

    rb_tree.delete(rb_tree.find(4.0))
    """
    ただの削除だと
                     5(b)
         2(b)                     7(b)
     1(b)      3(b)            y5(r)   8(b)
    0(r)1(r)  2(r)                       9(r)
    となるはず。これを rb_delete_fix すると (case 1-3)
                     5(b)
         2(b)                     8(b)
     1(b)      3(b)            7(b)   9(b)
    0(r)1(r)  2(r)            5(r)          
    となるはず。          
    """
    assert(len(rb_tree) == 11)
    assert(rb_tree.root.r.r.col == BLACK)
    assert(rb_tree.preorder_traverse() == [5, 2, 1, 0, 1, 3, 2, 8, 7, 5, 9])
    
    rb_tree.delete(rb_tree.find(0))
    """
    ただの削除でおしまい
                     5(b)
         2(b)                     8(b)
     1(b)      3(b)            7(b)   9(b)
       1(r)  2(r)            5(r)         
    となるはず。    
    """
    assert(len(rb_tree) == 10)
    assert(rb_tree.preorder_traverse() == [5, 2, 1, 1, 3, 2, 8, 7, 5, 9]) 

    rb_tree.delete(rb_tree.find(1.0))
    """
    ただの削除だと
                     5(b)
         2(b)                     8(b)
     y1(r)    3(b)            7(b)   9(b)
             2(r)            5(r)      
    となるはず。これを rb_delete_fix すると (case 1-2)
                     5(b)
         2(b)                     8(b)
      2(b)    3(b)            7(b)   9(b)
     1(r)                    5(r)       
    となるはず。    
    """
    assert(len(rb_tree) == 9)
    assert(rb_tree.root.l.col == BLACK)
    assert(rb_tree.root.l.l.col == BLACK)
    assert(rb_tree.preorder_traverse() == [5, 2, 2, 1, 3, 8, 7, 5, 9])

    rb_tree.delete(rb_tree.find(2))
    """
    ただの削除だと
                     5(b)
         3(b)                    8(b)
      2(b)    y               7(b)   9(b)
     1(r)                    5(r)            
    となるはず。これを rb_delete_fix すると (case 2-3)
                     5(b)
         2(b)                    8(b)
      1(b)   3(b)             7(b)   9(b)
                            5(r)            
    """
    assert(len(rb_tree) == 8)
    assert(rb_tree.root.l.l.col == BLACK)
    assert(rb_tree.preorder_traverse() == [5, 2, 1, 3, 8, 7, 5, 9])

    rb_tree.delete(rb_tree.find(7))
    """
    ただの削除だと
                     5(b)
         2(b)                    8(b)
      1(b)   3(b)            y5(r)   9(b)
    となるはず。これを rb_delete_fix すると (case 1-4)
                     5(b)
         2(b)                   y8(b)
      1(b)   3(b)            5(r)   9(r)
    再帰し、これを rb_delete_fix すると (case 2-4)
                     5(b)
         2(r)                    8(b)
      1(b)   3(b)            5(r)   9(r)    
    となるはず。
    """
    assert(len(rb_tree) == 7)
    assert(rb_tree.root.l.col == RED)
    assert(rb_tree.preorder_traverse() == [5, 2, 1, 3, 8, 5, 9])



def tree_dfs(tree, node):
    """ balance チェック用の補助関数。tree の node を根とした時の最大深さを返す"""
    l_size, r_size = 0, 0
    if node.l != tree.nil:
        l_size = tree_dfs(tree, node.l)
    if node.r != tree.nil:
        r_size = tree_dfs(tree, node.r)
    return max(l_size, r_size) + 1    # 左部分木、右部分木の深さの最大値に自身の深さの分を足す



def test_red_black_tree_insert_balance():
    """
    10**2 <= N <= 10**3 回ランダムな値を挿入し赤黒木を構築することを Iteration 回行う。
    それぞれについて最大深さを調べ、<= 2 * lgN であることを確認する
    """
    Iteration = 5
    for _ in range(Iteration):
        N = randint(10**2, 10**3)
        rb = RedBlcakTree()
        for _ in range(N):
            rb.insert(randint(-50, 50))
        max_depth = tree_dfs(rb, rb.root)
        assert max_depth <= 2 * ceil(log2(N))



def test_red_black_tree_insert_delete_balance():
    """
    10**2 <= N <= 10**3 回ランダムな値を挿入、削除し赤黒木を構築することを Iteration 回行う。
    それぞれについて最大深さを調べ、<= 2 * lg(SIZE) であることを確認する
    """
    Iteration = 5
    for _ in range(Iteration):
        N = randint(10**2, 10**3)
        rb = RedBlcakTree()
        counter = defaultdict(int)
        size = 0
        for _ in range(N):
            num = randint(-50, 50)
            rb.insert(num)
            size += 1
            counter[num] += 1
            # 5 回に 1 回削除を行う
            if randint(0, 4) == 0:
                num, cnt = counter.popitem()
                assert cnt > 0
                node = rb.find(num)
                assert node != -1
                rb.delete(node)
                cnt -= 1
                if cnt > 0:
                    counter[num] = cnt    # 1 減らして再登録
                size -= 1
        max_depth = tree_dfs(rb, rb.root)
        assert max_depth <= 2 * ceil(log2(size))






if __name__ == "__main__":
    pytest.main(['-v', __file__])

