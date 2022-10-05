---
Title: はてなブログにカスタムURL付きで新規投稿する
Category:
- ドキュメント作成
- Python
Date: 2022-10-03T19:51:40+09:00
URL: https://blog.tricrow.com/entry/general/git-hatena2
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889924238925
---

[先だっての記事](https://blog.tricrow.com/entry/general/git-hatena)ではてなブログからの記事リスト取得と記事編集ができるようになった。

ところが記事の編集のたびにファイル名が変わってしまう（おそらくＵＲＬも変わっている）謎の現象が起きた。

また、ディレクトリ構成が日付ごとの上にmark-downのファイル名が[数字].mdとなって管理しづらくもあった。いったんドラフトを入れてから編集というフローも煩雑であった。

これらの問題がカスタムURLを指定することで解消できそうであったため、指定する方式に改めることにした。

[:contents]

# やりたいこと

- 独自のディレクトリ構成とファイル名を使いたい
    - こうすると編集のたびにURLが変わる問題も解消されるはず
- ドラフトを通さずに投稿したい

# どう実現するか？

カスタムURLを指定しつつ投稿できるようにする。カスタムURLの指定は[公式ドキュメント](https://developer.hatena.ne.jp/ja/documents/blog/apis/atom/)に記載が**ない**のだが、[こちらのブログ](https://blog.masahiko.info/entry/2018/08/01/191005)の通り、投稿の際のXMLに混ぜこむことで指定できる。

投稿用のスクリプトを改修し、Markdownに記載しているフロントマターからカスタムURLを生成すれば、やりたいことは実行できそうである。


# スクリプトの作成

以下のようになった（リンク先参照）。

## pythonスクリプト

[GitHubのコード](https://github.com/nakatatsu/tech-know-how/blob/main/blog/good-one.hatenablog.com/post.py)


## テンプレート

[GitHubのコード](https://github.com/nakatatsu/tech-know-how/blob/main/blog/good-one.hatenablog.com/post.j2)


# 結果

おおむね問題なさそうである。パスの指定がやや面倒くさいという問題があるが、許容範囲内だろう。
