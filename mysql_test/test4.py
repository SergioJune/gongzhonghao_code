# 修改数据库里的内容（增加，修改某条或者删除数据）
import pymysql


class OperateSQL(object):
    def get_conn(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='your password',db='news',port=3306,charset='utf8')
        except pymysql.Error as e:
            print(e)
            print('数据库连接失败')

    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)
            print('数据库关闭失败')

    def add_one(self):
        sql = 'INSERT INTO `new`(`title`,`content`,`type`,`view_count`,`release_time`) VALUE(%s,%s,%s,%s,%s)'
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            cursor.execute(sql, ('title', 'content', 'type', '1111', '2018-02-01'))
            cursor.execute(sql, ('标题', '内容', '类型', '0000', '2018-02-01'))
            # 一定需要提交事务，要不不会显示，只会占位在数据库
            self.conn.commit()
            return 1
        except AttributeError as e:
            print('Error:', e)
            return 0
        except TypeError as e:
            print('Error:', e)
            # 发生错误还提交就是把执行正确的语句提交上去
            # self.conn.commit()
            # 下面这个方法是发生异常就全部不能提交,但语句执行成功的就会占位
            self.conn.rollback()
            return 0
        finally:
            cursor.close()
            self.close_conn()

    def update(self):
        sql= 'UPDATE `new` SET `author`=%s WHERE `title`=%s'
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            num = cursor.execute(sql, ('sergiojune', 'title'))
            # 提交事务
            self.conn.commit()
            cursor.close()
            return num
        except pymysql.Error as e:
            print(e)
            # 修改失败就回滚
            self.conn.rollback()

        finally:
            if self.conn:
                self.close_conn()

    def delete(self):
        sql = 'DELETE FROM `new` WHERE `view_count`=%s'
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            num = cursor.execute(sql, ('0',))
            self.conn.commit()
            cursor.close()
            return num
        except pymysql.Error as e:
            print('删除数据失败')
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.close_conn()


def main():
    news = OperateSQL()
    if news.delete():
        print('删除数据成功')
    else:
        print('发生异常，请检查！！！')


if __name__ == '__main__':
    main()

