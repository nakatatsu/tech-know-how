---
Title: WindowsでLambda関数開発環境を用意する
Category:
- Windows
- Lambda
Date: 2022-10-07T22:20:27+09:00
URL: https://blog.tricrow.com/entry/windows/development-environment
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889925415671
---

WindowsでLambda関数の開発を行うための開発環境を構築した件について記載する。

構成は以下の通り。

- Windows 10 Home Edition
- Python3.9
- Windows Terminal
- VisualStudio Code
- WSL2 + Ubuntu 22
- Docker Desktop on Windows
- AWS CLI

[:contents]

# Python

[本家](https://www.python.org/downloads/)からDownloadしてインストーラを実行する。パスを通すことだけ忘れなければあとは手なりで進めればOK。

ただし、2022/10現在、今月にはPython3.11がリリースされようかという時期なのであるが、**実に**嘆かわしくもLambda PythonはPython3.9までしか対応していない。そのためコンテナ版ではないLambdaでの利用を前提とするなら**3.9を使わざるを得ない**。

ここは気を付けるべきポイント。

# Windows Terminal, PowerShell

1. Microsoft Store からWindows Terminalを入手する。
2. ついでなのでPowerShellも[公式](https://learn.microsoft.com/en-us/powershell/)から取得して最新化しておく。
3. Windows Terminalを起動し、スタートアップ→既定のプロファイルをPowerShellの最新版に変更
4. 同じくWindows Terminalで使わないプロファイルを非表示にするなり削除するなり。

# VisualStudio Code

[本家](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)からDownloadしてインストーラを実行するだけ。


# WSL2 + Ubuntu 22

1. Powershellを管理者権限で開いて wsl --install を実行
   - [本家ヘルプはこちら](https://learn.microsoft.com/ja-jp/windows/wsl/install)
2. Microsoft Store からUbuntu 22を入手
3. Windows TerminalからUbuntu22を起動
   - id/pass:main/passwordで設定。ローカル限定のため簡略に。言うまでもなくパブリックなネットワークで使っていいパスワードではない。
4. systemctlを使えるようにするため、`sudo /usr/libexec/wsl-systemd` を実行。

# Docker Desktop on Windows

- [本家](https://docs.docker.com/desktop/install/windows-install/)からDocker Desktop on WindowsのインストーラをDownloadして実行。
- Open Docker Dashboard at startupとUse Docker Compose V2にチェックを入れておく。
  - `docker ps`や`docker-compose up`を思いついたときにすぐ実行したいので。

# AWS CLI

- [本家](https://aws.amazon.com/jp/cli/)からダウンロードして実行。


# 参考
- https://qiita.com/shigeokamoto/items/ca2211567771cf40a90d
- https://zenn.dev/tatsurom/articles/aws-sam-or-terraform
- https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/what-is-sam.html
