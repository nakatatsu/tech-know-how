---
Title: Pythonで作るスクリプトのバリデーションについて
Category:
- Python
- Validation
Date: 2022-10-07T18:21:39+09:00
URL: https://blog.tricrow.com/entry/python/python-validation
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889925347777
---

[:contents]


# どこで値のチェックを行うか？

値のチェックにあたり、バリデーションをユーザー入力受付時に行うだけでなく、Entityの値入力時に行うと堅牢である。[公式の例](https://pydantic-docs.helpmanual.io/usage/validators/)ではEntityでバリデーションを行っているように見える。

が、これを両方行うとDRYにしづらく、結局は異なる記述方式で両方で値やルールを合わせながら行わねばならなくなることしばしばで、なかなか大変である。コードのボリュームも増える。

ControllerとEntityをきっちり分離して別々に管理する大規模プロジェクトなら、両方でやったほうがいいと思う。EntityがControllerの値チェックがないと問題を起こすのは困るからだ。だが小さなスクリプトでそこまでやるのは冗長すぎるように思える。

そこでおおまかながら次のように整理したい。

| プロジェクトの規模 | 実行するチェック |
|---|---|
|大| 入力時のバリデーション、Entity作成時の値検証 |
|小| 入力時のバリデーション |

# バリデーション用のライブラリは何を使う？

[Cerberus](https://docs.python-cerberus.org/en/stable/customize.html)を採用した。シンプルで使いやすく、拡張性もあり優秀。
