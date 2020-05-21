"""
VS code の python snippet (python.json) 作成用スクリプト
json にする上で厄介な 
- double quote -> single quote 変換 (docstring や文字列リテラルなど)
- 見やすくするための各行のインデント
- インデントの深さに対応したタブ文字の挿入
- 各行の冒頭末びの double quote と末尾のカンマの挿入
を一挙にやってくれるぞ

Usage:
スニペットにしたい関数やクラスをコピー -> 実行 -> コピーしたコードの行数を入力 -> コピーした内容を貼り付け -> 変換結果が出力される！
そのまま python.json にコピペしよう
"""


def read_all(line_num):
    # 指定行数分読み込んでリストにまとめて返すぞ
    L = []
    for _ in range(line_num):
        L.append(input())
    return L

def count_head_space(s):
    # 文字列の先頭のスペースの個数を数えるぞ
    cnt = 0
    for char in s:
        if char == ' ':
            cnt += 1
        else:
            break
    return cnt



if __name__ == "__main__":
    line_num = int(input('input the line numbers: '))
    L = read_all(line_num)
    print('')
    print('### now converting... ###')
    print('')
    for i in range(line_num):
        L[i] = L[i].replace("\"", "'")
    for i in range(line_num):
        c = count_head_space(L[i])
        L[i] = ' ' * c + '"' + r'\t' * (c // 4) + L[i][c:] + '"' + (',' if i != line_num - 1 else '')
    for elm in L:
        print(elm)

