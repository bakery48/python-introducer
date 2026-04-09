# Python インストールヘルパー

Windows で Python をインストール・セットアップする作業を対話形式で案内するツールです。
会社PCなど管理者権限がない環境にも対応しています。

## 使い方

### Python がまだインストールされていない場合

`start.bat` をダブルクリックして起動してください。
Python が見つからない場合はインストール手順を案内します。

### Python がすでにインストールされている場合

```
python main.py
```

または `start.bat` をダブルクリックしてください。

## 機能

| メニュー | 内容 |
|---------|------|
| 環境診断 | Python / pip / PATH の状態を確認 |
| インストール手順 | 公式サイト・Microsoft Store の2通りを案内 |
| PATH の確認・修正 | PATH が通っていない場合の修正手順・コマンドを生成 |
| pip・仮想環境 | pip のアップグレード、venv の作成・使い方説明 |

## 会社PCへの対応

- インストール時に「Install for current user only」を選ぶことで管理者権限なしでインストール可能
- Microsoft Store 版 Python も案内（最も簡単・管理者権限不要）
- PATH 修正もユーザースコープのみで対応

## ファイル構成

```
python-introducer/
├── start.bat           # 起動スクリプト（Python不要）
├── main.py             # メインメニュー
├── checker.py          # 環境診断
├── installer_guide.py  # インストール手順案内
├── path_helper.py      # PATH 修正補助
├── venv_helper.py      # pip・仮想環境補助
└── ui.py               # UI ユーティリティ
```

## 動作環境

- Windows 10 / 11
- Python 3.8 以上（`main.py` を直接実行する場合）
