"""
Manacher のアルゴリズム
ある文字列の部分文字列（部分列ではない！）で最長の回文となるものを O(|s|) で求めることができる
"""


def calc_longest_palindrome_substring(s, dummy='$'):
    """
    Manacher のアルゴリズム
    ある文字列の部分文字列（部分列ではない！）で最長の回文となるものを O(|s|) で求めることができる

    dummy 文字を s の各文字に対して挟んだ文字列 inserted_s とする。
    「inserted_s[i] を中心とする (s[i] ではない)」極大回文半径を dp[i] とする ((回文の長さ + 1) // 2)
    
        - 定式化
        - dp を左から埋めていくことを考える。
        - dp[0]...dp[i-1] までがわかっている時、dp[i] を考えたい
        - 愚直に inserted_s[i] を中心に左右を見比べることにより dp[i] は計算可能。dp[i] = r とする。
        - 1 <= d <= r - 1 なる d について、X との距離が d である文字について考える (左側の文字は inserted_s[i-d] (Y), 右端の文字は inserted_s[i+d] (Y))

                    a.....................X.....................b
                     ==========r=========== 
                                          ==========r===========
                             Y............X............Y
                              ======d======
                                          =======d=====
            1.          p....Y....q               q....Y....p          
                         =rl==                         ==rr=
            2.      a........Y........c       a........Y........c
                     ===rl====                         ====rr===
                    a........Y........b      .b........Y........b.
                     ===rl====                         ====rr=====
            3.    ..a........Y........a..     a........Y........b
                  =====rl=====                         ====rr===
            
            dp[i-d] = rl, dp[i+d] = rr とする。
            1. r - d > rl の時、図より rr = rl と定まる。
            2. r - d = rl かつ inserted_s[i-r] = inserted_s[i-d+rl-1] の時、図より rr = rl と定まる。
            2. r - d = rl かつ inserted_s[i-r] ≠ inserted_s[i-d+rl-1] の時、図より rr >= rl 。次の探索箇所である。
            3. r - d < rl の時、図より rr = r - d と定まる。

    Args:
        s (str)
        dummpy (str): s に出現しないダミー文字
    Returns:
        dp (list)
    """
    if s:
        inserted_s = ''.join(sum([[s[i], dummy] for i in range(len(s) - 1)], []) + [s[-1]])    # 'hoge' -> 'h$o$g$e'
    else:
        inserted_s = ''
    n = len(inserted_s)
    dp = [0] * n

    i, r = 0, 0
    # i: 回転中心を inserted_s[i] とする。
    while i < n:
        while 0 <= i - r and i + r < n and inserted_s[i - r] == inserted_s[i + r]:
            r += 1
        dp[i] = r
        d = 1
        # d: 注目する文字 Y の i との距離
        while 0 <= i - d and r - d > dp[i - d]:
            # 1 パターン
            dp[i + d] = dp[i - d]
            d += 1
        # 2, 3 パターン。半径は r - d 以上であることが確定している
        i += d
        r -= d
    
    return dp


def is_palindrome(l, r, dp):
    """
    dummy 文字列を挿入した inserted_s に対し計算した極大回文半径を記した dp テーブルをもとに
    「もとの文字列 s の部分文字列 s[l:r] が」回文となっているかを O(1) で返す
    """
    begin = 2 * l
    end = 2 * (r - 1)
    center_ind = (begin + end) // 2
    # center_ind 中心の最大回文文字列長  inserted_s での部分文字列数
    return dp[center_ind] * 2 - 1 >= (end - begin + 1)


def reconstruct_longest_palindrome(s, dp):
    """
    dummy 文字列を挿入した inserted_s に対し計算した極大回文半径を記した dp テーブルをもとに
    O(n) で最長の回文部分文字列を求めてリストで返す
    """
    # 偶数 i について dp[i] = r のとき、もとの文字列での回文長は 1 + ((r-1)//2)  * 2 = (r-1 if r%2==0 else r)
    # 奇数 i について dp[i] = r のとき、もとの文字列での回文長は (r//2) * 2 = (r if r%2==0 else r-1)
    n = len(dp)
    max_length = -1
    indices = []
    for i in range(n):
        r = dp[i]
        if i % 2 == 0:
            size = r - 1 if r % 2 == 0 else r
        else:
            size = r if r % 2 == 0 else r - 1
        if max_length < size:
            indices, max_length = [i], size
        elif max_length == size:
            indices.append(i)
    ans = []
    for ind in indices:
        if ind % 2 == 0:
            center_ind = ind // 2
            ans.append(s[center_ind - (max_length-1)//2 : center_ind + (max_length-1)//2 + 1])
        else:
            slice_center = (ind + 1) // 2
            ans.append(s[slice_center - max_length//2 : slice_center + max_length//2])
    return ans
        


if __name__ == "__main__":
    manacher = calc_longest_palindrome_substring("abba")
    assert(manacher == [1, 1, 2, 4, 2, 1, 1])
    assert(is_palindrome(0, 4, manacher) == True)
    assert(is_palindrome(0, 3, manacher) == False)
    assert(is_palindrome(1, 3, manacher) == True)
    assert(reconstruct_longest_palindrome("abba", manacher) == ["abba"])

    manacher2 = calc_longest_palindrome_substring("levelcivicwowc")
    assert(reconstruct_longest_palindrome("levelcivicwowc", manacher2) == ["level", "civic", "cwowc"])

    # empty
    manacher3 = calc_longest_palindrome_substring("")
    assert(manacher3 == [])
    assert(reconstruct_longest_palindrome("", manacher3) == [])

    # character
    manacher4 = calc_longest_palindrome_substring("S")
    assert(manacher4 == [1])
    assert(reconstruct_longest_palindrome("S", manacher4) == ["S"])    

    print(" * assertion test ok * ")