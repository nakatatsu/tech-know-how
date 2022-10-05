import os
import re
import sys
from datetime import datetime
from xml.sax.saxutils import escape

import frontmatter
import requests
import yaml
from jinja2 import Environment, FileSystemLoader

""" はてなブログへ新規投稿する
コマンド: python post.py [ファイルパス]
e.g. python post.py /posts/entry/general/git-hatena2.md

その後に blogsync pull good-one.hatenablog.com もしたほうが良い。
"""


class Post:
    def __init__(
        self, title: str, name: str, categories: list, content: str, draft: bool, updated: datetime, custom_url: str
    ):
        self.__title = title
        self.__name = name
        self.__categories = categories
        self.__content = content
        self.__updated = updated
        self.__draft = draft
        self.__custom_url = custom_url

    @property
    def title(self) -> str:
        return self.__title

    @property
    def name(self) -> str:
        return self.__name

    @property
    def categories(self) -> str:
        return self.__categories

    @property
    def content(self) -> str:
        return self.__content

    @property
    def draft(self) -> bool:
        return self.__draft

    @property
    def updated(self) -> datetime:
        return self.__updated

    @property
    def custom_url(self) -> str:
        return self.__custom_url


def send_hatena(hatena_id: str, blog_id: str, api_key: str, data: str) -> str:
    URL = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry"
    return requests.post(URL, auth=(hatena_id, api_key), data=data.encode("utf-8"))


# in & check
post_path = sys.argv[1]
if not os.path.isfile(post_path):
    raise ValueError("file not exists.")

# config
blog_id = "good-one.hatenablog.com"
with open(os.path.expanduser("~/.config/blogsync/config.yaml"), "r") as config_text:
    config = yaml.safe_load(config_text)

# logic
with open(post_path, "r", encoding="utf-8") as post_text:
    parsed_post = frontmatter.load(post_text)

# パース結果の簡易チェック
if not len(parsed_post["Title"]) > 0:
    raise ValueError("parsed_post is incorrect.")

#  Postインスタンスを生成
m = re.match(r"^.*/entry/(.*).md$", post_path.replace("\\", "/"))
if m is None:
    raise ValueError("file path is incorrect.")

draft = parsed_post["Draft"] if "Draft" in parsed_post else False
categories = parsed_post["Category"] if "Category" in parsed_post else []

new_post = Post(
    parsed_post["Title"],
    config[blog_id]["username"],
    parsed_post["Category"],
    escape(parsed_post.content),
    draft,
    datetime.now(),
    m.group(1),
)

#  レンダリング
template = Environment(loader=FileSystemLoader(os.path.dirname(__file__), encoding="utf8")).get_template("post.j2")

rendered = template.render(post=new_post)

#  投稿
response = send_hatena(config[blog_id]["username"], blog_id, config[blog_id]["password"], rendered)

# output
print(response)
