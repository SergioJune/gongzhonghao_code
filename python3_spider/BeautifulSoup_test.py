#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'bs库的详解'

__author__ = 'sergiojune'

from bs4 import BeautifulSoup
import requests

response = requests.get('https://book.douban.com/').text
# print(response)
# 创建bs对象
soup = BeautifulSoup(response, 'lxml')
# 获取标签
print(soup.li)  # 这个只是获取第一个li标签
# 获取标签名字
print(soup.li.name)
# 获取标签内容
print(soup.ul.string)  # 这个只能是这个标签没有子标签才能正确获取，否则会返回None
# 获取标签属性
print(soup.li['class'])  # 第一种
print(soup.div.attrs['id'])  # 第二种

# 获取标签内的标签
print(soup.li.a)
print(soup.li.a.string)  # 这个标签没有子标签所以可以获取到内容

# 获取子节点
print(soup.div.contents)  # 返回一个列表 第一种方法
for n, tag in enumerate(soup.div.contents):
    print(n, tag)

# 第二种方法
print(soup.div.children)  # 返回的是一个迭代器
for n, tag in enumerate(soup.div.children):
    print(n, tag)

# 获取标签的子孙节点
print(soup.div.descendants)  # 返回的是一个迭代器
for n, tag in enumerate(soup.div.descendants):
    print(n, tag)

# 获取父节点
print(soup.li.parent)  # 返回整个父节点
# 获取祖先节点
print(soup.li.parents)  # 返回的是一个生成器
for n, tag in enumerate(soup.li.parents):
    print(n, tag)

# 获取兄弟节点
print(soup.li.next_siblings)  # 获取该标签的所有同级节点，不包括本身  返回的是一个生成器
for x in soup.li.next_siblings:
    print(x)

print(soup.li.previous_siblings)  # 获取兄弟节点的下一个节点


# 使用find_all()来进行筛选标签
# 参数分别为name,attrs,recursive,text,**kwargs
# 先使用name参数
print(soup.find_all('li'))  # 返回一个列表，所有的li标签名字
# 使用name和attrs参数
soup.find_all('div', {'class': 'more-meta'})  # 这个对上个进行了筛选,属性参数填的是一个字典类型的
# 对相关属性进行进行查找也可以这样
print(soup.find_all(class_='more-meta'))  # 使用关键字参数，因为class是python关键字，所以关键字参数时需要加多一个下划线来进行区别
# find()方法，和find_all()差不多，只是这个方法只是返回一个标签
print(soup.find('li'))
print(soup.find(class_='more-meta'))

# 还可以用标签选择器来进行筛选元素, 返回的都是一个列表
print(soup.select('ul li div'))  # 这个是根据标签名进行筛选
print(soup.select('.info .title'))  # 这个是根据class来进行筛选
print(soup.select('#footer #icp'))  # 这个是根据id来进行筛选
# 上面的可以进行混合使用
print(soup.select('ul li .cover a img'))
# 获取属性
for attr in soup.select('ul li .cover a img'):
    # print(attr.attrs['alt'])
    # 也可以这样
    print(attr['alt'])

# 获取标签的内容
for tag in soup.select('li'):
    print(tag.get_text())  # 里面可以包含子标签，会将子标签的内容连同输出

