#!/usr/bin/env python
# encoding: utf-8

"""
@author: sergiojune
"""
import requests, jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image


class Spider(object):
    def __init__(self):
        self.num = 1
        self.file = open('comments.txt', 'w', encoding='utf-8')

    def __get_json(self, index):
        url = 'https://cache.zhibo8.cc/json/2018/nba/0517123898_%d.htm?key=0.1355540028791382' % index
        response = requests.get(url)
        if response.status_code == 200:
            for item in response.json():
                # 写入文件
                self.__write_file(item['content'])
                self.num += 1
            return 1
        else:
            return 0

    def __write_file(self, item):
        self.file.write(item + '\n')
        print('写入成功' + str(self.num)+'条')

    def __get_wordcloud(self):
        with open('comments.txt', 'r', encoding='utf-8') as comments:
            text = comments.read()  # 加载数据
            words = ' '.join(jieba.cut(text, cut_all=True))  # 采用结巴全分词模式
            image = np.array(Image.open('1.jpg'))  # 背景图片
            # 初始化词云
            wc = WordCloud(font_path=r'C:\Windows\Fonts\simkai.ttf',
                           background_color='white', mask=image,
                           max_font_size=100, max_words=2000)
            wc.generate(words)  # 生成词云
            wc.to_file('img.png')  # 生成图片
            image_file = Image.open('img.png')  # 打开图片
            image_file.show()

    def run(self):
        index = 0
        while True:
            res = self.__get_json(index)
            if not res:
                print('以获取完所有评论')
                break
            index += 1
        # 获取词云
        self.__get_wordcloud()
        self.file.close()


def main():
    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()
