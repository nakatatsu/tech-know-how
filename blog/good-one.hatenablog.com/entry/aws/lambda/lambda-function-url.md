---
Title: API Gatewayを通さず直接Lambdaにアクセスする機能を試してみた(Lambda 関数URL)
Category:
- AWS
- Lambda
- Python
Date: 2022-10-13T13:19:30+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-function-url
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889927059785
---

[Lambda 関数URL](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-urls.html)を使ってAPI Gatewayを通さず直接Lambdaにアクセスする機能を試してみた。

[:contents]


# 結論、どうなのか？

便利なのだが簡易版といった趣で、不便な点もある。"やったぞAPI Gatewayがいらなくなった！"と言えるわけでは**ない**。

特に、2022/10現在、**エンドポイントをこちらで指定できない**というのがかなりの落とし穴と感じる。

大抵の業務用用途では、途中でリバースプロキシをはさむなどしてクライアントからはエイリアス的なエンドポイント（e.g. https://api.example.com/user/)にアクセスさせるようにし、生の関数URL（e.g. https://XXXXXXXXXXXXX.lambda-url.ap-northeast-1.on.aws)は隠ぺいしたほうが安全であろうと思われる。

    # たとえばこういう構成
    [Client] --(https://api.example.com/user/)--> [Reverse proxy] --(https://XXXXXXXXXXXXX.lambda-url.ap-northeast-1.on.aws)--> [Lambda]


というのは、うっかり関数URLをクライアントに直で持たせると、Lambda関数を新しく作りなおしたりB/Gデプロイで切り替えたりするたびにクライアントも直さないといけなくなってしまうためだ。

Terraformを使っていると、設定の修正内容によってはリソースを削除→新規作成されてしまうことが時折あるので、なおさらこの点は気になるところ。

ただ、それをマネージドで実現できるソリューションとはAPI Gatewayなのでは、という説もあり（CloudFrontも要件次第では使えるかもしれないが）、将来どうなるか読めないならAPI Gateway+ Lambdaという古式ゆかしき構成をとっておくのが鉄板な気がする。

一方、その辺りが気にならないなら、API Gatewayを通さずに直接使えるのはすばらしく便利であり、ちょっとの間使えれば十分、みたいな用途ならガンガン使ってよさそう。

# Terraformを使ったコードの例

aws_lambda_function_urlがFunction URLを設定する部分。

    resource "aws_lambda_function" "send_mail" {
    architectures                  = ["x86_64"]
    function_name                  = local.send_mail_function_name
    handler                        = "main.lambda_handler"
    memory_size                    = "128"
    package_type                   = "Zip"
    reserved_concurrent_executions = "-1"
    publish                        = false
    role                           = aws_iam_role.send_mail.arn
    runtime                        = "python3.9"
    timeout                        = "10"
    s3_bucket                      = var.administrative_bucket
    s3_key                         = var.send_mail_s3_key
    ephemeral_storage {
        size = "512"
    }
    tracing_config {
        mode = "PassThrough"
    }
    environment {
        variables = {
        REGION             = var.region
        SERVICE_ADMIN_MAIL = var.administrator_mail_address
        SERVICE_NAME       = var.service_name
        SERVICE_URL        = var.service_url
        REPLY_TITLE        = var.mail_reply_title
        }
    }
    }

    resource "aws_lambda_function_url" "send_mail" {
    function_name      = aws_lambda_function.send_mail.function_name
    authorization_type = "NONE"

    cors {
        allow_origins = var.cors_allow_origins
        allow_methods = ["POST"]
        max_age       = 86400
    }
    }

cors_allow_originsはterraform.tfvarsに記載しており、ドメインは実際と変えているがこのような内容となっている。

    cors_allow_origins = ["https://www.example.com", "http://www.example.com"]


# 参考

- https://tech.nri-net.com/entry/lambda_url
- https://dev.classmethod.jp/articles/try-aws-lambda-function-urls/
