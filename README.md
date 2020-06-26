[![Build Status](https://travis-ci.org/ikeshou/Kyoupuro_library_python.svg?branch=master)](https://travis-ci.org/ikeshou/Kyoupuro_library_python)
# Kyoupuro_library_python
Python libraries for programming competition

Useful and typical algorithms and data structures that are not covered with Python's built-in libraries are implemented.
All of the libraries passed assertion test and doctest written in itself.
Some of the libraries are verified by AOJ and AtCoder.

<br>

##  はじめに

* 競技プログラミングの Python ライブラリです。
* src/ 以下のライブラリコードは Python3.5 の標準ライブラリのみで動くはずです (多分)。**tests/ 以下のテストコードの実行には Python3.8, pytest, numpy, scipy, networkx が必要です。**
* 使用方法は各関数やクラスに記載された docstring を見ればわかるかと思います。アルゴリズムや実装の簡易的なメモはスクリプト冒頭に書いてあります。
* 大体のライブラリはランダムケースを用いたブラックボックステストをパスしています。(ナイーブに解ける問題サイズにおいて愚直解と比較、サードパーティー製の scipy, networkx などの出力と比較など。)
* 一部のライブラリは AOJ, AtCoder により verify ずみです。
* （最大フローと赤黒木がお気に入り）

<br>

## テストをするには
* doctest を走らせる
```bash
cd src/
# module として試したいファイルを実行。実行で怒られが発生しなかったら成功。以下は一例
python -m mypkg.string.rolling_hash
```
* pytest を走らせる (テストコードでは python 3.8 以上かつ pytest, numpy, scipy, networkx が必要)
```bash
cd tests/
pytest [-v]
```

<br>

---

### 1. algorithms
- ソートに関連するアルゴリズムで有用なもの
  - STL の nth_element(), stable_partition()
  - 範囲指定が可能なクイックソート
  - 範囲指定が可能なマージソート
  - 反転数
  - 線形ソート、基数ソート
- 整数問題に関係するアルゴリズムで有用なもの
  - 素数判定、約数列挙、エラトステネスの篩
  - ユークリッドの互除法
  - modpow
  - 階乗、フィボナッチ数 (ジェネレータ)
  - 階乗テーブル、階乗の逆元テーブル、剰余版組み合わせ計算
- 尺取り法
- 累積和 (imos 法)
  - 一次元、二次元
- スライディング最小値
- 座標圧縮
  - 一次元 (大小関係を保存、空白領域を保存)、二次元 (大小関係を保存、空白領域を保存)
- 半分全列挙


### 2. basic data structures
- 循環型双方向連結リスト
- 優先度付きキュー
  - 最大優先度付きキュー、最小優先度付きキュー
  - 優先度の変更が可能な優先度付きキュー
  - 削除が可能な優先度付きキュー
- 赤黒木


### 3. graphs
- 基本的な DFS, BFS を使用するアルゴリズムで有用なもの
  - DFS による全点探索と全経路探索 (再帰による実装、スタックによる実装)
  - BFS による全点探索と全経路探索
  - 無向グラフに対する橋の検出、関節点の検出、二重連結成分分解
  - 有向グラフに対するトポロジカルソート (DFS による実装、BFS による実装)
  - 有向グラフに対する強連結成分分解
  - 木の直径
  - 二部グラフ判定
  - 木に対するダブリングによる祖先の二分探索
  - 最小共通祖先
- 最短経路問題
  - 単一始点最短距離 (Bellman-Ford 法、Dijkstra 法)
  - 全点対間最短距離 (Warshall-Floyd 法)
- 最小木 (MST) (Prim 法、Kruskal 法)
- フロー
  - 最大フロー (Ford-Fulkerson 法、Edmonds-Karp 法)
  - 二部グラフの最大マッチング


### 4. advanced data structures
- Union-Find Tree
- kD Tree
- 平方分割
  - (普通) RSQ, RMQ, RAQ
  - (遅延伝播) RUQ, RAQ_RSQ
- Fenwick Tree
  - RSQ
- Segment Tree
  - RSQ, RMQ, template for Segment Tree


### 5. string
- Rolling Hash
- Trie Tree


### 6. geometry
- 回転、ノルム、偏角の差、内積、外積
- ベクトルの直交判定、平行判定
- 点の直線に対する射影、反射
- 線分の交差判定、線分の交点、円と直線の共有点、円と円の共有点
- 点と直線の距離、点と線分の距離、線分と線分の距離


### 7. typical dp
- ロッド切り出し問題
- 連鎖行列積
- ナップザック問題
- 最長増加部分列 (LIS)
- 最大部分列
- 最長共通部分列 (LCS)
- 最長共通回文
- 最長共通連続部分列
- 最長共通連続回文 (Manacher のアルゴリズム)
- 編集距離
- 巡回セールスマン問題 (TSP)
- 行列累乗


### 8. others
- 稀によく書く (?) 関数たち (多次元版 flatten とか transpose とか)
