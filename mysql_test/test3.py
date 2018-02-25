# 用面向对象的方法来进行操作数据库，对MySQL数据库的内容进行查询
import pymysql
class MysqlSearch(object):
    def get_conn(self):
        '''连接mysql数据库'''
        try:
            self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='your password',port=3306,charset='utf8',db='news')
        except pymysql.Error as e:
            print(e)
            print('连接数据库失败')

    def close_conn(self):
        '''关闭数据库'''
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)
            print('关闭数据库失败')

    def get_one(self):
        '''查询一条数据'''
        try:
            # 这个是连接数据库
            self.get_conn()
            # 查询语句
            sql = 'SELECT * FROM `new` WHERE `type`=%s'
            # 这个光标用来执行sql语句
            cursor = self.conn.cursor()
            cursor.execute(sql,('英超',))
            new = cursor.fetchone()
            # 返回一个字典，让用户可以按数据类型来获取数据
            new_dict = dict(zip([x[0] for x in cursor.description],new))
            # 关闭cursor
            cursor.close()
            self.close_conn()
            return new_dict
        except AttributeError as e:
            print(e)
            return None
    def get_all(self):
        '''获取所有结果'''
        sql = 'SELECT * FROM `new` '
        self.get_conn()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            news = cursor.fetchall()
            # 将数据转为字典，让用户根据键来查数据
            # news_list =list(map(lambda x:dict(zip([x[0] for x in cursor.description],[d for d in x])),news))
            # 这样也行,连续用两个列表生成式
            news_list = [dict(zip([x[0] for x in cursor.description],row)) for row in news]
            cursor.close()
            self.close_conn()
            return news_list
        except AttributeError as e:
            print(e)
            return None

    def get_more(self,page,page_size):
        '''查多少页的多少条数据'''
        offset = (page-1)*page_size
        sql = 'SELECT * FROM `new` LIMIT %s,%s'
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            cursor.execute(sql,(offset,page_size,))
            news = [dict(zip([x[0] for x in cursor.description],new)) for new in cursor.fetchall()]
            cursor.close()
            self.close_conn()
            return news
        except AttributeError as e:
            print(e)
            return None

def main():
    # 获取一条数据
    # news = MysqlSearch()
    # new = news.get_one()
    # if new:
    #     print(new)
    # else:
    #     print('操作失败')

    # 获取多条数据
    # news = MysqlSearch()
    # rest = news.get_all()
    # if rest:
    #     print(rest)
    #     print(rest[7]['type'],rest[7]['title'])
    #     print('类型：{0},标题：{1}'.format(rest[12]['type'],rest[12]['title']))
    #     for row in rest:
    #         print(row)
    # else:
    #     print('没有获取到数据')

    #获取某页的数据
    news = MysqlSearch()
    new = news.get_more(3,5)
    if new:
        for row in new:
            print(row)
    else:
        print('获取数据失败')

if __name__ == '__main__':
    main()