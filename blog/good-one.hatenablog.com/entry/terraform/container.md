---
Title: DockerでTerraformを利用してみる
Category:
- Docker
- Terraform
Date: 2022-11-13T18:05:15+09:00
URL: https://blog.tricrow.com/entry/terraform/container
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889936215579
---

しばらく暫定的にWindow直でTerraformを利用していたが、環境を再現しづらく、従って環境の統一もしづらい問題が気になる。ついでに、AWSをMFA付きで利用するにあたっては、いちいち[公式で紹介されている手順](https://aws.amazon.com/jp/premiumsupport/knowledge-center/authenticate-mfa-cli/)を使うのも地味に手間がかかるので、[こちらで紹介されている](https://qiita.com/mizue/items/8292a1ea39d31a0d43bf)スクリプトを導入したいところ。

というわけで試してみることにした。

ちなみにTerraformの[公式コンテナ](https://hub.docker.com/r/hashicorp/terraform)のページに曰く、

> Running Terraform inside a Docker container requires more configuration than running the Terraform CLI executables directly. Unless you need container isolation, we recommend using the non-containerized Terraform CLI packages.

意訳：　コンテナ上でTerraformを使うのは、CLIを直接設置するのに比べて必要な設定が多くなる。コンテナとして隔離しなくていいんだったらCLIをそのまま使ったほうがいいと思うよ。

だそうである。

やってみた感じ、たしかにこれは真実であった。


[:contents]

# やること

1. ベースイメージを決め、Dockerfileを作る
2. AWS CLIで使うための設定ファイルを用意する
3. docker-composeでビルドと起動
4. コンテナに入って起動

コンテナを起動する際にterraformも起動する方式が、たぶんコンテナの精神には沿うのだろうが――たしかワンバイナリっぽく扱うのがカッコいいとされていたはず、公式のTerraformコンテナもそんな作りになっている――、今回の場合、それだとトライ・エラーがやりづらい。というわけで自分が使いやすいようにdocker execを使うことにした。


# 1. ベースイメージを決め、Dockerfileを作る

Terraformは[公式がコンテナを用意してくれている](https://hub.docker.com/r/hashicorp/terraform)のだが、開発しながら利用するにはAlpineで使いづらい。そのためあえて避け、amazon/aws-cli:latestにTerraformをインストールして使うことにした。もっとプレーンなイメージにAWS CLIとTerraformをインストールして使ってもいいわけだが、aws-cliがプリインストールされているAWSオフィシャルなAmazonLinux2という点が個人的にポイントであった。

## Dockerfile

Dockerfileはこれだけ。

    FROM amazon/aws-cli:latest

    RUN yum update -y
    RUN yum install -y unzip jq tar gzip
    RUN curl  -OL https://releases.hashicorp.com/terraform/1.3.4/terraform_1.3.4_linux_amd64.zip
    RUN unzip terraform_1.3.4_linux_amd64.zip -d /bin

    ENTRYPOINT ["/bin/bash"]

tarやgzipはリモートデスクトップに必要だった。

# 2. AWS CLIで使うための設定ファイルを用意する

これはaws configureをホスト（自分の環境ではWindows)側で実行し、docker-compose.ymlでボリュームをマウントすればOK。

        version: "3.9"
        services:
        terraform:
            container_name: terraform
            build: ./containers/terraform1.3
            tty: true
            volumes:
            - ./src:/src
            - ~/.aws:/root/.aws

# 3. docker-composeでビルドと起動

下記コマンドを打つ。

    docker-compose up --build

# 4. コンテナに入って起動

下記コマンドを打つ。

    docker-compose exec terraform /bin/bash

# 実際に利用してみた結果

結論、これはこれで手間がかかる。というのは、`terraform apply`をかけた後でキャンセルしただけでもコンテナからログアウトしてしまうため。

MFA認証がいらないならまた話が変わってきそうだが、要MFAだと、環境の統一はWSLで行うほうが良い印象。

究極的には、いっそクラウド版のTerraformやEC2上でTerraformを利用するにしくはないかも。
