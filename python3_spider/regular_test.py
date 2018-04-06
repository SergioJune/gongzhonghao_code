#!/usr/bin/env python3
# -*- coding:utf_8 -*-

'使用正则表达式来匹配豆瓣图书'

__author__ = 'sergiojune'
import re, requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
response = requests.get('https://book.douban.com/', headers=headers)
# print(response.text)
# 使用正则对象
pattern = re.compile('<li.*?cover.*?title="(.*?)".*?<p>.*?author">(.*?)</span>.*?year">(.*?)</span>.*?publisher">(.*?)</span>.*?</li>', re.S)
# 进行匹配
books = pattern.findall(response.text)
print(len(books))
for book in books:
    print('name:', book[0], 'author:', book[1].strip(), 'year', book[2].strip(), 'publisher:', book[3].strip())
