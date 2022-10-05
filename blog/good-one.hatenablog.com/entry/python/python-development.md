---
Title: PythonとVisualStudio Codeで開発環境づくり
Category:
- Python
- VisualStudio Code
- 開発環境
Date: 2022-10-04T18:09:07+09:00
URL: https://blog.tricrow.com/entry/python/python-development
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889924490080
---

Pythonの開発をVisualStudio Codeで行うにあたり、Formatter/Linterも使ってなるべく楽がしたい。コードの標準化を人力で行うのは避けたい。

という動機により、VSCodeと以下を連携させて開発環境を構築した。

- Formatterとして black（設定楽なので）
- blackの補助として isort（blackは対応してなかったので）
- Linterとして flake8（よく普及してるそうなので）

[:contents]

# black

## Install

**プレビュー版ながら**、VSCodeの拡張機能でBlack Formatterを使うことができる。ProductionでPreviewを使うのは許されないが、今回はPersonal Useであり、遠からずGAするであろうという期待の元そちらを利用した。

ワークスペース設定内のsettings内に設定を記載した。（後述）

# isort

## Install

pipでインストール。

    pip install isort

ワークスペース設定内のsettings内に設定を記載した。（後述）

# flake8

## Install

1. pipでインストール。

        pip install flake8
        # 確認
        pip show flake8

2. VSCodeの設定画面に移動し、"pylintEnabled"で検索。pylintEnabledとflake8Enabledにチェックを入れる。
   - という手順を踏んだが、後述の内容をコピペすれば済む。


# VSCodeのワークスペース設定

VSCodeでワークスペースを保存する際にできる***.code-workspaceにあるsettingsの項目を、以下のように記載した。

    {
        "folders": [
            {
                "path": "."
            }
        ],
        "settings": {
            "editor.codeActionsOnSave": {
                "source.organizeImports": true
            },
            "python.linting.enabled": true,
            "python.linting.flake8Enabled": true,
            "python.linting.flake8Args": [
                "--max-line-length",
                "120"
            ],
            "[python]": {
                "editor.defaultFormatter": "ms-python.black-formatter",
                "editor.formatOnSave": true
            },
            "black-formatter.args": [
                "--line-length=120"
            ]
        }
    }

ちゃんと動作していそうである。

ちなみにユーザー設定として保存する方法もあるそうだが、違うPCで作業を行う際に設定が消えてしまうのは困るため、ワークスペースに保存している。

# 参考

- https://qiita.com/fehde/items/723b619013dc86008acc
- https://zenn.dev/wtkn25/articles/python-isort
- https://qiita.com/nujust/items/e0985240fd461e5c4c0a
-
