import os
import requests
import yaml
from datetime import datetime

DOMAIN = "good-one.hatenablog.com"

with open(os.path.expanduser("~/.config/blogsync/config.yaml"), "r") as yml:
    config = yaml.safe_load(yml)

HATENA_ID = config[DOMAIN]["username"]
API_KEY = config[DOMAIN]["password"]

URL = f"https://blog.hatena.ne.jp/{HATENA_ID}/{DOMAIN}/atom/entry"


updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
custom_url = "test/path"

xml = f"""<?xml version="1.0" encoding="utf-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:app="http://www.w3.org/2007/app" xmlns:opt="http://www.hatena.ne.jp/info/xmlns#hatenablog">
    <title>DUMMY TITLE</title><author><name>name</name></author><content type="text/markdown">DUMMY CONTENT</content>
    <updated>{updated}</updated><app:control><app:draft>yes</app:draft></app:control><opt:custom-url>{custom_url}</opt:custom-url></entry>"""

r = requests.post(URL, auth=(HATENA_ID, API_KEY), data=xml)

print(r)
