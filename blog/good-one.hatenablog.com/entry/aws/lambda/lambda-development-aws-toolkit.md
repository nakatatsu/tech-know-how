---
Title: VSCode+AWS Toolkit+SAMでAWS Lambda関数を作成・デバッグ（開発環境用、NOT 本番環境用）
Category:
- AWS
- Lambda
- Python
Date: 2022-10-11T20:08:17+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-development-aws-toolkit
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889926561213
---

AWS Lambda関数の開発にあたり、Localでできる作業はLocalで行うにしても、やはりAWS上で動かさないと仕方ない部分が残る。

といって、いくら開発環境用だとしても、マネジメントコンソール上で編集するのはVSCodeの開発ツールが使えないので嬉しくないし、管理上もさすがにいかがなものか感ある。

そこでVSCode + AWS ToolkitでローカルからAWSの**開発用**関数になるべくシームレスにアップロード・テスト・デバッグができるようにする。

尚、あくまで開発時専用のフローを想定したものであり、本番環境用ではない。

[:contents]


# AWS SAM

## Install

SAM CLIをインストールする。

[公式ドキュメント](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)の通りに行えばインストールできる。

ついでにDockerもインストールしておく。どの道開発環境の作成で必要になる事項。

# AWS Toolkit for Visual Studio Code

## Install

VSCodeの拡張機能でAWS Toolkitを選択し、インストールする。

ただしリソースの利用にはIAM権限が必要なため、aws configureなどで適宜用意しておく。

すでに自分の環境ではAWS CLIの利用時にaws configureで設定を済ませており、VSCodeもインストールしていたため、これらは省略できた。

これでプライマリサイドバーにAWSのマークが表示される。

公式Document: https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html


# 関数を追加

上記手順でAWSにVSCodeからLambda関数をアップロードできる。

## 手順の概要

1. Terraformで空の関数を先に作る。
2. VSCodeのAWS Toolkitでダウンロードする。
3. VSCodeで編集する。
4. VSCodeのAWS Toolkitでアップロードする。
5. VSCodeのAWS Toolkitで実行(invoke)する。

開発時は、先にTerraformで空の関数を先に作っておき、それを編集する形がよいと判断した。

VSCodeからLambda関数を新規作成することもできるようだが、自分の環境で試したところ途中でスタックして動かなかった。ただ、そうでなくとも、直接リソースを新規作成する運用にすると構成管理システムとの連携が複雑化する。

Lambda関数のコーディングにTerraformを関わらせるメリットは、開発が煩雑化するデメリットに見合わないと感じる。そのため上述の手順としている。ちなみにアップロードは、コンテナ上のPython+Remote開発と組み合わせるなら、シェルスクリプトを用いてAWS CLI経由でアップロードするほうが簡単かつ確実な印象。オペミスが怖い業務用のフローだとそちらで行うかもしれない。

また、できることならAWS Organizationsを使うなどして、アカウントを開発用と本番用で分けておくほうが安全。それが困難なら、命名規則で開発用関数はprefixとして"develop"をつけるものとし、かつVSCodeから使えるIAM権限をリソース名に限定条件を入れるなどしてproductionの関数を編集してしまわないようにする。

たとえばこんな感じのポリシーを使う。

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "LambdaEditDevelopOnly",
                "Effect": "Allow",
                "Action": [
                    "lambda:Invoke*",
                    "lambda:Publish*",
                    "lambda:Put*",
                    "lambda:TagResource",
                    "lambda:UntagResource",
                    "lambda:Update*"
                ],
                "Resource": "arn:aws:lambda:*:*:function:develop*"
            },
            {
                "Sid": "LambdaGetInformation",
                "Effect": "Allow",
                "Action": [
                    "lambda:Get*",
                    "lambda:List*",
                    "tag:GetResources"
                ],
                "Resource": "*"
            }
        ]
    }

AWS Toolkitは手作業でデプロイ先の関数を決めるようになっており、デプロイ先を誤って選択するオペミスが十分起こりえる。この程度のセーフティはかけておいてしかるべきだろう。

# Terraformとの関係は？

下記の方針をとる。

1. 関数や周辺リソースの構築・修正にのみTerraformを関わらせる。
2. コードの作成や修正にTerraformは関わらせない。

関数や周辺リソースの作成にはTerraformを使いたい。しかし一方で、開発中のコードのデプロイはむしろTerraformに一切関与させたくない。頻繁にトライ・エラーを繰り返すフェーズで煩雑なデプロイやチェックを必要にしてしまうと開発効率を損なう。

本番環境はまだしも、開発環境では、アプリ開発側がインフラエンジニアにいちいちお伺いを立てることなく自由にコードの編集・実行・修正ができなければならない。また、迅速に、それもできれば数秒程度で――それを望めるのがＬＬのはずだ――デプロイが終わらなければならない。productやrelease(stagingという名前かもしれない)なら品質重視だからCI/CDを行うべきだが、開発環境では開発効率を重視するべきだ。


## トラブルシューティング

### パス長制限問題

実行時、Windows10のパス長制限に抵触して`Error: Unstable state when updating repo. Check that you have permissions to create/delete`とエラーが出てしまった。これは長いパスを受け入れるようレジストリを編集することで解消された。

    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

### IAM Policyの権限不足エラーメッセージが違う問題

"lambda:Get*"と"lambda:List*"だけでは読み取りに失敗する。tag:GetResourcesも読み取り権限に必要。ところが、それが足りないときのエラーメッセージとして`lambda:ListFunctions on resource: *`が表示される。結局公式ポリシーLambda読み取り専用ユーザーの内容を参考にデバッグしたのだが、なかなかのハマりどころだった。


# 参考

- https://speakerdeck.com/twada/testable-lambda-working-effectively-with-legacy-lambda
- https://github.com/aws/aws-sam-cli/issues/4031
- https://blog.nijohando.jp/post/2020/partially-managing-lambda-with-terraform/
