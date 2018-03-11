#!/usr/bin/env python 3
# -*- coding:utf-8 -*-

'练习urllib库的用法'

__author__ = 'sergiojune'

from urllib import request, parse, error
from http import cookiejar

# 请求获取网页返回内容
response = request.urlopen('https://movie.douban.com/')
# 获取网页返回内容
print(response.read().decode('utf-8'))
# 获取状态码
print(response.status)
# 获取请求头
print(response.getheaders())
for k, v in response.getheaders():
    print(k, '=', v)

# 获取对应参数的请求头
print(response.getheader('Vary'))

print('-------------------')

# 使用Requests对象来实现复杂一点的请求
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
requests = request.Request('https://movie.douban.com/', headers=headers)  # 加入自己的请求头更加接近浏览器
# 进行请求,把Request对象传入urlopen参数中
response = request.urlopen(requests)
print(response.read().decode('utf-8'))

# 使用post方法来进行模拟登陆豆瓣
data = {'source': 'None',
        'redir': 'https://www.douban.com/',
        'form_email': 'user',
        'form_password': 'passwd',
        'remember': 'on',
        'login': '登录'}
# 将data的字典类型转换为get请求方式
data = bytes(parse.urlencode(data), encoding='utf-8')
requests = request.Request('https://accounts.douban.com/login', headers=headers, data=data, method='POST')
response = request.urlopen(requests)
print(response.read().decode('utf-8'))

# 另外一种添加单个请求头Request.add_header(),参数为两个，分别为键值

# 获取cookie
cookie = cookiejar.CookieJar()
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
# 请求网页
response = opener.open('https://movie.douban.com/')
# 打印cookie
for c in cookie:
    print(c.name, '=', c.value)

# 将cookie保存在文件中
filename = 'cookie.txt'
# 表示使用Mozilla的cookie方式存储和读取
cookie = cookiejar.MozillaCookieJar(filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
opener.open('https://movie.douban.com/')
# 保存文件
cookie.save(ignore_discard=True, ignore_expires=True)

# 另外一种保存cookie为文件方法
# 表示 Set-Cookie3 文件格式存储和读取
cookie = cookiejar.LWPCookieJar(filename)
# 创建处理器
handler = request.HTTPCookieProcessor(cookie)
# 利用handler构建opener
opener = request.build_opener(handler)
opener.open('https://movie.douban.com/')
# 保存文件
cookie.save(ignore_discard=True, ignore_expires=True)

# 从cookie文件加载到网页上实现记住登陆
cookie = cookiejar.LWPCookieJar()
# 加载文件
cookie.load(filename, ignore_discard=True, ignore_expires=True)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
opener.open('https://movie.douban.com/')

# 使用代理ip
try:
    proxy = request.ProxyHandler({
        'https': 'https://106.60.34.111:80'
    })
    opener = request.build_opener(proxy)
    opener.open('https://movie.douban.com/', timeout=1)
except error.HTTPError as e:
    print(e.reason(), e.code(), e.headers())
except error.URLError as e:
    print(e.reason)

# 解析url
print(parse.urlparse('https://movie.douban.com/'))
print(parse.urlparse('https://movie.douban.com/', scheme='http'))
print(parse.urlparse('movie.douban.com/', scheme='http'))

# 将列表元素拼接成url
url = ['http', 'www', 'baidu', 'com', 'dfdf', 'eddffa']  # 这里至少需要6个元素（我乱写的，请忽视）
print(parse.urlunparse(url))

# 连接两个参数的url, 将第二个参数中缺的部分用第一个参数的补齐
print(parse.urljoin('https://movie.douban.com/', 'index'))
print(parse.urljoin('https://movie.douban.com/', 'https://accounts.douban.com/login'))

# 将字典类型转换成get类型的字符串
data = {'name': 'sergiojuue', 'sex': 'boy'}
data = parse.urlencode(data)
print('https://accounts.douban.com/login'+data)
