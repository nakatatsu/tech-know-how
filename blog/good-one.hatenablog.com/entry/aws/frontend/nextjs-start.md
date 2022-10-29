---
Title: Next.jsをインストールして動かしてみる。(Windows)
Category:
- frontend
Date: 2022-10-29T21:30:40+09:00
URL: https://blog.tricrow.com/entry/aws/frontend/nextjs-start
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889931905321
---

[:contents]


# やったこと

手順は[こちら](https://nextjs.org/docs)にある。
 
- https://nodejs.org/en/ からNode.jsをDownloadしてインストール
- `npx create-next-app@latest --typescript`と打ち、対話式でプロジェクト名を聞かれるため入力。今回はpersonal-website。
  - typescriptを使いたいので、`--typescript`をつける。
  - ディレクトリ名がpersonal-websiteで作られたが、srcにリネーム。
- `cd src`してから`npm run dev`。

これだけで初期画面を表示させられた。意外に簡単。

<img src="https://cdn-ak.f.st-hatena.com/images/fotolife/g/good-one/20221029/20221029211513.png" alt="20221029211513">
