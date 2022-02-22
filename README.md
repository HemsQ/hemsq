# HEMSQ
HEMS (Home Energy Management System) は家庭のエネルギー使用を効率よくするために
管理するシステムで、主に以下の3つの要素で構成されています。

1. 家庭で発生する需要・天気などの予測
2. エネルギー使用・売電などのスケジューリング
3. 制御

`hemsq` はこの2番目のスケジューリングを**アニーリングマシン**という
組合せ最適化問題を得意とするマシンを用いて行います。

## 必要条件
- python >= 3.7
- numpy >= 1.6
- amplify >= 0.6.5
- matplotlib >= 3.0
- pandas >= 1.1

## インストール

```
pip install git+https://github.com/CanonMukai/hemsq-prototype.git
```

```python
from hemsq import HemsQ
```
