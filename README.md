# Kyoupuro_library_python
Python libraries for programming competition

Useful and typical algorithms and data structures that are not covered with Python's built-in libraries are implemented.


## 1. algorithms
- ソートに関連するアルゴリズムで有用なもの
  - STL の nth_element(), stable_partition()
  - i 番目の順序統計量
  - 線形ソート (非破壊、破壊)、基数ソート
- 整数問題に関係するアルゴリズムで有用なもの
  - 素数判定、エラトステネスの篩
  - ユークリッドの互除法
  - 階乗、フィボナッチ数 (ジェネレータ)
  - 剰余計算を行う組み合わせ
- 尺取り法
- 累積和 (imos 法)
  - 一次元、二次元
- スライディングウィンドウ
- 平方分割
  - RSQ, RMQ, RAQ, RUQ, RAQ_RSQ
- 座標圧縮
  - 一次元 (大小関係を保存、空白領域を保存)、二次元 (大小関係を保存、空白領域を保存)
- 半分全列挙

## 2. basic_data_structures_complement
- 循環型双方向連結リスト
  - 番兵を使うバージョン、使わないバージョン
- 優先度付きキュー
  - 最大優先度付きキュー、最小優先度付きキュー
- 赤黒木

## 3. graphs
- 基本的な DFS, BFS を使用するアルゴリズムで有用なもの
  - DFS (再帰による実装、スタックによる実装) (全点探索と全経路探索)
  - BFS (キューによる実装) (全点探索と全経路探索)
  - 無向グラフに対する橋の検出、関節点の検出、二重連結成分分解
  - 有向グラフに対するトポロジカルソート (DFS による実装、BFS による実装)
  - 有向グラフに対する強連結成分分解
  - 木の直径
  - 二部グラフ判定
  - 木に対するダブリングによる祖先の二分探索
  - 最小共通祖先
- 最短経路問題
  - 点間最短距離 (Bellman-Ford 法、Dijkstra 法)
  - 全点対間最短距離 (Warshall-Floyd 法)
- 最小木 (MST)
  - Prim 法、Kruskal 法
- フロー
  - 最大フロー (Ford-Fulkerson 法、Edmonds-Karp 法)
  - 二部グラフの最大マッチング

## 4. advanced_data_structures
- Union-Find Tree
- kD Tree
- Segment Tree
  - RMQ, RSQ, template for Segment Tree
  - Fenwick Tree

## 5. string
- Rolling Hash
- Trie Tree
