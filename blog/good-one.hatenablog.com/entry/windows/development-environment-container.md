---
Title: Windows+Python+Lambda+Dockerで開発環境づくり
Category:
- Windows
- Lambda
- Python
- Container
Date: 2022-10-11T19:23:23+09:00
URL: https://blog.tricrow.com/entry/windows/development-environment-container
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889926544671
---

過去にWindows直でPythonをインストールして開発環境を作成した。用途はAWS Lambdaの関数作成である。

おおむね問題なかったのだが、[ローカルの環境変数を読み込ませるいい方法がなく](https://rinoguchi.net/2019/10/python-environment-variables.html)、結局コンテナ上でdirenvを使うことにした。どの道AWS LambdaはLinux上で動かすわけなので、Windows上での開発は補助的なものとして扱うのが適切なのでは、と気づいたこともある。これ自体はよい気付きであったと思う。Windowsで開発環境を作る前に気づければもっとよかったのだが。

[:contents]

# やりたいこと

以下の流れで開発を行いたい。

1. ホストのWindowsのVSCodeを使ってソースコードを編集する。
2. ホストのWindowsからDocker上のPythonコンテナにpythonスクリプト群を同期する。
      - マウントするだけだが。
      - Lambda用想定なので専用のものを利用。
3. デバッグ/実行をコンテナ上で実行する。
      - 逐一SSHで入らないといけないのは開発効率を落とすので、VSCodeの拡張機能のRemote Developmentを導入して手早く行えるようにしたい。

1はもうできているので、2と3を行えばよい。

      Windows(VSCode) C:\MyFile\GitHub\my-lambda-functions\develop_send_mail
                  　　　　　　　　　　　　　　　　↓ マウント
      Container(amazon/aws-lambda-python) /app/my-lambda-functions\develop_send_mail

2のコンテナ起動用ファイルの作成と、VSCodeのRemote Developmentの設定がやや大変か。

なおボリュームのマウントにはオーバーヘッドがそこそこある。だから数千を超えるような数のファイルをマウントするとパフォーマンスの問題を引き起こすおそれがあるわけだが、幸いというか今回の対象ファイル数は微々たるものである。というわけで心置きなくマウントする。


# コンテナ起動用ファイルの作成

## docker-compose.yml

docker-composeで起動したいため、docker-compose.ymlから作成。内容は下記。


      version: "3.9"
      services:
      python:
         container_name: aws-lambda-python
         build: ./containers/aws-lambda-python3.9
         tty: true
         volumes:
            - ./src:/lambda
            - ~/.aws:/root/.aws

- ソースコードとAWSのクレデンシャルを同期させている。うっかりミスでアクセスキーをgit上に公開してしまっては目も当てられないため、アクセスキーは.envrcにも記載しない。いくら.gitignoreで除外すると言っても危ないものは危ない。
  - 本当はコンテナにアクセスキーを持たせるのも嫌なのだが、これはもうしょうがないと割り切った。ただ、業務だとIAMの管理やアクセスキーの管理がややこしくなるので、最初から開発用のEC2やLambdaを使ってください、の方向に振り切ってしまうかも。AWSリソース依存の部分のテストはLambdaを直接叩いて結合テストでカバーする方向。
- コンテナ名は固定しておいたほうが安定する。あとでリモート開発用のキーとしても使うためだ。


## Dockerfile

Dockerfileは下記のようになる。direnv, aws cli, python用モジュールをインストールしているくらいで、ことさら説明が必要な部分はないはず。

      FROM amazon/aws-lambda-python:3.9

      RUN yum update -y
      RUN yum install -y git go make unzip tar
      RUN git clone https://github.com/direnv/direnv && cd direnv && make install && cd ..
      RUN echo 'eval "$(direnv hook bash)"' >> /root/.bashrc && source /root/.bashrc
      RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
      RUN pip install cerberus email_validator boto3 pytest pytest-cov  pytest-mock
      CMD ["/bin/bash"]

# VSCodeのRemote Developmentの設定

## Install

拡張機能からRemote Developmentをインストールするだけ。

## .devcontainer/devcontainer.jsonの用意。

手動でRemote Development用の設定ファイルを作成する。.devcontainerディレクトリもないので作る。devcontainer.jsonを下記の内容で作成。
[こちら](https://dev.classmethod.jp/articles/add-vs-code-remote-development-settings-to-existing-docker-environment/)が参考になるので見ると吉。

      {
         "name": "aws-lambda-python",
         "dockerComposeFile": [
            "../docker-compose.yml"
         ],
         "service": "python",
         "workspaceFolder": "/lambda"
      }

成功すると、VSCodeの左側のアイコンにリモートエクスプローラーが表示される。そこからコンテナを選んで"Open Folder in Container"で入れる。最初は"Attach to Container"が必要。


# 所感

大変便利に使える予感。リモート開発だとターミナルもVSCodeから普通に使えるため、開発用途ならAWS CLIをシェルスクリプトで叩いて自動アップロードするようにしたほうがAWS Toolkitよりも案外ラクかもしれない。頻繁に何度も行うなら、という条件は付くけれども。

めったに行わないならシェルスクリプトをわざわざ用意するのも手間なので、AWS Toolkitで簡易に行ったほうが多分ラク。

# 参考

- https://dev.classmethod.jp/articles/add-vs-code-remote-development-settings-to-existing-docker-environment/
- https://qiita.com/kompiro/items/5fc46089247a56243a62
