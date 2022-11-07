---
Title: Terraformの*.tfstateファイルを保存するためのS3のバケットをCLIで作る
Category:
- AWS
- S3
- Terraform
Date: 2022-11-01T19:49:13+09:00
URL: https://blog.tricrow.com/entry/aws/s3/bucket-for-terraform
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889932788731
---

TerraformのtfstateファイルをS3に保存する場合、そのバケット自体はTerraformを使わずに作成することが推奨されている。

というわけで、CLIを使ってバケットを作成することにした。

# コマンド

先にコマンドを記載する。結論、以下のようにした。

    aws s3api create-bucket --region ap-northeast-1 --create-bucket-configuration LocationConstraint=ap-northeast-1 --bucket [BUCKET_NAME]
    aws s3api put-bucket-versioning --bucket [BUCKET_NAME] --versioning-configuration Status=Enabled
    aws s3api get-bucket-versioning --bucket [BUCKET_NAME]
    aws s3api put-public-access-block --bucket [BUCKET_NAME] --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
    aws s3api get-public-access-block --bucket [BUCKET_NAME]
    aws s3api put-bucket-encryption --bucket [BUCKET_NAME] --server-side-encryption-configuration "{\"Rules\":[{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\":\"AES256\"}}]}"
    aws s3api get-bucket-encryption --bucket [BUCKET_NAME]
    aws s3api put-bucket-tagging --bucket [BUCKET_NAME] --tagging "TagSet=[{Key=Environment,Value=[ENVIRONMENT]}]"
    aws s3api get-bucket-tagging --bucket [BUCKET_NAME]

`[BUCKET_NAME]`には実際のバケット名が入る。また、`[ENVIRONMENT]`には環境名が入るのだが、タグのつけ方は状況にあわされたし。

# コマンドの説明

バケットは以下の方針で作っている。

- バケット名は[環境名]-[用途]-[ユニークにするための文字列]とする。
  - e.g. product-log-abcdefgh
- バージョニングを有効化する。
  - うっかり消してしまうと悲惨なので。
- セキュリティのため、パブリックアクセスブロックは全部ブロック。またサーバーサイド暗号化も有効化する。
  - 個人で使うTerraformなのでAmazon S3 マネージドキーによる暗号化で済ませているが、より強固にしたいならKMSタイプを。
- タグも付けておく。
