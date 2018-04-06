import re, requests

class Spider(object):
    def __init__(self, headers, url):
        self.headers = headers
        self.url = url

    def __get_hrefs(self):
        '''获取书本的所有链接'''
        response = requests.get(self.url, self.headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            hrefs = re.findall('toctree-l1.*?reference internal" href="([^"]*?)">(.*?)</a>', response.text, re.S)
            return hrefs
        else:
            print('访问书本内容失败，状态码为', response.status_code)

    def __get_page(self, url):
        '''获取首页'''
        response = requests.get(url, self.headers)
        response.encoding = 'utf-8'
        content = re.findall('section".*?(<h1>.*?)<div class="sphinxsidebar', response.text, re.S)
        return content[0]

    def __get_content(self, href):
        '''获取每个页面的内容'''
        if href:
            href = self.url + href
            response = requests.get(href, self.headers)
            response.encoding = 'utf-8'
            content = re.findall('section".*?(<h1>.*?)<div class="sphinxsidebar', response.text, re.S)
            if content:
                return content[0]
            else:
                print('正则获取失败')
        else:
            print('获取内容失败')

    def run(self):
        '''循环获取整本书内容'''
        self.num = 0
        hrefs = self.__get_hrefs()
        content = self.__get_page(self.url)
        with open(str(self.num)+'Python最佳实践指南.html', 'w', encoding='utf-8') as f:
            f.write(content)
            print('写入目录成功')
        for href, title in hrefs:
            title = title.replace('/', '或')  # 路径问题，一个坑
            if "#" in href:
                continue
            self.num += 1
            content = self.__get_content(href)
            with open(str(self.num)+title+'.html', 'w', encoding='utf-8') as f:
                f.write(content)
                print('下载第'+str(self.num)+'章成功')
        print('下载完毕')


def main():
    url = 'http://pythonguidecn.readthedocs.io/zh/latest/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
    spider = Spider(headers, url)
    spider.run()


if __name__ == '__main__':
    main()
