# 练习用python操作MySQL数据库
import pymysql
# 连接数据库
try:
    db = pymysql.connect(host='127.0.0.1',user='root',passwd='your password',db='news',port=3306,charset='utf8')
    # 检验数据库是否连接成功
    cursor = db.cursor()
    # 这个是执行sql语句，返回的是影响的条数
    data = cursor.execute('SELECT * FROM `new`')
    # 得到一条数据
    one = cursor.fetchone()
    print(data)
    print(one)
except pymysql.Error as e:
    print(e)
    print('操作数据库失败')
finally:
    # 如果连接成功就要关闭数据库
    if db:
        db.close()
