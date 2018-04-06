#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'练习用selenium库来操作浏览器'

__author__ = 'sergiojune'

from selenium import webdriver

# 声明浏览器对象
browser = webdriver.Chrome()  # 这个谷歌浏览器
# 这里有个坑，就是需要下载chromedriver驱动，把这个驱动文件放在谷歌的application文件下，然后添加在path的环境变量，还是不行的话重启编译器试试
# 或者在创建浏览器对象的时候把这个chromedriver的路径添加到变量上也可以的
# 打开网页
# browser.get('https://www.baidu.com')  # 这就打开了一个百度网页
# 关闭打开的网页
# browser.close()
# 这里还有其他的浏览器如firebox，safari等，我没有安装驱动就不试了

# 打开百度
browser.get('https://www.baidu.com')
# 获取网页元素
response = browser.page_source
# print(response)

# 获取单个页面元素
url = 'https://www.jianshu.com/'  # 简书
# 打开简书
browser.get(url)
tag = browser.find_element_by_class_name('name')  # 这个是通过classname来查找元素
print(tag)  # 返回一个WebElement对象
tag = browser.find_element_by_tag_name('div')  # 通过标签名字来查找
print(tag)
browser.find_element_by_css_selector('.content .author .info')  # 通过css选择器来查找
print(tag)
# 还可以通过xpath来进行选择
tag = browser.find_element_by_xpath('//div')
print(tag)
# 还可以通过name属性，连接文本等来查找，就不一一演示了，都差不多，想了解请查文档

# 另外一种方法
from selenium.webdriver.common.by import By
btn = browser.find_element(By.CLASS_NAME, 'btn')  # 这个使用By类进行获取，和上面的差不多
print(btn)
# 再通过标签名字来查找
li = browser.find_element(By.TAG_NAME, 'li')
print(li)

# 获取多个元素就把上面的方法的element改成elements即可
lis = browser.find_elements_by_tag_name('li')  # 获取全部的li标签
print(lis)  # 返回一个列表，装的都是对象


# 进行元素交互操作
browser.get('http://www.baidu.com')  # 打开百度
wd = browser.find_element_by_name('wd')  # 获取输入框
wd.send_keys('简书')  # 输入简书进行搜索
# 获取点击按钮
btn = browser.find_element_by_class_name('s_btn')
btn.click()  # 点击按钮
print(browser.page_source)
# 在清空一下输入框
# wd.clear()
# 搜索简书后进行网站
# href = browser.find_element_by_class_name('c-showurl').get_attribute('href')  # 获取搜索结果的第一个网站,  get_attribute()是获取属性，.text是获取标签内容
# # 发起请求
# browser.get(href)
# print(browser.page_source)


# 在网页进行交互动作，比如拖拽
from selenium.webdriver import ActionChains
browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-example-droppable')
browser.switch_to_frame('iframeResult')  # 切换图层,参数为id名字,当切换到这个frame时，就无法找到这个frame以外的元素
actions = ActionChains(browser)  # 进行动作前期
# 获取需要拖的元素
drag = browser.find_element(By.ID, 'draggable')
# 获取拖放的终点
drop = browser.find_element(By.ID, 'droppable')
# 进行拖放
actions.drag_and_drop(drag, drop)
# 开始动作
actions.perform()
print('拖拽完成')
# 更多动作参考ActionChains文档


# 执行js语句
import time
browser.get('https://www.jianshu.com/')
# 执行js语句
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 参数为js语句
time.sleep(2)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(2)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

# 获取标签的各种信息
li = browser.find_element_by_tag_name('li')
print(li.text)  # 获取标签的内容
print(li.get_attribute('date-note-id'))
print(li.id)  # 标签id
print(li.location)  # 标签位置
print(li.tag_name)  # 标签名字
print(li.size)  # 标签大小


# 现在练习等待，等待分两种，一种显式等待，另一种为隐式等待
# 先练习隐式等待，
# browser.implicitly_wait(10)  # 设置等待10秒时间
# browser.get('https://www.taobao.com/')
# mq = browser.find_element(By.ID, 'mq')
# print(mq.text)

# 现在练习显式等待，常用，原理是意思为在等待时间内满足等待条件就会正常运行，否则就会抛出异常
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# browser.get('https://www.taobao.com/')
# wait = WebDriverWait(browser, 10)  # 最多等待10秒
# tag = wait.until(EC.presence_of_element_located((By.ID, 'mq')))  # 里面的参数是一个元组
# print(tag.get_text())


# 页面后退
browser.back()
time.sleep(3)
# 页面前进
browser.forward()

# 窗口管理
# 新开窗口
browser.execute_script('window.open()')
# 切换窗口
browser.switch_to.window(browser.window_handles[1])  # 角标为1的窗口

# 异常所在的包：selenium.common.exceptions
