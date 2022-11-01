---
Title: MUIを使って個人サイトをリニューアル
Category:
- frontend
Date: 2022-11-01T13:34:00+09:00
URL: https://blog.tricrow.com/entry/aws/frontend/mui-template
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889932698506
---

Next.jsで個人サイトをリニューアルするにあたり、[MUIのテンプレート](https://mui.com/)がFreeかつ便利そうであったため、これを採用することにした。WEBデザインまでは手が回らない自分にとり、テンプレートはありがたい存在である。自前で一からデザインするより早いし高クオリティなのだから使わない手はない。

[:contents]

# とにもかくにも動作させるまで

1. 使うのは[ここ](https://github.com/mui/material-ui/tree/master/docs/src/pages/premium-themes/onepirate)。
2. そこでgitから一度まとめてダウンロードし、該当のディレクトリをNext.jsのプロジェクト内にあるpagesに*.tsxだけコピーする。
3. ライブラリをインストール

    npm install @mui/material @emotion/react @emotion/styled @mui/icons-material react-final-form

4. `npm run dev`で起動し、初期ページに手打ちで飛ぶと、無事画面が表示される。画像のリンク切れが発生しているが、これは修正前なのである意味当然。

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/g/good-one/20221031/20221031125747.png" alt="20221031125747">


# 修正

## 不要な部品を削除

自分の場合コンテンツはブログメインで行くつもりなので、個人サイトはリンクと問い合わせフォームがあればひとまず事足りる。

というわけで、index.tsxを残し、後は全て部品も含めて削除する。

## コードを追加・修正

問い合わせフォームを追加するとともに、個人用サイトに合わせてindex.tsxおよびその部品も修正。

細かい内容は逐一書いているとキリがないので省略するが、モノは[こちら](https://github.com/nakatatsu/personal-website)に置く予定。

# 参考

- https://amateur-engineer.com/react-material-ui/
