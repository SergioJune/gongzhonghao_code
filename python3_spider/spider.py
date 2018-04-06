# 爬取豆瓣电影top250，并把他们的数据放在mysql数据库里面
import re,requests
import pymysql
from pymongo import MongoClient


class Spider(object):

    def __init__(self):
        self.root_pattern = '<div class="hd">([\d\D]*?)</li>'
        self.page_pattern = '<link rel="next" href="([\d\D]*?)"/>'
        self.title_pattern= '<span class="title">([\d\D]*?)</span>'
        self.other_pattern = '<span class="other">&nbsp;/&nbsp;([\d\D]*?)</span>'
        self.director_pattern = '导演:([\d\D]*?);&nbsp;&nbsp;主演'
        self.is_playable_pattern = '<span class="playable">([\d\D]*?)</span>'
        self.producer_country_pattern = '&nbsp;/&nbsp;([\u4e00-\u9fa5\s]*?)&nbsp;/&nbsp;'
        self.producer_year_pattern = '([0-9]{2,4})&nbsp;/&nbsp;'
        self.type_pattern = '&nbsp;/&nbsp;([\u4e00-\u9fa5\s]*?)</p>'
        self.score_pattern = '<span class="rating_num" property="v:average">([\d\D]*?)</span>'
        self.number_of_commnets_pattern = '<span>([\w]*?人评价)</span>'
        self.quote_pattern = '<span class="inq">([\d\D]*?)</span>'
        self.url = 'https://movie.douban.com/top250'
        self.num=1
        # 请求头信息
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)'}

    def __get_htmls(self, url):
        '''获取网页返回的htmls信息'''
        htmls = requests.get(url,headers=self.header)
        # htmls.text就是获取该网页的html结构
        return htmls.text

    def __get_one(self, htmls):
        '''利用正则表达式获取一个电影的所有数据,并且返回下一页的url'''
        # 获取每一个电影
        films = re.findall(self.root_pattern, htmls)
        # 获取下一页链接
        page = re.findall(self.page_pattern, htmls)
        #print(page)
        return films, page

    def __get_key_info(self, films):
        '''获取需要存储的数据'''
        films_list = []
        for film in films:
            # 获取每个电影的数据
            title = re.findall(self.title_pattern, film)
            other = re.findall(self.other_pattern, film)
            director = re.findall(self.director_pattern, film)
            is_playable = re.findall(self.is_playable_pattern, film)
            producer_country = re.findall(self.producer_country_pattern, film)
            producer_year = re.findall(self.producer_year_pattern, film)
            type = re.findall(self.type_pattern, film)
            score = re.findall(self.score_pattern, film)
            numbers = re.findall(self.number_of_commnets_pattern, film)
            quote = re.findall(self.quote_pattern, film)
            # 有些标题是两个的，因为有中英文
            if len(title) == 2:
                title = title[0]+title[1]
                title = title.replace('&nbsp;','')
            else:
                title = title[0]
                # 这里的类型匹配因为有些空格字符，所以用这个方法清除左右两边的空格
            if type:
                type = type[0].strip()
            # 判断是否为空
            director = director[0] if director else ''
            other = other[0] if other else ''
            is_playable = '可播放' if is_playable else '不可播放'
            producer_country = producer_country[0] if producer_country else ''
            producer_year = producer_year[0] if producer_year else ''
            score = score[0] if score else ''
            numbers = numbers[0] if numbers else ''
            quote = quote[0] if quote else ''
            # 把每个电影数据存入字典
            film_dict = {'title': title, 'other': other, 'director': director, 'is_playable': is_playable, 'producer_country': producer_country,
                         'producer_year': producer_year, 'type': type, 'score': score, 'numbers': numbers, 'quote': quote}
            # 最后把每个电影存入列表方便进行操作
            films_list.append(film_dict)
        return films_list

    def write2mongodb(self, films_list):
        '''写入mongodb数据库'''
        print('正在写入第%d页数据' % self.num)
        db = MongoClient('localhost', 27017)['films']
        db.films.insert_many(films_list)

    def write2sql(self,films_list):
        '''写入mysql数据库'''
        print('正在写入第%d页数据'%self.num)
        for film in films_list:
            db = Operate_SQL()
            db.add_data(film)



    def run(self):
        url = 'https://movie.douban.com/top250'
        '''循环取下页的电影'''
        while True:
            htmls = self.__get_htmls(self.url)
            films, page = self.__get_one(htmls)
            films_list =  self.__get_key_info(films)
            self.write2sql(films_list)
            print('   第%d页数据已完成'%self.num)
            # 判断是否存在下一页，没有时证明所有页数据已爬完
            if page:
                self.url = url + page[0]
                self.num +=1
            else:
                print('所有数据已经完成')
                break


# 操作 mysql
class Operate_SQL():
    # 连接数据库
    def __get_conn(self):
        try:
            # 我用的的本地数据库，所以host是127.0.0.1
            self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='密码',port=3306,db='douban_films top250',charset='utf8')
        except pymysql.Error as e:
            print(e, '数据库连接失败')

    def __close_conn(self):
        '''关闭数据库连接'''
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e, '关闭数据库失败')

    def add_data(self,film):
        '''增加一条数据到数据库'''
        sql = 'INSERT INTO `films`(`title`,`other`,`director`,`is_playable`,`producer_country`,' \
              '`producer_year`,`type`,`score`,`numbers`,`quote`) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.__get_conn()
            cursor = self.conn.cursor()
            cursor.execute(sql, (film['title'],film['other'],film['director'],film['is_playable'],film['producer_country'],
                                 film['producer_year'],film['type'],film['score'],film['numbers'],film['quote'],))
            self.conn.commit()
            return 1
        except AttributeError as e:
            print(e,'添加数据失败')
            # 添加失败就倒回数据
            self.conn.rollback()
            return 0
        except pymysql.DataError as e:
            print(e)
            self.conn.rollback()
            return 0
        finally:
            if cursor:
                cursor.close()
            self.__close_conn()

    def select(self):
        '''查询数据'''
        sql = 'SELECT `title`,`type`,`id` FROM `films` ORDER BY `producer_year` LIMIT 5,20'
        try:
            self.__get_conn()
            cursor = self.conn.cursor()
            films = cursor.execute(sql)
            return cursor.fetchall()
        except AttributeError as e:
            return None
            print(e,'查询数据失败')
        finally:
            if cursor:
                cursor.close()
            self.__close_conn()


def main():
    # spider = Spider()
    # spider.run()
    db = Operate_SQL()
    films = db.select()
    if films:
        num = 1
        for film in films:
            print('{3}  id:{2}  title:{0} -> type:{1}'.format(film[0],film[1],film[2],num))
            num += 1
    else:
        print('data exist')

if __name__ == '__main__':
    main()