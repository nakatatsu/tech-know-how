---
Title: Terraformの.tfstateファイルをS3に保存する際の手順（DynamoDBなし）
Category:
- Terraform
- AWS
Date: 2022-10-06T15:11:01+09:00
URL: https://blog.tricrow.com/entry/terraform/terraform-tfstate-s3
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889925012622
---

AWSリソースをTerraformで扱う際、もしも.tfstateファイルをS3に保存するなら事前にバケットを作成する必要がある。

その際の手順を記載する。

ただしDynamoDBを用いてのロックは行っていない。

[:contents]

# S3 Bucketの用意

.tfstateをS3に保存する場合、Bucketを用意する必要がある。詳細は[公式ドキュメント](https://www.terraform.io/language/settings/backends/s3)が詳しい。

このBucketは素直にAWS CLIで作成する。[公式曰く](https://www.terraform.io/language/settings/backends/s3)、これをTerraformで実行するのは非推奨とのことである↓

> Terraform is an administrative tool that manages your infrastructure, and so ideally the infrastructure that is used by Terraform should exist outside of the infrastructure that Terraform manages. This can be achieved by creating a separate administrative AWS account which contains the user accounts used by human operators and any infrastructure and tools used to manage the other accounts. Isolating shared administrative tools from your main environments has a number of advantages, such as avoiding accidentally damaging the administrative infrastructure while changing the target infrastructure, and reducing the risk that an attacker might abuse production infrastructure to gain access to the (usually more privileged) administrative infrastructure.

また、場合によっては秘密情報が含まれる.tfstateを保存するわけだから、セキュリティに気を使う必要がある。またデータの保全も欲しい。というわけで次の設定を行いたい。

- 非公開にする
- サーバーサイドの暗号化を行う
- バージョニングを行う

また、タグもつけておく。

## Bucketの作成コマンド

以下で作成した。バケット名、リージョン、タグなどの細かい点は各環境に合わせる必要あり。


    # バケット作成
    aws s3api create-bucket --bucket development-terraform-20221006  --region "ap-northeast-1" --create-bucket-configuration LocationConstraint="ap-northeast-1"
    # サーバーサイドの暗号化を行う
    # この行だけはPowershellではなくコマンドプロンプトを使う。ダブルクォーテーションのエスケープがpowershellで通らなかったため。
    aws s3api put-bucket-encryption --bucket development-terraform-20221006 --server-side-encryption-configuration "{""Rules"" : [{""ApplyServerSideEncryptionByDefault"" : {""SSEAlgorithm"" : ""AES256""}}]}"
    # 非公開にする
    aws s3api put-public-access-block --bucket development-terraform-20221006 --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    # バージョニングを行う
    aws s3api put-bucket-versioning  --bucket development-terraform-20221006 --versioning-configuration Status=Enabled
    # タグをつける
    aws s3api put-bucket-tagging --bucket development-terraform-20221006 --tagging 'TagSet=[{Key=Environment,Value=development},{Key=Service,Value=shared}]'
 

# その他

- 今回は行わないが、S3とDynanoDBを併用してロックする方法もあるそうである。
- Teamで運用するならTerraform用の小さなEC2インスタンスを用意してそこで実行するほうが確実じゃないかと思われる。インスタンスを分ければ環境ごとにIAM Roleを作って割り振るのも簡単だし。
  - Terraform用のアクセス権限の管理を業務で通用するレベルで行うのはなかなか大変で、小さなインスタンスを一つ立てておくくらいの価値はある。お金がもったいないと思うなら都度start/stopすれば費用は最小限で済む。
  - 詳しくないがTerraform Cloudでもいいのかもしれない。

# 参考

- https://qiita.com/tsukakei/items/2751e245e38c814225f1
- https://qiita.com/sinshutu/items/7d3cc7438871c50ea63c
