# 概要

本リポジトリのコードは、下記論文で提案されたアルゴリズムを Python で実装したものです。

Stephen Alstrup, Cyril Gavoille, Haim Kaplan and Theis Rauhe, Nearest Common Ancestors: A Survey and a New Distributed Algorithm. In Proc. 14th annual ACM symposium on Parallel algorithms and architectures, pp.258–264, 2002.

# ディレクトリ構成

```
  .
  ├── README.md       # 本ファイル
  ├── sample.py       # サンプルスクリプト
  ├── input.csv       # 入力用のファイル
  ├── lib             # ライブラリ置き場
  │   ├── config.py   # 定数値の設定ファイル
  │   ├── rmq.py      # RmQ ロジックの実装
  │   └── utils.py    # utility
  ├── rmq             # 対話式コマンド
  ├── rmq_naive       # ナイーブアルゴリズム
  └── test            # テストコード置き場
      ├── test.csv    # テスト用入力ファイル
      └── test.py     # テストコード
```
  
# Python のバージョン

3.6 以上を想定

```
$ python -V
Python 3.6.3 :: Anaconda, Inc.
```

# 動作確認方法

```
$ ./rmq
Input filename (if you want to use default file, press ENTER):  <- csvファイル名を入力

Input query positions (input 'q' for quite)
start position: 1             <- 開始位置を入力(添字は 0 始まり)
end position: 6               <- 終了位置を入力(添字は 0 始まり)
1

Input query positions (input 'q' for quite)
start position: q             <- クエリ入力を無限回求めてくるので、q で停止
$ 
```

-v を付与すると詳細情報を表示する

```
$ ./rmq -v
Input filename (if you want to use default file, press ENTER):
Input filename is /path/to/csv/file/input.csv
Input array is A[0..99]
Preprocessing...
Complete!

Input query positions (input 'q' for quite)
start position: 1
end position: 6

A = [3145, 4693, 5116, 6808, 9953, 7674, 4905, 5879, 3392, 5364, 7049, 735, 4878, 6746, 9180, 4450, 7297, 9184, 6022, 487, 933, 3665, 2947, 7738, 4080, 267, 3643, 6336, 2355, 2991, 8984, 8099, 3707, 7626, 6798, 1119, 2869, 5435, 2690, 5980, 6613, 6879, 4896, 8789, 5713, 9556, 1353, 9088, 6780, 2652, 7830, 8873, 845, 8702, 8701, 6049, 464, 6438, 141, 3385, 2935, 4510, 8735, 1666, 225, 7590, 4347, 2062, 4409, 4242, 9942, 1836, 406, 1989, 3506, 2491, 1311, 3916, 1428, 9367, 2431, 6151, 1127, 9241, 9081, 9538, 4535, 1629, 6359, 2314, 7675, 6055, 243, 138, 5917, 6026, 4826, 1192, 8027, 6119]

RmQ(1, 6) = 1

A[1..6] = [4693, 5116, 6808, 9953, 7674, 4905]

Input query positions (input 'q' for quite)
start position: q
$ 
```
