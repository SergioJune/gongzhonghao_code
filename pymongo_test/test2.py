#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'继续练习mongodb的更多用法'

author = 'sergiojunr'

from pymongo import MongoClient
from bson.objectid import ObjectId  # 根据id来查询数据需要
# 连接数据库
client = MongoClient('mongodb://localhost:27017')

db = client.students
# print(dir(db))
# print(db.name)
# # 插入一条数据
# stu = {'name': 'python', 'age': 21, 'sex': 'woman', 'grade': 453}
# db.students.insert_one(stu)
# # 插入多条数据
# stu1 = {'name':'stu1','age':19}
# stu2 = {'name':'stu2','age':16}
# stu3 = {'name':'stu3','age':14}
# result = db.students.insert_many([stu1,stu2,stu3])
# print(result)

# 查询数据
stu = db.students.find_one({'age':19})  # 查询一条数据，参数为查找条件
print(stu)
stus = db.students.find({'age': 16})  # 查询多条数据，返回一个Cursor对象
# 获取某个id的数据
stu = db.students.find_one({"_id": ObjectId("5ab7c4c7fc4d783e642e233d")})  # id对应的值为一个对象
print(stu)

# 修改数据库
# d = db.students.update_one({'age': 18}, {'$inc': {'age': 2}})  # 修改一条数据，第二个参数需注意
# print(d)
# d = db.students.update_many({'age': 18}, {'$inc': {'age': 2}})
# print(d.matched_count)  # 条件的匹配数
# print(d.modified_count)  # 修改的数量

# 删除数据
# d = db.students.delete_one({'age': 19})  # 删除一条数据
# print(d.deleted_count)  # 查看删除的条数
d = db.students.delete_many({'age': 20})  # 删除多条数据
print(d.deleted_count)









