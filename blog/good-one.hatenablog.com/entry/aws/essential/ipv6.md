---
Title: IPv6オンリーのVPCで遊んでみた
Category:
- AWS
- IPv6
Date: 2022-11-15T12:48:44+09:00
URL: https://blog.tricrow.com/entry/aws/essential/ipv6
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889936779788
---

タイトルの通り、IPv6オンリーのVPCを試してみた。[以前の記事](https://blog.tricrow.com/entry/aws/tips/2022111416)でIPv6オンリーは業務用だと要注意、と書いたばかりだが、個人用途で試す分にはイケイケでいける。NAT ゲートウェイがいらない（Egress Only IGWが使えるので）ため安くあがる点が個人用途だとポイントである。



[:contents]


# ネットワーク上の主な違い

- SubnetにIPv4を振らない。
  - VPCにはIPv4を設定する必要があった。
- NAT Gatewayがいらない。
  - 代わりにEgress-Only Internet Gatewayを使う。固定費がかからないNATゲートウェイみたいなものである。
- Elastic IPがいらない。
  - IPv6だから元から固定IPとして使える。
- **全ての**場面でIPv6を使うことになる。
  - ローカルのPCからSSHで接続するのもIPv6である。
  - "いかん、ここはIPv4でないと困る"みたいなことがあっても対応不能である。
    - 大抵問題ないはずだが、**"動くはず"と"動いた"は違う**。
      - という問題があるので業務用でIPv6オンリーはなかなか怖いわけだが。




# 気づいたこと

遊んでいて気になったことがいくつかあった。やはりIPv6オンリーで利用すると細かいところが違ってくる。

## IPアドレス直での管理は避けたほうが良い

[公式リファレンス](https://docs.aws.amazon.com/ja_jp/vpc/latest/userguide/configure-your-vpc.html#vpc-sizing-ipv6)に

> IPv6 CIDR ブロックと VPC の関連付けを解除できます。VPC から IPv6 CIDR ブロックの関連付けを解除すると、IPv6 CIDR ブロックと VPC を後で再び関連付けた場合に同じ CIDR を受け取ることは期待できません。

とある。従って、VPC内のEC2を管理するにあたって /etc/hostsにIPを直接記載したり、プログラム内でIPを直接記載したり（あまり良い造りではないが）すると変化に弱くなる。もしIPを振り直しになった場合、直接記載した部分を全部修正しないといけなくなるだろう。面倒に感じても、DNSを使ってホスト名で管理したほうが良い。

## ElasticIPがいらない

[公式ドキュメントによると](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/Stop_Start.html#what-happens-stop)、

> インスタンスを停止しても、次のものは保持されます。  
> IPv6 アドレス。

だそうである。実際、停止→起動を行ってみても保持されたので、本当だと思われる。つまりElasticIPを使う必要がない。例えば、踏み台サーバーを普段止めておいて使うときだけ起動する使い方をしても、EIP料金を取られなくていいわけだ。地味に嬉しいポイントである。

一方で、常に固定IP状態とも言えるので、セキュリティには十分気を使わないといけないが。

## 書式がIPv4と異なる

IP直で接続する場合、IPv6は[]で囲む必要がある。そのためWEBサーバーにアクセスする場合でも、IPv4ならhttp://192.168.1.1/のように接続できるが、IPv6だとhttp://[xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx]/のように記載しないといけない。

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/g/good-one/20221115/20221115114157.png" alt="20221115114157">



これはSSHで接続する場合も同じで、configの記載が微妙に異なる。

    Host bastion
        HostName xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:79c2


    Host develop-target
        HostName xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:670b

    Host develop-*
        ProxyCommand ssh bastion -W [%h]:%p <- ここである。
        #   ProxyCommand ssh bastion -W %h:%p <- IPv4ならこう書く。

    Host *
        Port 22
        User ec2-user
        IdentityFile ~/.ssh/test.pem
