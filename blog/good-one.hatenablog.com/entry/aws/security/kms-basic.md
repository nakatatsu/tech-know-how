---
Title: AWS KMSを復習してみる
Category:
- Tips
- AWS
- Security
- KMS
Date: 2022-12-19T21:32:23+09:00
URL: https://blog.tricrow.com/entry/aws/security/kms-basic
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889946506660
---

KMSを改めて復習したくなったので、自前のメモがてらに記事にしてみる。

[:contents]


# KMSとは？

[データの暗号化やデジタル署名に使用するキーを作成して管理する](https://aws.amazon.com/jp/kms/)マネージドサービス。

データの暗号化や複合などの処理まで行うというよりは（※）、キーの管理をメインとしているサービスである。

暗号化に使うキー（ファイル）の保管は、がっちりセキュリティを守ろうとすると難題で、「盗っ人に入られたらどうするんだ」なんてことまで気にしないといけなくなる。そういうことをしなくて済むのは大変ありがたい。

※ [データキーの生成、暗号化、復号はKMS側で行う](https://docs.aws.amazon.com/ja_jp/kms/latest/developerguide/concepts.html#data-keys)。[エンベロープ暗号化戦略](https://docs.aws.amazon.com/ja_jp/wellarchitected/latest/financial-services-industry-lens/use-envelope-encryption-with-customer-master-keys.html)を採用しているため。

> AWS KMS はデータキーの生成時、即座に使用 (オプション) できるプレーンテキストのデータキーと、データと共に安全に保存できるデータキーの暗号化されたコピーを返します。データを復号する準備ができたら、最初に AWS KMS を要求して、暗号化されたデータキーを復号します。
> AWS KMS はデータキーを生成、暗号化、復号します。ただし、AWS KMS はデータキーの保存、管理、追跡、またはデータキーの暗号化オペレーションを実行しません。AWS KMS の外部でデータキーを使用して管理する必要があります。データキーを安全に使用する方法については、「AWS Encryption SDK」を参照してください。（[AWS KMS の概念](https://docs.aws.amazon.com/ja_jp/kms/latest/developerguide/concepts.html#data-keys)）


# KMSで管理できるキーの種類と用途

また、暗号キーは２種・２用途に細かく分けられている。


KMSで管理できるキーには、単一の暗号化キーを使うSymmetric、秘密鍵と公開鍵を使うAsymmetricの２種がある。それぞれ1)データの暗号化・複合 2)改ざん検知 に用いるので、２×２で４つの組み合わせがある。

1. Symmetric（共通鍵暗号方式）
   - Encrypt and decrypt（暗号化・複合）
   - Generate and verify MAC(生成と検証)
2. Asymmetric（公開鍵暗号方式）
   - Encrypt and decrypt（暗号化・複合）
   - Sign and verify（署名と検証）

Asymmetricのほうは公開鍵ももちろん取得できる。こんな感じのテキストデータである。


    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhFAAOCAQ8AMIIBCkiG9w0BAQEgKCAQEAjQt/KIm5oEDQqy0pqzww
    uaToJDAe1QPi45tD9D1+bzr0FSPo5LUrjEBlQ0gztLLFSibr10IEi9p0+QaNqEE7
    8k9iTw/fWtHJpp+6z4gSq/rpARNkZSjZLXLdpAZlBNyjx9H8x8eKKEg0hZXkSiZR
    piYEcsCVm1ikh4LHwXfeit7z6X2WTmQzeRjjS1Xj1qne22oBZb3Ar8KIq5a3xnVp
    WAqPIAMqb1J9lawPg6QTP8SFd5PC9gbrwP6T+NRmUtY5Q5TQ/zHcGg0PXgqa/NjX
    Eq4a5bYmPit4o4+WFaJXJBrO32DW35gcuhIKB0Ulnp7Lagkyb8CWZM8MswYV80ii
    /QIDAQAB
    -----END PUBLIC KEY-----

なお言うまでもなくダミーであり、私はこの公開鍵を用いていない:-)

# 暗号化と複合化はどのタイミングで行う？

AWSで使う場合、マネージドサービスが使うサーバーサイド暗号化と、自分たち利用者側で勝手に行うクライアントサイド暗号化がある。前者はKMSのキーを構築時に指定すれば透過的に使える一方で、後者は自らアプリケーションの中で処理を行う必要がある。

もちろんどちらもフリーランチではなく、負荷が増す。そのため数年前まで、クライアントサイド暗号化はもちろん、サーバーサイド暗号化も、意識の高い現場（もしくは業務上より高いセキュリティが必要とされる業務に携わる現場）でもないと割合省略されがちだったと思うが、昨今ではむしろ行って当然のものに変わりつつある印象である。これまでよりもKMSの重要性は高まっていると考えるべきだろう。


# 運用上の注意点は？

鍵の漏洩と消失が起こると**悲惨**なことになる。漏洩するとクラッカーが複合も改竄もできるようになってしまいうる。消失すると、そのキーを使っていたデータは使うことができなくなる。

従って、漏洩させないよう管理を厳にするとともに（最小権限の原則を実現するためのKMSでのアクセス制御）、漏洩しても被害を限定し（KMSのローテーション機能や異常検知の仕組みの整備）、かつトレーサビリティを確保すべく操作ログも残さないといけない（CloudTrailによる証跡の保存と、S3のオブジェクトロックやMFA deleteによる保護）。

また、うっかりミスで削除してサービスが復旧不能（本当にありえる！）にならない仕組みもいる。[削除予定の鍵が使われたら通知する](https://dev.classmethod.jp/articles/trigger-alarm-when-disabled-kms-key-is-used/)仕組みがこれにあたる。


# AWS CloudHSM 

CloudHSM というものもある。KMSでも歯が立たないほど際立って厳しいセキュリティ要件に対応するためのもの。

専用ハードウェアで処理を行うため大変堅牢なのだとか。ただし、それだけに[お高い](https://aws.amazon.com/jp/cloudhsm/pricing/)。


# 参考

- [要点整理から攻略する『AWS認定 セキュリティ-専門知識』](https://amzn.to/3HNguZ0)
