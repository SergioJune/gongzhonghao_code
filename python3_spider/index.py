import requests
from bs4 import BeautifulSoup
# 我们用选择器来选择我们需要获取的内容
def get_info(soup):
    imgs = soup.select('dd .board-img')  # 这是获取图片链接
    names = soup.select('dd .board-item-main .name')  # 这是获取电影名字
    starses = soup.select('dd .board-item-main .movie-item-info .star')  # 这是获取电影主演
    times = soup.select('dd .board-item-main .movie-item-info .releasetime')  # 这是获取电影上映时间
    scores = soup.select('dd .board-item-main .score-num')
    films = []  # 存储一个页面的所有电影信息
    for x in range(0, 10):
        # 这个是获取属性的链接
        img = imgs[x]['data-src']
        # 下面的都是获取标签的内容并去掉两端空格
        name = names[x].get_text().strip()
        stars = starses[x].get_text().strip()[3:]  # 使用切片是去掉主演二字
        time = times[x].get_text().strip()[5:]  # 使用切片是去掉上映时间二字
        score = scores[x].get_text().strip()
        film = {'name': name, 'stars': stars, 'img': img, 'time': time, 'score': score}
        films.append(film)
    pages = soup.select('.list-pager li a')  # 可以看到下一页的链接在最后一个a标签
    page = pages[len(pages)-1]['href']
    return films, page


url_start = 'http://maoyan.com/board/4'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'}
page = ''
while True:
    response = requests.get(url_start + page, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    films, page = get_info(soup)
    # 写个json文件吧，这样容易点
    with open('猫眼电影top250.json', 'a', encoding='utf-8') as f:
        for film in films:
            f.write(str(film)+'\n')
    if '下一页' not in response.text:  # 下一页不在就表示下载完毕
        print('所有电影下载完毕')
        break
