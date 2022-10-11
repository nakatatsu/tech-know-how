---
Title: pytest
Category:
- Python
- pytest
- unittest
Date: 2022-10-11T15:12:38+09:00
URL: https://blog.tricrow.com/entry/python/python-pytest
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889926483716
---

Pythonスクリプトのユニットテストをpytestで行ってみる。

pythonには最初からユニットテストを行う機能が付属しているのだが、[2021 年 Python 開発者アンケートの結果](https://lp.jetbrains.com/ja-jp/python-developers-survey-2021/)によると一番人気はpytestであるため、普及率に合わせて――普及率は正義である。大抵こなれているし、調べものもしやすい――こちらを採用した。

[:contents]


# pytest

## Install
 
    pip install pytest pytest-cov  pytest-mock

pytest-covはユニットテストのカバレッジ計測用。ユニットテストを行うならカバレッジ計測もしたくなるものなので、最初から導入しておく。

pytest-mockはモック用。これもどの道使うはずなので入れておく。

## Example

### ディレクトリ構成

ファイルが少なければ同じディレクトリでOK。

    └─develop_send_mail
        main.py
        main_test.py

[公式によれば](https://docs.pytest.org/en/7.1.x/getting-started.html#get-started) test_*.py または *_test.py のファイルを実行してくれる。



大量のファイルがあるなら、[こちらで紹介されているように](https://rinatz.github.io/python-book/ch04-07-project-structures/)ディレクトリを分けて下記のようにする。

    develop_send_mail
        └─develop_send_mail
            __init__.py
            ...
        └─tests
            __init__.py
            ...
   
元ネタは[こちら](https://docs.python-guide.org/writing/structure/#structure-of-the-repository)らしい。


### ソースコード

下記のように書く。**pytestをコマンドで呼び出す**のでテストコードのほうで表現しなくてよいらしい。


    from cerberus import Validator

    import main


    def test_is_email():
        v = Validator({"email": {"check_with": main.is_email}})
        assert v.validate({"email": "test@example.com"})
        assert not v.validate({"email": "testexample.com"})

### 実行方法

    pytest main_test.py

ファイル指定なしでもOK。

    pytest

# 参考

- https://qiita.com/kg1/items/e2fc65e4189faf50bfe6
- https://rinatz.github.io/python-book/ch08-02-pytest/
