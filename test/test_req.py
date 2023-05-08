import os

import requests

url = "https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%B8%95%E5%BA%95%E4%BA%9A%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89"
r = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
})
r.encoding = "UTF-8"
if not os.path.exists("html"):
    os.mkdir("html")
with open("html/main.html", mode="w+", encoding="utf8") as f:
    f.write(r.text)
