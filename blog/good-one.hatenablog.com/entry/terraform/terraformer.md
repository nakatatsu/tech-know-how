---
Title: WindowsでTerraformerを利用する
Category:
- terraformer
- Terraform
Date: 2022-10-05T15:06:27+09:00
---

自サイト用のインフラをTerraform管理に移行するにあたり、まず既存のリソースをコード化する必要があった。

そこで[terraformer](https://github.com/GoogleCloudPlatform/terraformer)を利用し、既存リソースを元にScaffoldingを行うことにした。

[:contents]

# Terraformer のInstall

公式の手順通りでインストールできる。

1. (まだ入れていなければ）[Terraform](https://www.terraform.io/downloads)をインストール
2. [terraformerのバイナリ配布ページ](https://github.com/GoogleCloudPlatform/terraformer/releases)からwindows用のバイナリを取得
3. 取得したバイナリは拡張子がなぜかついていないので、リネームして.exeをつける。
4. リネームした実行ファイルにパスを通すか、パスを通したディレクトリに実行ファイルを配置する。
5. `terraformer --version`と打ってみてバージョンが表示されればOK。


# Usage

適当なディレクトリを作成し、そこへmain.tfを以下の内容で配置する。バージョンは適宜変更のこと。

    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 4.33"
        }
      }

      required_version = "1.3.1"
    }

    provider "aws" {
      region  = "ap-northeast-1"
    }

Terraformの初期化コマンドを入力し、

    terraform init

[公式ドキュメント](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/aws.md)を参考にリソースタイプを選択しつつコマンドを入力。


    terraformer import aws --resources=vpc --connect=true --regions=ap-northeast-1

generated\aws 以下に目当てのリソースのTerraform用構成ファイルが作成される。

    │  .terraform.lock.hcl
    │  main.tf
    │
    ├─.terraform
    │  └─providers
    │      └─registry.terraform.io
    │          └─hashicorp
    │              └─aws
    │                  └─4.33.0
    │                      └─windows_amd64
    │                              terraform-provider-aws_v4.33.0_x5.exe
    │
    └─generated
        └─aws
            └─vpc
                    outputs.tf
                    provider.tf
                    terraform.tfstate
                    vpc.tf