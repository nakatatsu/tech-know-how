---
Title: AWS Lambdaの開発・運用手順に関する課題のメモ書き
Category:
- AWS
- Lambda
- Python
Date: 2022-10-13T14:24:31+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-development-operation
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889927075895
---

[:contents]


# GitHub Flow / Git Flow

- 日常的にゴリゴリ更新していけるプロジェクトであればGitHub Flow、モバイルアプリのバックエンドのように特定期日までにまとまった機能をリリースしないといけないならGit Flow。
- どちらであっても本番環境はCI/CD前提。
  - つまりソースコードは必ずGitを通す。Pythonを用いたLambda関数はブラウザ上で編集できるわけだが、運用としてもソース管理が甘くなるしレビューも怪しくなるし事前のテストもしづらいしで、本番環境で推奨したい運用ではない。
  - 実際の業務を考えるための実験という意味合いもあるので、そこは真面目に。

# LambdaのImmutableデプロイは可能か？

そもそもLambdaはデプロイの都度バージョンが新しくなるイミュータブルデプロイ式。そのため切り替え方式さえ用意すればいいわけだが、どう切り替えるか。

シンプルにエイリアス機能で切り替えられるなら良いのだが？

# SAMどうよ

Terraformを使うなら無理にSAMを使う必要はないんじゃないかなあ、という気がする。住み分けが結構難しい。

# TerraformとAPI GatewayとSwaggerの兼ね合いどうしよう

なんと[一つに組み合わせられられるらしい](https://qiita.com/neruneruo/items/94a0e637ea1c6c95d9e4)。

SwaggerでAPIエンドポイントの設計を書いてTerraformに食わせ、API Gatewayを構築することができるならそれに越したことはない。

# 参考

- https://tech.hicustomer.jp/posts/blue-green-deployment-in-serverless/
- https://blog.nijohando.jp/post/2020/partially-managing-lambda-with-terraform/
- https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-aliases.html
