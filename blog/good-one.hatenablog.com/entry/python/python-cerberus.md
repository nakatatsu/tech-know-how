---
Title: CerberusでValidationを行う
Category:
- Python
- Cerberus
- Validation
Date: 2022-10-07T18:18:22+09:00
URL: https://blog.tricrow.com/entry/python/python-cerberus
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889925346975
---

PythonスクリプトのバリデーションをCerberusで行ってみる。

[:contents]


# Cerberus

## Install
 
    pip install cerberus

## Example


    schema = {
        "name": {
            "type": "string",
            "required": True,
        },
    }

    request_body = {
        "name": "me",
    }

    v = Validator(schema)
    v.allow_unknown = True

    # バリデーション実行
    if not v.validate(request_body):
        # エラー理由
        print(v.errors)

    print("Success")

# 使用感

よくあるValidatorとして普通に使える。

メールアドレスのチェックがデフォルトで入っていないのは驚いたが、拡張は容易なのでそこまで問題にならないのではないか。

小さなスクリプトでも大きなプロジェクトでも普通に使えそうでかなり好印象。

# 参考

- https://docs.python-cerberus.org/en/stable/
- https://qiita.com/iisaka51/items/7eea371c166780e8a56b
