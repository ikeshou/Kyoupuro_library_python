import pytest
from random import randint
from mypkg.string.trie_tree import TrieHashNode, TrieHashTree



def test_trie_tree_handmade():
    """
    実装メソッドが機能しているか最低限チェックする。
    """
    trie = TrieHashTree()

    # root
    assert(trie.root.data == '')
    assert(trie.root.parent is None)
    assert(trie.root.children == {})
    assert(trie.root.terminal is False)
    assert(trie.root.word_count == 0)
    # method call when empty
    assert(trie.traverse() == [])
    assert(trie._common_prefix_node('hoge') == None)
    assert(trie.search_prefix('hoge') == False)
    assert(trie.search_word('hoge') == False)
    assert(trie.count_all_word_with_prefix('hoge') == 0)
    assert(trie.find_all_word_with_prefix('hoge') == [])

    trie.insert_word('moo')
    # root
    assert(trie.root.data == '')
    assert(trie.root.parent is None)
    assert(tuple(trie.root.children.keys()) == ('m',))
    assert(trie.root.terminal is False)
    assert(trie.root.word_count == 1)
    # method call
    assert(trie.traverse() == ['moo'])
    assert(trie._common_prefix_node('m').data == 'm')
    assert(trie._common_prefix_node('m').terminal == False)
    assert(trie._common_prefix_node('mo').data == 'mo')
    assert(trie._common_prefix_node('mo').terminal == False)
    assert(trie._common_prefix_node('moo').data == 'moo')
    assert(trie._common_prefix_node('moo').terminal == True)
    assert(trie._common_prefix_node('hoge') == None)
    assert(trie.search_prefix('mo') == True)
    assert(trie.search_word('mo') == False)
    assert(trie.search_prefix('moo') == True)
    assert(trie.search_word('moo') == True)
    assert(trie.count_all_word_with_prefix('m') == 1)
    assert(trie.find_all_word_with_prefix('m') == ['moo'])

    trie.delete_word('moo')
    # root
    assert(trie.root.data == '')
    assert(trie.root.parent is None)
    assert(trie.root.children == {})
    assert(trie.root.terminal is False)
    assert(trie.root.word_count == 0)
    # method call when empty
    assert(trie.traverse() == [])
    assert(trie._common_prefix_node('m') == None)
    assert(trie.search_prefix('m') == False)
    assert(trie.search_word('m') == False)
    assert(trie.count_all_word_with_prefix('m') == 0)
    assert(trie.find_all_word_with_prefix('m') == [])

    trie.insert_word('tail')
    trie.insert_word('talk')
    trie.insert_word('tall')
    trie.insert_word('that')
    trie.insert_word('the')
    trie.insert_word('then')
    trie.insert_word('marverick')
    # root
    assert(trie.root.data == '')
    assert(trie.root.parent is None)
    assert(tuple(trie.root.children) == ('t', 'm'))
    assert(trie.root.terminal is False)
    assert(trie.root.word_count == 7)    
    # method call
    assert(trie.traverse() == ['tail', 'talk', 'tall', 'that', 'the', 'then', 'marverick'])
    assert(trie._common_prefix_node('t').data == 't')
    assert(trie._common_prefix_node('m').data == 'm')
    assert(trie._common_prefix_node('z') is None)
    assert(trie.search_prefix('ta') == True)
    assert(trie.search_word('ta') == False)    
    assert(trie.search_prefix('the') == True)
    assert(trie.search_word('the') == True)
    assert(trie.count_all_word_with_prefix('ta') == 3)
    assert(trie.count_all_word_with_prefix('the') == 2)
    assert(trie.find_all_word_with_prefix('ta') == ['tail', 'talk', 'tall'])
    assert(trie.find_all_word_with_prefix('the') == ['the', 'then'])

    trie.delete_word('the')
    assert(trie.search_prefix('the') == True)
    assert(trie.search_word('the') == False)
    assert(trie.count_all_word_with_prefix('the') == 1)
    assert(trie.find_all_word_with_prefix('the') == ['then'])
    
    assert(trie.traverse() ==  ['tail', 'talk', 'tall', 'that', 'then', 'marverick'])







if __name__ == "__main__":
    pytest.main(['-v', __file__])
