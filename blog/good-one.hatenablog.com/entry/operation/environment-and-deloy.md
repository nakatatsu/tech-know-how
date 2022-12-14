---
Title: 本番環境へのデプロイはどう行うべきなのか？
Category:
- DevOps
- デプロイ
Date: 2022-11-04T22:48:41+09:00
URL: https://blog.tricrow.com/entry/operation/environment-and-deloy
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889933734599
---

ITサービスの開発・運用を行うにあたって避けて通れないのがデプロイである。プロジェクトのたびに一から考えると（そしてドキュメント化するのも）手間がかかるので、よくある方針や例を記しておく。


[:contents]

# 方針

1. 手順をなるべく自動化して手作業は最小限にできる
  - 効率化
  - オペミスの防止
    - 手動の作業はミスがつきものなので
2. 環境間で動作を合わせられる
  - 違っていると不具合や事故の元なので。
3. ロールバックに対応できる
  - デプロイした内容にバグが見つかるのはザラ。とりあえず切り戻しができれば被害は最小限になる。
    - できなかったらHotfixとかで直すまでサービスダウンまであり得る。怖すぎ。
  - 問題はＤＢのスキーマなど、別に依存がある場合。互換性があればいいが、ないとロールバックは無理。
    - マイグレーションすればいい、という考え方もあるが、本番のDBスキーマにデグレードをかけるのは往々にして無理筋。
    - あと分散モノリシックな造りだと、API同士のバージョンに互換性が必要だったりもするのでさらにツライ。
4. ダウンタイムを極力短くできる。できればゼロ。
  - ダウンタイム＝逸失利益なので、これは当然。
    - ただしゼロといっても厳密には0ミリ秒はありえなくて、ごくわずかな時間繋がらなくなっているはずだが、リトライするなどして認識されないため、ゼロダウンタイム（と思ってもらえる）。
5. 事前にアプリケーションの動作確認、テストを行える
    - 本番環境で動作確認はなかなか無理がある。
6. デプロイのログが残る。何かあったら通知が出る。
    - 不測の事態が起きた際、ログがなかったらお手上げ。通知もないと気づけない。

# それぞれどう実現すればいいか？

- 自動化
  - CI/CDツールを使う。CodePipelineやGitHub Actionsなど。
- 環境間での動作の統一
  - できるだけ同じスクリプトで動作させればよい。環境間の違いはなるべくパラメータでカバー。
- ロールバックへの対応
  - ECSを使えるならタスクを戻すだけ。
  - EC2に直でデプロイしている場合はシンボリックリンクなどで切り替える。
  - Lambdaを使っているならエイリアスに紐づいたバージョンを戻す。ただし呼び出す際にエイリアス付きで呼び出している必要あり。
  - CloudFront+S3の構成は難しい。どうしてもとあらば[Lambda@Edgeを使う方法](https://foghornconsulting.com/2022/04/15/blue-green-websites-on-s3-with-cloudfront/)のようにS3の前に切り替える仕掛けを仕込むことになるはず。
    - とはいえ大がかりすぎてコストやオーバーヘッドが気にかかる。前回のデプロイ時のファイル群をs3 syncで戻すくらいが落としどころか。運用でカバーである。
- ダウンタイムの極小化
  - 切り替え式のデプロイを行っていれば切り替えにかかる時間だけとなる。
    - それが難しいCloudFront＋S3だと上書きになってしまう。一瞬表示が崩れるなどのことは覚悟せざるを得ないかもしれない。
  - ただしAuroraのアップデートなどがあると専用の大がかりな仕掛けが必要になるはず。
- 事前の動作確認 
  - 環境を分ける。いわゆるstagingやpreと名のつく環境を本番と同じ設定で用意。
- デプロイのログが残る。何かあったら通知が出る。
  - ECSのように元からログの記録とセットのものを使う。そういうものがなければ、デプロイスクリプトの中で自らログを残す。通知も同様、既製品の中にあればそれを使い、なければ自前でセット。

# 構成例

## 環境の分離

 - 本番環境(product)
 - テスト環境(staging)

## デプロイフロー　backend(ECSの場合)

1. 複数の環境用設定(e.g. product.env, staging.env)を格納したコンテナイメージを作成。
2. それをstaging環境で起動して確認。
3. 同じソースコードからコンテナイメージを作り直してproduct環境にデプロイ。
   - 環境の差は環境変数で表現する。

※ 上記はCI/CDで実行する。Github Actionsとか。

## デプロイフロー　backend(API Gateway + Lambdaの場合)

1. staging環境にデプロイして動作を確認
2. 問題なければ同じソースコードからproduct環境にデプロイ。
   - こちらも環境の差は環境変数で表現する。

### 余談：昔話

クラウドがまだ流行していないオンプレの時代は上書き式のデプロイがよく見られた。Dockerはまだ実用に耐える技術として普及しておらず、AWSのように切り替えるポイントがいくつもあるわけでなく、またサーバー自体も気軽に増減などさせられなかったから、ある意味最適でもあった。下手するとバージョン管理システムが使われていないプロジェクトもあったくいらいで、バージョン管理システムとデプロイツールの連携どころではなかった。今から思うと凄い時代である。その時代はstaging->productで同期させるのが堅いやり方だった。が、2022年現在、gitも普及している上、CI/CDのツールも豊富である。当時のノウハウはもう余程のことがなければお蔵入りさせてよさそうだ。


## デプロイフロー　frontend(Cloudfront + S3)

1. staging環境にデプロイして動作を確認
2. 問題なければ同じソースコードからproduct環境にデプロイ。
   - こちらも環境の差は環境変数で表現する。
