---
Title: 'Cannotpullcontainererror: pull image manifest has been retried 5 time(s):
  failed to resolve ref docker.io/library/nginx:latest: failed to do request'
Category:
- AWS
- IPv6
Date: 2022-11-16T00:41:19+09:00
URL: https://blog.tricrow.com/entry/aws/essential/ipv6-docker
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889936951874
---

[先の記事](https://blog.tricrow.com/entry/aws/essential/ipv6)の後にもIPv6 Only VPCを試していたのだが、思わぬところに落とし穴がやはりあった。

[:contents]

# 問題

    "Cannotpullcontainererror: pull image manifest has been retried 5 time(s): failed to resolve ref docker.io/library/nginx:latest: failed to do request"

Fargateを試していたのだが、どういうわけかDockerHubからコンテナが取得できない。上述のエラーメッセージが表示される。

なんとDockerHubがIPv6非対応らしい。

# 解決

仕方ないのでSubnetにIPv4を設定し、IPv4/IPv6デュアルスタックにして対応したところ解決した。しかしこの対応だと、Private Subnetに置くためにはNatゲートウェイが必要になるわけで、なんともトホホな結果である。

SecurityGroupで接続元をALBに限定すればpublic subnetに置いていてもおかしな通信を叩き込まれることはないはず、と言えばそうなのだが、SGの設定を間違えると素通しになるわけで、あまり嬉しくない防御法である。


# その他

ちゃんと検証していないが、[こちらの記事](https://zenn.dev/ekrecker/articles/a66b8ccc80c650)にもある通り、Target GroupもIPv4を使っていそうな雰囲気。

あとECRがIPv6対応しているのか公式ドキュメントを探しても記載箇所が見つからない。これもかなり心配な感じである。こちらはGatewayを使えばいいのかもしれないがegress only IGWで対応できないとなるとコスト面で（業務用なら屁でもないのだが）辛みがでる。

総じて**IPv6 onlyはまだまだいばらの道**という感がある。IPv6自体は便利だと思うのだが、周辺サービスがついてきていない。業務用だと、当面はIPv4を大人しく使うか、デュアルスタックで部分的に導入するか、といった選択になるのではなかろうか。見切り発車でIPv6 onlyを選択すると大変苦労するであろう。
