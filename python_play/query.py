#!/usr/bin/env python
# encoding: utf-8

"""
@author: sergiojune
@contact: 2217532592@qq.com
@file: query.py
"""
import requests
import re, json
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


class Spider(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
                        }
        self.data = {
            'ScriptManager1': 'UpdatePanel1|Radio1$1',
            '__EVENTTARGET': 'Radio1$1',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': '',
            'hidtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Radio1': '1',
            'txtname': '',
            'txtpwd': '',
            'txtyzm': '',
            '__ASYNCPOST': 'true'
        }
        self.url = 'http://172.18.2.42:8000/Login.aspx'
        self.flag = 1

    def __get_value(self, html):  # 获取表单的两个参数__VIEWSTATE和__EVENTVALIDATION
        try:
            soup = BeautifulSoup(html, 'lxml')
            value = soup.select('input[type="hidden"]')
            values = [v for v in value if '/w' in str(v)]
            state = values[0]['value']
            action = values[1]['value']
            self.data['__VIEWSTATE'] = state
            self.data['__EVENTVALIDATION'] = action
        except IndexError as e:  # 证明这个不是首页，需要另外的规则
            match = re.search('__VIEWSTATE\|(.*?)\|.*?__EVENTVALIDATION\|(.*?)\|', html)
            self.data['__VIEWSTATE'] = match.group(1)
            self.data['__EVENTVALIDATION'] = match.group(2)
        except Exception as e:
            print('get_value', e)

    def __get_html(self, url=None):
        if self.flag:  # 第一次访问时需要先进行访问下网站初始化那两个验证参数
            r = self.session.post(self.url)
            self.__get_value(r.text)
            self.flag = 0
        if url:
            response = self.session.get(url, headers=self.headers)
        else:
            response = self.session.post(self.url, data=self.data, headers=self.headers)
        if '异步' in response.text:
            print('请求网页失败，请检查参数')
        elif '236|error|500|' in response.text:
            print('表单数据有误或者顺序不对')
        else:
            return response.text

    def __get_txtjz2(self, html=None):  # 获取宿舍号
        if html:
            soup = BeautifulSoup(html, 'lxml')
            apartment = soup.select('select[name="txtjz2"] option')
            apartment = [(p.text, p['value']) for p in apartment]
            for index, p in enumerate(apartment):
                print(index, '公寓：', p[0])
            while True:
                num = input('请输入你的公寓，输入左边的编号即可')
                num = re.match('\d+', num)
                if num and int(num.group()) < len(apartment):
                    num = int(num.group())
                    break
                print('请输入正确的公寓编号')
            return apartment[num][1]
        # 写捕捉异常的话会有个bug，当捕捉到异常时会返回None
        # except ValueError as e:
        #     print('请输入正确的公寓编号')
        #     self.__get_txtjz2()
        # except IndexError as e:
        #     print('不存在此公寓，请重新输入')
        #     self.__get_txtjz2()

    def __get_name(self, jz, html=None):  # 输入宿舍号
        if html:
            # 表单顺序需要改变
            self.data = {
                'ScriptManager1': 'UpdatePanel1|txtjz2',
                'hidtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Radio1': '1',
                'txtjz2': jz,
                'txtname2': '001001001001001',  # 这个初始化值可以随意，但不能为空
                'txtpwd2': '',
                'txtyzm2': '',
                '__EVENTTARGET': 'txtjz2',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': '',
                '__EVENTVALIDATION': '',
                '__ASYNCPOST': 'true'
            }
            self.__get_value(html)  # 换下参数
            html = self.__get_html()
            if html:
                soup = BeautifulSoup(html, 'lxml')
                dormitory_num = soup.select('select[name="txtname2"] option')
                dormitory_num = [(p.text, p['value']) for p in dormitory_num]
                for index, p in enumerate(dormitory_num):
                    print(index, '宿舍号：', p[0])
                self.__get_value(html)
        while True:
            num = input('请输入你的宿舍，输入左边的编号即可')
            num = re.match('\d+', num)
            if num and int(num.group()) < len(dormitory_num):
                num = int(num.group())
                break
            print('请输入正确的宿舍编号')
        return dormitory_num[num][1]
        # 这里也有bug，和上面的意义
        # except ValueError as e:
        #     print('请输入正确的宿舍编号')
        #     self.__get_name(jz, html)
        # except IndexError as e:
        #     print('不存在此宿舍，请重新输入')
        #     self.__get_name(jz, html)

    def __login(self, jz, name, password):
        self.data = {

            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.data['__VIEWSTATE'],
            '__EVENTVALIDATION': self.data['__EVENTVALIDATION'],
            'hidtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Radio1': '1',
            'txtjz2': jz,
            'txtname2': name,
            'txtpwd2': password,
            'txtyzm2': '1848',  # 这个是验证码，乱写都可以
            'Button1': '',
        }
        html = self.__get_html()
        while True:
            if '密码错误，请重新输入!' in html:
                print(self.data['txtpwd2'])
                print('密码错误')
                password = input('请输入你的密码，若为空可以按enter键跳过')
                self.data['txtpwd2'] = password
                html = self.__get_html()
            else:
                break

    # def __get_chapter(self):
    #     # 获取验证码
    #     url = 'http://172.18.2.42:8000/ValidateCode.aspx'
    #     response = requests.get(url, headers=self.headers)
    #     with open('code.jpg', 'wb') as f:
    #         f.write(response.content)
    #     image = Image.open('code.jpg')
    #     image.show()
    #     code = input('请输入验证码')
    #     return code

    def __get_detail(self):
        url = 'http://172.18.2.42:8000/PowerMonitoring/ssjkSSSJCX2.aspx'
        html = self.__get_html(url)
        match = re.findall('disabled.*?value:"([^"]+)"', html)
        dormitory = match[3]
        is_use = match[5]
        sum_ele = match[7]
        month_ele = match[8]
        balance = match[13]
        time_update = match[14]
        month_use_money = match[9]
        print('宿舍名称：{0}\n{1}\n本月用电量：{2}\n本月所用电金额：{3}\n总用电量：{4}\n余额：{5}\n数据最后更新时间：{6}\n'.format(dormitory, is_use, month_ele, month_use_money, sum_ele, balance, time_update))

    def __get_month_detail(self, name):
        url = 'http://172.18.2.42:8000/UserAccountment/AccountDetails2.aspx'
        html = self.__get_html(url)
        self.__get_value(html)
        self.data = {
            '__EVENTTARGET': 'RegionPanel2$Region1$Toolbar1$ContentPanel1$btnSelect',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.data['__VIEWSTATE'],
            '__EVENTVALIDATION': self.data['__EVENTVALIDATION'],
            'hidJZ': 'jz'+name,
            'RegionPanel2$Region1$Toolbar1$ContentPanel1$TextBox1': (datetime.now()-timedelta(days=30)).strftime('%Y-%m-%d'),
            'RegionPanel2$Region1$Toolbar1$ContentPanel1$TextBox2': datetime.now().strftime('%Y-%m-%d'),
            'RegionPanel2$Region1$Toolbar1$ContentPanel1$txtDBBH': '',
            'RegionPanel2$Region1$Toolbar1$ContentPanel1$ddlCZFS': '----全部----',
            'RegionPanel2$Region1$toolbarButtom$pagesize': '1',
            '__box_page_state_changed': 'false',
            '__2_collapsed': 'false',
            '__6_selectedRows': '',
            '__box_disabled_control_before_postbac': '__10',
            '__box_ajax_mark': 'true'
        }
        response = self.session.post(url, data=self.data, headers=self.headers)
        if response.status_code == 200:
            match = re.findall('loadData\((.*?)\);\(function\(\)', response.text)
            if match:
                info = json.loads(match[0])
                print('    宿舍名称                昨日用电          更新时间')
                for i in info:
                    print('%s\t%s\t%s\t' % (i[1], i[5], i[9]))
                    print()

        else:
            print('查询失败')

    def run(self):
        html = self.__get_html()
        if html:
            jz = self.__get_txtjz2(html)
            name = self.__get_name(jz, html)
            password = input('请输入你的密码，若为空可以按enter键跳过')
            self.__login(jz, name, password)
            r = self.session.get('http://172.18.2.42:8000/Default2.aspx')
            if '欢迎回来' in r.text:
                print('登陆成功')
                while True:
                    num = input('请输入你需要查询的功能\n1：查询电费余额等\n2：查询最近一个月的电费使用情况\n3：退出程序')
                    if num == '1':
                        self.__get_detail()
                    elif num == '2':
                        self.__get_month_detail(name)
                    elif num == '3':
                        break
                    else:
                        print('请输入正确的编号')
                print('感谢您的使用！')
            else:
                print('登陆失败')


def main():
    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()
