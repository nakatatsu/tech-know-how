---
Title: AWS Lambdaをローカルで開発・テストするには？
Category:
- AWS
- Lambda
- Python
Date: 2022-10-13T14:09:46+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-local-development
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889927073042
---

Pythonを使ったAWS LambdaはAWSのマネジメントコンソールから直接コーディングとテスト（とデバッグ）ができる。

が、コーディング時にVSCodeや周辺ツールが使えないのは辛い。それにローカル環境で行える作業とテスト/デバッグはローカルで行いたい。

[:contents]

# 先に結論

次の方針で実行することにした。

- なるべくテスタビリティの高いコードを書いた上で（大前提）
- ローカルでできるテストはローカルで行う。
- ローカルでできないテストはAWS上で行う。
- Windows上のVSCode + AWS公式Lambdaコンテナで開発

# そもそも何をどこまでどうテストできるのか

単体テスト/結合テスト/システムテストの３つのフェーズでテストすると仮定すると、次のように整理できる。

| 名称   | 対象                | 環境 |
|--------|-------------------------------|--|
| 1. 単体テスト | 各関数ごとのテスト    |ローカルまたはCIでの自動テスト |
| 2. 結合テスト    | 呼び出し元の関数とそこから呼び出されるいくつかの関数の集まりのテスト | ローカルまたはCIでの自動テスト、AWS上の開発用Lambda関数を使った手動テスト |
| 3. システムテスト   | 本番環境と極力合わせた環境とフローでのテスト              | AWS上の開発用Lambda関数および利用元のFrontendを使った手動テスト |

プロジェクトによってテストの名前や段階、範囲はそれぞれ異なっているものだが――システムテストの後に発注者による受入テストがあったりする――、ここでは上記形態とする。開発者と発注者が同じ会社の中にいる想定である。

上述の通り、ローカル環境で完結できるテストは２の結合テスト（の一部）までとなる。

３のシステムテストは当然にローカルで行うことはできない。本番同様にAWS上で動かさないといけないためである。

また２の結合テストも、依存するAWSのリソースをスタブで代用できないなら、ローカルで完結させるわけにいかない(Lambdaを起動しないといけないから)。実際のAWSリソースを利用する他ない。つまり開発用であってもLambda関数はどの道どこかで必ず作成することになる。

Lambda関数の数が少なく、専用のローカル開発環境を整備するのがコストに見合わないようであれば、さっさと割り切って開発用のLambda関数を作ってしまい、ゴリゴリAWSリソースに依存して（もちろん開発環境用の）テストとデバッグをしたほうがおそらく有利だろう。ハッキリ言ってローカル開発環境を整備するのはコストのかかる作業である。一つ二つの小さな関数くらいはブラウザ上で（お行儀は良くないが）編集してしまったほうがよほど早い。

だがサービスのかなりの部分をサーバーレスで作成していて（もしくは作成する予定で）、専用のローカル開発環境を整備するだけの価値があるようなら、なるべくローカルでできることはローカルで行うようにするメリットが上回るのではないか。


# ローカルでLambda関数を開発するには？

結局のところ、Windows上のVSCodeを使いつつ、起動はAWS公式Lambdaコンテナ上で行うのが鉄板な印象。

なにぶんLambda自体はAmazonLinux2で動いているので思わぬ環境のズレが怖いし、direnvなどの周辺ツールもWindows版がないことがあってお辛い。Dockerfileを通して開発環境をカッチリ固定できる（しかもいらなくなったら簡単に捨てられる）ためチーム全体の環境を統一するのも比較的簡単、という点も見逃せない。

Volumeをマウントすれば編集自体はWindows上でできるため、使用感はさほど変わらない。

起動する際に一度コンテナ内に入る手間がかかるが、これもVSCodeのリモート開発から編集する方式にすれば軽減できる。ただリモート開発はまだPreview版のため、業務用として推奨し難いのが辛いところ。

ローカルでの起動は`python -c`や`python-lambda-local`でなんとかなる。ユニットテストをしたいならpytestが使える。AWSリソースに依存する部分（AWS SESとか）のテストにはアクセスキーの発行が必要となり、セキュリティ維持が若干手間になるのだが、MFA必須にすることで（手間だが）フォローは可能。

AWS Toolkit for Visual Studio Codeは、便利なのは便利なのだが、IoCやCI/CDを前提とすると意外に使いどころがない。構築・デプロイという用途がモロに被るからだ。そういったことをしない小規模プロジェクトであればブイブイ言わせそうな印象だが、無理に入れなくてもいいかもしれない。


# 環境変数をどうするか？

[direnv](https://github.com/direnv/direnv)を使うと楽。python-lambda-localでも直接指定できる機能があるようだ（未確認）。


# 参考

- https://speakerdeck.com/twada/testable-lambda-working-effectively-with-legacy-lambda
