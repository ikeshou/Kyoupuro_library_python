"""
トライ木

各頂点に文字が対応した根付き木で、根からの道上の頂点の文字たちで単語を表す
子のノードを
1. ハッシュテーブルで管理 
2. 左子右兄弟表現で各兄弟をソートした状態で管理
という二つの方法の実装がある。このファイルでは 1 を実装する。

(左子右兄弟表現かつ各兄弟をソートした状態で実現すると...)
登録単語数によらず以下のクエリに対し高速で答えることができる。
- 文字列の検索: 単語長 m として O(|使用文字種類|) * O(m)
- 文字列の挿入: 単語長 m として O(|使用文字種類|) * O(m)
- 前方一致検索: 接頭語長 m として O(|使用文字種類|) * O(m)
- 各ノードが以下に含む単語数を保持するようにすることで、辞書順最小、辞書順最大、辞書順 k 番目といったクエリに対し O(答えの単語長) で答えることが可能
- 「左の兄弟のノード」といった移動が容易になるので「辞書順で一つ前」「辞書順で一つ後ろ」と言ったクエリに対し O(答えの単語長) で答えることが可能
といった特徴がある。
最大の単語の長さの分の深さをもつ木となるため、少数の長い単語を管理するのには向かない。


(左子右兄弟表現ではなくハッシュテーブルで子供へのポインタを管理したり、キーは a-z であると決め打ちして 26 個の要素を持つリストで子供へのポインタを管理したりすると...)
検索時の O(|使用文字種類|) のペナルティはなくなるが... 後半 2 つの辞書順系のクエリにはむかなくなる (多分)
"""

# このクラスをユーザーが直接触ることはない

class TrieHashNode:
    def __init__(self, data='', parent=None, terminal=False, word_count=0):
        self.data = data    # root からこのノードまでを辿ってできる文字列
        self.parent = parent    # 親ノードへの参照
        self.children = dict()    # 次の文字をキーとして子ノード参照を記録している
        self.terminal = terminal    # この文字で終了する単語が存在するか
        self.word_count = word_count    # このノード以下の単語数
    
    def traverse(self):
        'このノード以下の全単語を巡回しリストにまとめて返す'
        ans = [self.data] if self.terminal else []    # root の時、単語の終わりでない時は [] となって欲しい
        for child_node in self.children.values():
            ans += child_node.traverse()
        return ans
    
    def search_child_char(self, char):
        'このノードの子供に char に対応するノードが存在するならそのノードを、存在しないなら None を返す'
        if char in self.children:
            return self.children[char]
        else:
            return None
    
    def set_child_char(self, char, is_terminal):
        'このノードの子供に char と対応するノードを作成しそのノードを返す'
        child_node = TrieHashNode(data=self.data+char, parent=self, terminal=is_terminal, word_count=1)
        self.children[char] = child_node
        return child_node
    
    def delete_self(self):
        'このノードを削除し親のノードを返す'
        char = self.data[-1]
        parent = self.parent
        del parent.children[char]
        return parent
    
    def incf_upcurrent_word_count(self):
        'このノードから root までの道 [self, root] 上の全てのノードの word_count を 1 増やす'
        current = self
        while current is not None:
            current.word_count += 1
            current = current.parent
    
    def decf_upcurrent_word_count(self):
        'このノードから root までの道 [self, root] 上の全てのノードの word_count を 1 減らす'
        current = self
        while current is not None:
            current.word_count -= 1
            current = current.parent



# メインのインターフェース

class TrieHashTree:
    def __init__(self):
        self.root = TrieHashNode()    # 色々書き込まれることはあるがその値に意味はない

    def traverse(self):
        """
        トライ木の全単語を巡回しリストにまとめて返す (O(全ノード数))
        Returns:
            list
        """
        return self.root.traverse()
    
    def _common_prefix_node(self, prefix):
        """
        (search_word(), search_prefix(), count_all_word_with_prefix(), find_all_word_with_prefix() で使用する内部関数)
        トライ木上で prefix と対応した道を探索し、終点のノードを返す。対応した道が存在しない場合 None を返す (O(単語長)) 。
        Args:
            prefix (str)
        Returns:
            Union(TrieHashNode, None)
        Raises:
            ValueError: prefix が '' の時
        """
        if prefix == '':
            raise ValueError('TrieHashTree._common_prefix_node(): prefix should not be an empty string.')
        current = self.root
        for char in prefix:
            child_node = current.search_child_char(char)
            if child_node is None:
                return None
            else:
                current = child_node
        return current

    def search_word(self, word):
        """
        トライ木に指定した単語が存在するか判定する (O(単語長))
        Args:
            word (str)
        Returns:
            bool
        """
        last = self._common_prefix_node(word)
        if last is None:
            return False
        return last.terminal    # 仮に word の char と対応するノードがあってもそこで単語がきれない場合は False (その単語を接頭語とする単語で登録されていた場合など)

    def search_prefix(self, prefix):
        """
        トライ木に指定した接頭語を持つ単語が存在するか判定する (O(接頭語長))
        Args:
            word (str)
        Returns:
            bool
        """
        return self._common_prefix_node(prefix) is not None
    
    def count_all_word_with_prefix(self, prefix):
        """
        指定した接頭語を持つ単語の個数を返す。(存在しない場合は 0) (O(接頭語長))
        Args:
            word (str)
        Returns:
            int
        """
        last = self._common_prefix_node(prefix)
        return last.word_count if last is not None else 0   

    def find_all_word_with_prefix(self, prefix):
        """
        指定した接頭語を持つ単語のリストを返す。(存在しない場合は []) (O(接頭語長))
        Args:
            word (str)
        Returns:
            list        
        """
        last = self._common_prefix_node(prefix)
        return last.traverse() if last is not None else []


    def insert_word(self, word):
        """
        指定した単語をトライ木に挿入する。(O(単語長))
        Args:
            word (str)
        """
        current = self.root
        res = ''
        for ind, char in enumerate(word):
            child_node = current.search_child_char(char)
            if child_node is None:
                res = word[ind:]
                break
            else:
                current = child_node
        # すでに対応するブランチは出来上がっていた場合
        if res == '':
            # 対応する単語が登録されていなかった場合のみ処理を行う
            if not current.terminal:
                current.terminal = True
                current.incf_upcurrent_word_count()
        # 今のノードから res に対応するブランチを作成する必要がある場合
        else:
            current.incf_upcurrent_word_count()
            for ind, char in enumerate(res):
                if ind != len(res)-1:
                    current = current.set_child_char(char, is_terminal=False)
                else:
                    current = current.set_child_char(char, is_terminal=True)


    def delete_word(self, word):
        """
        指定した単語をトライ木から削除する。(O(単語長))
        Args:
            word (str)
        Raises:
            ValueError: 指定した単語がそもそも登録されていない時
        """
        if not self.search_word(word):
            raise ValueError(f"TrieHashTree.delete_word(): {word} not in TrieHashTree")
        last = self._common_prefix_node(word)
        # ノードを削除する必要がない場合
        if last.children:
            assert(last.terminal == True)
            last.terminal = False
            last.decf_upcurrent_word_count()
        # 一本鎖のうちは削除を続ける
        else:
            last = last.delete_self()
            while last != self.root and len(last.children) == 0:
                last = last.delete_self()
            last.decf_upcurrent_word_count()
        
