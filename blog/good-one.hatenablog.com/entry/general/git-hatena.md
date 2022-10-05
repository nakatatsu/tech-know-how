---
Title: git管理したテキストファイルとはてなブログを連携させる
Category:
- ドキュメント作成
Date: 2022-10-03T16:08:17+09:00
URL: https://blog.tricrow.com/entry/general/git-hatena
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889924183841
---

技術系ドキュメントを公開したいが、CMSを自前で運用すると手間がかかる。そこではてなブログを利用することにした。

だが記事は使い慣れたVisualStudio Codeを使い、MarkDown形式のテキストファイルで作成したい。またそれぞれの記事はGitHubでバージョン管理とバックアップを行いたい。そこでblogsyncを使い、ローカルのテキストファイルをはてなブログと連携させることにした。

[:contents]

# blogsync

本家: https://github.com/x-motemen/blogsync

## インストールと設定

1. 公式ドキュメントにある通り、https://github.com/x-motemen/blogsync/releases からWindows用のバイナリを取得
2. 適当な場所に置いてパスを通す
3. `blogsync --version` でバージョンが出ることを確認
4. ~/.config/blogsync/config.yaml をドキュメントにしたがって記載
   - キーとして利用する文字列は、はてなブログの管理画面を開いたときにURL内に表示されるブログURLを使う

```shellscript:~/.config/blogsync/config.yaml
good-one.hatenablog.com:
  username: good-one
  password: XXXXXXXXXXXX
default:
  local_root: C:\MyFile\GitHub\tech-know-how\blog
```

5. `blogsync pull good-one.hatenablog.com`で記事を取得できればOK

## 使い方

### 記事の編集

`blogsync pull good-one.hatenablog.com` してから`blogsync push`。


    blogsync push <path/to/file>

例えばこう。

    blogsync push C:\MyFile\GitHub\tech-know-how\blog\good-one.hatenablog.com\entry\2022\10\03\122710.md

### 新規追加

これは上手く動作しなかった。仕方ないため後述のドラフトを先に作成する方法で問題を回避することに。

## 生じた課題

### 課題: 複数まとめて更新したい

解決策: 自分でbatなりps1なりでスクリプトを書いてコマンドを回す。

batファイルなら例えばこう。

```:C:\MyFile\blogsync\blogupdate.bat
forfiles /S /M *.md /C "cmd /c  blogsync push @PATH"
```

### 課題: 記事新規作成が失敗する

解決策: Windows10だからか、下記のようにでてしまう。

    error CreateFile /dev/stdin: The system cannot find the path specified.

問題を修正できなかったため、pythonスクリプトでいったんドラフトを作成 → pullして編集して更新 で回避する。

ちなみにスクリプトは以下のようになっている。

```python:draftpost.py
import os
import requests
import yaml
from datetime import datetime

DOMAIN = "good-one.hatenablog.com"

with open(os.path.expanduser("~/.config/blogsync/config.yaml"), "r") as yml:
    config = yaml.safe_load(yml)

HATENA_ID = config[DOMAIN]["username"]
API_KEY = config[DOMAIN]["password"]

URL = f"https://blog.hatena.ne.jp/{HATENA_ID}/{DOMAIN}/atom/entry"


updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

xml = f"""<?xml version="1.0" encoding="utf-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app">
    <title>DUMMY TITLE</title><author><name>name</name></author><content type="text/markdown">DUMMY CONTENT</content>
    <updated>{updated}</updated><app:control><app:draft>yes</app:draft></app:control></entry>"""

r = requests.post(URL, auth=(HATENA_ID, API_KEY), data=xml)

print(r)

```


### 課題: 画像を使いたい

解決策: はてなフォトライフに画像をアップロードして直リン。公開可能なフォトストレージサービスならなんでもいいわけだが、どうせはてなブログを使うので。

### 課題: markdownファイルを違う別ディレクトリ構成で管理するには

解決策: スクリプトを頑張って作ればなんとかなると思うが、大変。そこまでするくらいならディレクトリ構成を表現したインデックスページを専用に作るほうが有益なんじゃないか。

という理由により没。

# 運用

## フロー

1. ドラフトとして空記事を追加
2. pullして更新
3. ローカルに入った記事を編集してblogsync push
4. gitにcommitしてpushして終了

記事の削除やタグの付与などははてなブログ上で実行。

## しかし問題発生

上述のフローの運用にはどうにも気になる点が残った。

その説明と修正を[次の記事](https://blog.tricrow.com/entry/general/git-hatena2)で行う予定。

