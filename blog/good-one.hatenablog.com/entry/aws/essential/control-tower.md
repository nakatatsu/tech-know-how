---
Title: これからAWSを始めるならControl Towerの利用がよさそう
Category:
- AWS
- Control Tower
---

AWSでは事故防止やセキュリティ向上のためマルチアカウントの利用が望ましい。が、これがなかなか大変で、各アカウントの管理やそこで出る監査用のログの収集、セキュリティなどの各課題をどう設計するかは悩みどころだった。

が、AWSが[規範的なガイドライン](https://docs.aws.amazon.com/ja_jp/prescriptive-guidance/latest/migration-aws-environment/welcome.html)とAWS Control Towerを提供してくれたため、今ではとりあえずそれに乗っかるということができるようになっている。

これからAWSを始めるならControl Towerの利用がよさそうである。

[:contents]


# AWS Control Towerとは

[公式](https://docs.aws.amazon.com/ja_jp/controltower/latest/userguide/what-is-control-tower.html)にある通りだが、つまりはマルチアカウントを簡単に利用できるようにしてくれるサービスである。

- マルチアカウント管理
- Single Sign-Onの提供（IAM Identity Center）
- CloudTrailをはじめとする内部統制・セキュリティ系のサービスの設定

などを行ってくれる。かつてはこれらを逐一バラバラに自分で設定する必要があったが、これらをオーケストレーションしてくれるので大変に助かる。

また、Single Sign-OnはAWS CLIにも対応しているため、MFAも使える。これもうれしいところだ。CLIからMFAを利用するために苦労してあれこれとややこしい設定をするまでもなく、IAM Identity Centerの仕組みに乗っかるだけで済む。

これらの仕組みを、このレベルで一から検討・構築・運用しようと思ったら、一月どころでは済まないだろう。

