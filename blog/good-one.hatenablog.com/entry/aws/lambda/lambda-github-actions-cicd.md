---
Title: GitHub Actionsで自動テストし、AWS Lambdaに自動デプロイする。
Category:
- AWS
- GitHub Actions
- Lambda
- Python
Date: 2022-10-13T15:38:48+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-production-deploy
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889927092471
---

AWS Lambda関数の本番デプロイについて検討したCI/CDをGitHub Actionsで実現する。

[:contents]


# 実現したいフロー

1. masterにプルリクがマージされると起動する。
2. 指定のディレクトリの更新でのみ起動する。
3. AWSのリソースアクセス権限を取得する（できればOpenIdConnectを用いて）。
   - 参考: https://dev.classmethod.jp/articles/github-actions-oidc-configure-aws-credentials/
4. 自動テストを走らせ、もしErrorが出たら終了。
   - 自動で行うべきテストは、1)ユニットテスト 2)Flake8によるlintの２つ。
5. アップロードすべきファイルをZipで圧縮し、S3にPUTする。
6. Lambda関数にアップロードする。
7. アップロードしたLambda関数のバージョンを用いて、Lambdaのエイリアスを更新する。
8. 結果を通知する。

ex. 失敗した場合、失敗を通知する。

## 通知は何で行う？

業務用想定ということで、Slackへ通知する。

メールにも行えるらしいが、メールに投げ出すと受信するのが嫌になるほどメッセージが飛ぶので、避けられるなら避けたほうがいいんじゃないかと。

## 関数のアップロードにTerraformは使わない？

使わない。違うリポジトリを別々に同期させないといけないのは誤作動が恐ろしい。しかもTerraformは副作用的なリソース変更を実行してしまうリスクもある。そのためアプリケーションのデプロイには関係させない方向。

# GitHub Actions

## 事前準備： Slack

Slackにメッセージを飛ばすため、SlackのWEBHOOK URLを取得しておく。


## 



# 参考

- 『GitHub Actions 実践 入門』宮田 淳平
- https://github.com/github-actions-up-and-running/fizz-buzz/blob/master/.github/workflows/ci.yml
