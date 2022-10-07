---
Title: AWS Lambda Pythonで外部ライブラリを利用する
Category:
- AWS
- Lambda
- Python
Date: 2022-10-08T00:55:57+09:00
URL: https://blog.tricrow.com/entry/aws/lambda/lambda-layer
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889925454394
---

AWS Lambda（Python利用）でcerberusを使いたいが、Lambdaにはこちらの欲しいライブラリがインストールされていないため当然ながらエラーになる。

そこでLayerを使って先に外部ライブラリを用意しておく。

[:contents]


# 準備

WSLでUbuntuを起動し、python3.9とaws cliをインストールする。

コマンドは以下。

    sudo apt -y update
    sudo apt -y dist-upgrade
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt -y install zip unzip python3.9 python3.9-venv python3-pip
    sudo ln -s /usr/bin/python3.9 /usr/bin/python

    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    aws configure

なお、python3で指定してインストールすると3.10が入ってしまったため、3.9を指定して入れなおしている。

# 作成とアップロードの例

ここではcerberusとemail_validatorをLayerとしてアップロードしている。各パラメータは固有のため適宜変更の必要あり。

なおディレクトリ名は**必ず**python/ を指定する。[Lambdaの仕様上そう指定されている](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-layers.html#configuration-layers-path)ので、適当なディレクトリ名を使うと動作しない。

    mkdir python
    pip install -t python/ cerberus email_validator
    chmod 755 -R python/
    zip -r cerberus.zip python/
    aws lambda publish-layer-version --layer-name develop-cerberus --zip-file fileb://cerberus.zip --compatible-runtimes python3.9
    aws lambda update-function-configuration --function-name develop_send_mail  --layers "arn:aws:lambda:ap-northeast-1:XXXXXXXXXXXX:layer:develop-cerberus:1"


# 備考

- Zipで圧縮したライブラリ群をAWS Lambdaにアップロードするだけなのだが、OSはLinux、CPUのアーキテクチャも作業するノードとLambdaの設定を合わせなければ動作しない恐れがある。そのためWindowsから直接行うことはできず、WSL上のUbuntuから行う。また対応できるLambda関数もx86_64のもののみと考える。
- arm64のほうが料金が安いのだが――大ざっぱに8掛けくらい――もともとそこまでLambdaの料金が高いサービスを扱う予定はないのでx64のまま使ってしまう。もし大きなコストがかかるLambdaの使い方をするなら、arm64を使うことを改めて検討する。


# 参考

- https://bftnagoya.hateblo.jp/entry/2021/06/23/074120
- https://qiita.com/kai_kou/items/87b56e91a096af757fbd
