#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'练习requests库的用法'

__author__ = 'sergiojune'

import requests
from requests.exceptions import ReadTimeout, ConnectTimeout, HTTPError, ConnectionError, RequestException
from requests.auth import HTTPBasicAuth

# 发送请求
response = requests.get('http://httpbin.org/get')
print(response.text)
# 请求头
print(response.headers)
# 请求状态码
print(response.status_code)

# 还可以添加请求头进行请求
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
response = requests.get('http://httpbin.org/get')
print(response.headers)
print(response.text)

# 进行带参数的post请求
data = {'name': 'june', 'password': 123456}
response = requests.get('http://httpbin.org/get', params=data)
print(response.text)

# 进行post请求
data = {'name': 'june', 'password': 123456}
response = requests.post('http://httpbin.org/post', data=data, headers=headers)
print(response.text)

# 还可以进行put，delete请求等。

# 解析json
j = response.json()  # 可以用json库来解析，结果一样
print(type(j), j)

# 从网上读取二进制数据，比如图片
response = requests.get('https://www.baidu.com/img/bd_logo1.png', headers=headers)
# 这个是直接获取字节码
print(response.content)
# 这个是获取解码后的返回内容
print(response.text)
# 用文件来把图片下载下来
with open('baidu.png', 'wb') as f:
    f.write(response.content)
    print('下载完毕')

print(response.cookies)  # 获取cookie
print(response.status_code)  # 获取请求状态码
print(response.url)  # 获取请求的url
print(response.headers)  # 获取请求头

print(requests.codes.ok)  # 请求成功的状态码

# 上传文件
files = {'picture': open('baidu.png', 'rb')}
response = requests.post('http://httpbin.org/post', files=files)
print(response.text)

# 获取cookie
response = requests.get('https://www.baidu.com')
for k, v in response.cookies.items():
    print(k, '=', v)

# 用会话来保持登陆信息
session = requests.session()
response = session.get('http://httpbin.org/cookies/set/number/123456')
print(response.text)

# 证书验证
response = requests.get('https://www.12306.cn', verify=False)  # 不加这个关键字参数的话会出现验证错误问题，因为这个网站的协议不被信任
print(response.status_code)  # 看到结果会出现一个警告，解决是在请求时加个cert关键字参数，里面放的是可信任证书就可以了

# 设置代理
proxies = {'http': 'http://122.114.31.177:808',
           'https': 'https://119.28.223.103:8088'}
# 在请求时添加上列代理
response = requests.get('http://httpbin.org/get', proxies=proxies)
print(response.text)

# 超时设置
try:
    response = requests.get('http://httpbin.org/get', timeout=0.5)  # 规定时间内未响应就抛出异常
    print(response.text)
except ReadTimeout as e:
    print('请求超时')
except ConnectTimeout as e:
    print('连接失败')

# 设置认证
# requests.get('需要认证的网址', auth=HTTPBasicAuth('user', 'passwd'))  # 由于找不到需要认证的网址，所以先写个主体
# 还可以这样认证
# requests.get('需要认证的网址', auth=('user', 'passwd'))  # 这样就简单点

# 捕捉异常
try:
    response = requests.get('http://httpbin.org/get', timeout=0.1)  # 规定时间内未响应就抛出异常
    print(response.text)
except ReadTimeout as e:
    print('请求超时')
except ConnectionError as e:
    print('连接失败')
except RequestException as e:
    print('请求失败')
