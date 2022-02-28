# HEMSQ
HEMS (Home Energy Management System) は家庭のエネルギー使用を効率よくするために
管理するシステムで、主に以下の3つの要素で構成されています。

1. 家庭で発生する需要・天気などの予測
2. エネルギー使用・売電などのスケジューリング
3. 制御

`hemsq` はこの**2番目のスケジューリング**を**アニーリングマシン**という組合せ最適化問題を得意とするマシンを用いて行います。

## 必要条件
- python >= 3.7
- numpy >= 1.6
- amplify >= 0.6.5
- matplotlib >= 3.0
- pandas >= 1.1

## インストール

```
pip install git+https://github.com/HemsQ/hemsq.git
```

## 簡単な使い方
### 初期化

```python
from hemsq import HemsQ
hq = HemsQ()
```

### Amplify クライアント設定

[無料ユーザー登録](https://amplify.fixstars.com/ja/register)をして、アクセストークンを取得してください。

```python
from amplify.client import FixstarsClient

client = FixstarsClient()
client.token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # アクセストークン
client.parameters.timeout = 1000 # タイムアウト1秒
client.parameters.outputs.num_outputs = 0
client.parameters.outputs.duplicate = True # エネルギー値が同一の解を重複して出力する
hq.set_client(client)
```
### デフォルト値で最適化

```python
# 最適化
result = hq.solve()

# 結果が正しく出力されたら可視化
if result:
    hq.show_all()
```

## 構成

|クラス名|パッケージ名|概要|
|---|---|---|
|HemsQ|hemsq.py|天気や需要パターン、その他あらゆるパラメータが表す個々の状況に合わせてHEMSシステムの最適化を行い、結果を可視化する。|

### HemsQ クラス

**・メソッド一覧**
|メソッド名|機能|
|---|---|
|set_params|天気や需要など状況を表すパラメータを細かく設定する。|
|params|プロパティ。現在設定されているパラメータを返す。|
|reset_params|パラメータをデフォルト値に戻す。|
|set_client|`Amplify` クライアントを設定する。|
|show_all|show_cost, show_all_schedule, show_demand, show_solar, show_cost_and_charge, show_cost_and_useを全て実行する。|
|show_cost|得られたスケジュールによってかかるコスト(または売上)、CO2排出量を表示する。|
|show_all_schedule|スケジュール表を表示する。|
|show_demand|需要と供給のグラフを表示する。|
|show_solar|太陽光発電関係のグラフを表示する。|
|show_cost_and_charge|商用電源の価格と購入の推移を表すグラフを表示する。|
|show_cost_and_use|商用電源の価格と使用の推移を表すグラフを表示する。|
