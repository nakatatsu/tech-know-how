---
Title: Windows+VSCodeでTerraformの開発環境の用意
Category:
- Terraform
- Linter
- Formatter
Date: 2022-10-06T12:41:58+09:00
URL: https://blog.tricrow.com/entry/terraform/terraform-ecosystem
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889924977416
---

Windows+VSCodeでTerraformを使うための開発環境を用意する方法について記載する。

VSCode、Terraformはインストール済という前提。

[:contents]

# Linter(tflint)

## Install

1. https://github.com/terraform-linters/tflint/releases から Windows用のアセットを取得を取得する。(e.g. tflint_windows_amd64.zip)　なおWindows用の最新版が必ずしも間に合うわけではないらしい。ない場合は以前のバージョンにないか探すことになる。
2. 解凍してパスを通すか、パスが通った場所にコピーする。Terraformのバイナリと同じ場所に配置すれば簡単。
3. Powershellで`tflint --version`と打ってバージョンがでればOK

## VSCodeとの連携

なんと、なくなったらしい（！）。当面はTerminalからコマンドで打つしかないか。

# Formatter

## Install

拡張機能の HashiCorp Terraform をVSCodeにインストールするだけ。もともとTerraformは`terraform fmt`でフォーマットできるので、新たにフォーマッタを入れなくていい。

## VSCodeとの連携

セーブ時にフォーマットをかける汎用の設定を入れれば良い。

ワークスペースの設定ファイル（.code-workspace）はこうなる。

    {
      "folders": [
        {
          "path": "."
        }
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
