#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'练习用python操作mongodb数据库'

author = "sergiojune"
from pymongo import MongoClient

# 连接数据库(连接之前需要先打开mongodb数据库)
# client = MongoClient()  # 最简单的连接
# client = MongoClient('loaclhost', 270171)  # 指定端口和数据库地址进行连接
client = MongoClient('mongodb://localhost:27017')  # 使用url地址进行连接
print(dir(client))
print(client.get_database('students'))
db = client['films']
print(db)
# 关闭连接
client.close()
