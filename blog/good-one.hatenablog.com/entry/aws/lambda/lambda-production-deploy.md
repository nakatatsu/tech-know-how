---
Title: AWS Lambdaの本番デプロイについての検討
Category:
- AWS
- Lambda
- Python
Date: 2022-10-13T15:38:48+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-production-deploy
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889927092471
---

AWS Lambda関数の本番デプロイについて検討する。

[:contents]


# 方向性

- 自動テスト
  - 本番リソースにアクセスするようなテストは避けるが、本番にデプロイする予定のソースコードを、本番環境のリソースに影響が出ない範囲でテストするのは行っておきたいもの。
- 自動デプロイ
  - 今回はお手軽にデプロイする方向なので、masterブランチに入った以上はデプロイまで自動で行ってOK。
  - [デプロイする前に手動の承認を必要とする、みたいな作り](https://zenn.dev/matken/articles/approve-deployments-with-github-environments)も考えられるが、今回はそこまでしない。
- デプロイ内容のトレーサビリティの確保
  - コンテナなら話は早い。ECRにコンテナを残しておけばいいだけだ。
    - 当然CI/CD時のログは残しているものとして。
  - 問題はソースコードをZIPで固める場合。これもアップロードしたファイルを消滅させるのではなく、ちゃんと履歴として残したい。**かなり長く、最低でも３か月くらいは**。
    - ということはS3に一度アップロードして、それを指定する方法でデプロイすることになるはず。
- 即時ロールバックができること
  - デプロイしなおしではなく、切り替え式のデプロイを使うこと
    - といってもLambda関数にはバージョンを保持する機能が元からあるので、デプロイだけしてlatestにいきなりバチッと100%切り替えるような真似をしなければいいだけのような気もする。
- 本番直前環境(preとかstagingと呼ばれるような)は今回使わない
  - これは本来作ったほうがいい。
  - が、そこまでするほどの規模・品質要求の高さを想定していないため、今回は省略。
  - GitHub Flow式、すなわちmasterブランチに入れた以上はデプロイを許可されているものとみなす方式を取っているからでもある。
- （できれば）関係ない関数までデプロイしない
  - これはGitHub Actionsなら実現できるのではないかと期待している。
- （できれば）アクセスキーをGitHubに持たせない
  - [OpenIdConnectに対応しているそうで](https://zenn.dev/miyajan/articles/github-actions-support-openid-connect)、極力その方向で行きたい。
