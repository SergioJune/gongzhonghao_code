import pymysql
try:
    conn = pymysql.connect(host='127.0.0.1',user='root',passwd='your password',db='news',charset='utf8',port=3306)
    # 这个是光标，用来操作数据库语句
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute('SELECT * FROM `new`')
    print(cursor.fetchone())
    # print(dir(cursor))
    print(cursor.description)
    # print(cursor.fetchall())
    # 关闭光标
    cursor.close()
except pymysql.Error as e:
    print(e)
    print('操作数据库失败')
finally:
    if conn:
        conn.close()

# 将一条数据转成字典方便查找
new = dict(zip([x[0] for x in cursor.description],[x for x in cursor.fetchone()]))
print(new)

print(new['title'])
# 将多条数据转成字典类型
print('-----------')
def new2dict(new):
    return dict(zip([x[0] for x in cursor.description],[x for x in new]))
news_list = list(map(new2dict,cursor.fetchall()))
print(news_list)
# 把上面的第一条数据插进去这个列表
news_list.insert(0,new)
print(news_list)
# 查询某一条数据
print(news_list[9]['type'],news_list[9]['title'])








