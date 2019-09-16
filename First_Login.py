#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():
    # 无法直接访问
    # url = 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/C/LocalChronicleRegion.aspx?NodeID=11'

    url = 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/D/LocalChronicleItem_2293311.aspx'
    driver.get(url)
    time.sleep(3)
    # 选定d读者证
    driver.find_element_by_xpath('//*[@id="jvForm"]/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/input[2]').click()
    time.sleep(1)


    driver.find_element_by_xpath('//*[@id="username"]').clear()
    driver.find_element_by_xpath('//*[@id="username"]').send_keys("60638335")#用户名
    driver.find_element_by_xpath('//*[@id="password"]').clear()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("111111") #密码

    # # 等待1秒后点击登录
    driver.find_element_by_xpath('//*[@id="jvForm"]/table[2]/tbody/tr/td[2]/table/tbody/tr[6]/td/input[1]').click()
    #
    #
    # #　点击进入新方志 ，有一个跳转新页面的反爬虫机制
    driver.find_element_by_xpath('//*[@id="a23"]/ul/li[9]/a[2]').click()

    # 完成跳转之后的页面的定位！
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])


    # 继续点击进入地区链接
    driver.find_element_by_xpath('//*[@id="wrap3"]/ul/li[1]/a/t').click()









    #
    # driver.find_element_by_xpath('//*[@id="login_btn"]').click()
    # driver.find_element_by_xpath('//*[@id="kwdselectid"]').send_keys("运维")  #可以针对其他岗位进行统计分析
    # # 还要剔除本地选项　　（“”）
    #
    # driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button').click()
    #
    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,48):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[last()]/a').click()
        time.sleep(1)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    location_name = selector.xpath('//*[@id="wrap3"]/ul/li/a/t/text()')
    link = selector.xpath("//div[@class='dw_table']/div/p/span[1]/a/@href")
    firms = selector.xpath('//*[@id="resultList"]/div/span[1]/a/text()')
    long_tuple = (i for i in zip(jobs, link, firms))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='JOB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into xian_yunwei (jobs,link,firms) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass

get_first_page()


#
# if __name__ == '__main__':
#         html = get_first_page()
#         content = parse_html(html)
#         time.sleep(1)
#         insertDB(content)
#         while True:
#             html = next_page()
#             content = parse_html(html)
#             insertDB(content)
#             print(datetime.datetime.now())
#             time.sleep(1)


# #
# create table xian_yunwei(
# id int not null primary key auto_increment,
# jobs varchar(80),
# link varchar(88),
# firms varchar(80)
# ) engine=InnoDB  charset=utf8;


# 封面 前言  目录 东城区概况
# 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/F/view/%E5%B0%81%E9%9D%A2.aspx?ID=LocalChronicleItem_2293311&transaction=%7b%22ExtraData%22%3a%5b%5d%2c%22IsCache%22%3afalse%2c%22Transaction%22%3a%7b%22DateTime%22%3a%22%5c%2fDate(1568634666051%2b0800)%5c%2f%22%2c%22Id%22%3a%22cf0a695a-3537-4054-914c-aaca01472549%22%2c%22Memo%22%3anull%2c%22ProductDetail%22%3a%22LocalChronicleItem_2293311%22%2c%22SessionId%22%3a%229fec6bb3-7987-4edb-88ed-e102264310f6%22%2c%22Signature%22%3a%22E4%5c%2ftS5fodslF%2bhi0HBGOQp%5c%2frdVdyDca6uzEHalHUdDRLPAmD7Pjp7PPR8dEQK9uw%22%2c%22TransferIn%22%3a%7b%22AccountType%22%3a%22Income%22%2c%22Key%22%3a%22LocalChronicleItemFulltext%22%7d%2c%22TransferOut%22%3a%7b%22AccountType%22%3a%22GBalanceLimit%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22Turnover%22%3a0.50000%2c%22User%22%3a%7b%22AccountType%22%3a%22Group%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22UserIP%22%3a%2210.18.17.187%22%7d%2c%22TransferOutAccountsStatus%22%3a%5b%5d%7d'
# 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/F/view/%E5%89%8D%E8%A8%80.aspx?ID=LocalChronicleItem_2293312&transaction=%7b%22ExtraData%22%3a%5b%5d%2c%22IsCache%22%3afalse%2c%22Transaction%22%3a%7b%22DateTime%22%3a%22%5c%2fDate(1568634988566%2b0800)%5c%2f%22%2c%22Id%22%3a%22a780b02a-eec7-46d9-a6eb-aaca01489f3c%22%2c%22Memo%22%3anull%2c%22ProductDetail%22%3a%22LocalChronicleItem_2293312%22%2c%22SessionId%22%3a%229fec6bb3-7987-4edb-88ed-e102264310f6%22%2c%22Signature%22%3a%22P77IJrsbh%5c%2fiXgJfxL%2bl3fzHzinLJOM9dAhGY%2becSB3sGKRrdMhSeEEQtKm1mwvK0%22%2c%22TransferIn%22%3a%7b%22AccountType%22%3a%22Income%22%2c%22Key%22%3a%22LocalChronicleItemFulltext%22%7d%2c%22TransferOut%22%3a%7b%22AccountType%22%3a%22GBalanceLimit%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22Turnover%22%3a1.00000%2c%22User%22%3a%7b%22AccountType%22%3a%22Group%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22UserIP%22%3a%2210.18.17.187%22%7d%2c%22TransferOutAccountsStatus%22%3a%5b%5d%7d'
# 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/F/view/%E7%9B%AE%E5%BD%95.aspx?ID=LocalChronicleItem_2293313&transaction=%7b%22ExtraData%22%3a%5b%5d%2c%22IsCache%22%3afalse%2c%22Transaction%22%3a%7b%22DateTime%22%3a%22%5c%2fDate(1568635045802%2b0800)%5c%2f%22%2c%22Id%22%3a%22d1ce0891-409c-43bd-96fa-aaca0148e253%22%2c%22Memo%22%3anull%2c%22ProductDetail%22%3a%22LocalChronicleItem_2293313%22%2c%22SessionId%22%3a%229fec6bb3-7987-4edb-88ed-e102264310f6%22%2c%22Signature%22%3a%22TnGqI1qGf0M0We6E%2b7nqxX6VJvwmn7wVp%2bmVRjYGjME2dsCzWPLvbUw%2bxbjQU7hQ%22%2c%22TransferIn%22%3a%7b%22AccountType%22%3a%22Income%22%2c%22Key%22%3a%22LocalChronicleItemFulltext%22%7d%2c%22TransferOut%22%3a%7b%22AccountType%22%3a%22GBalanceLimit%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22Turnover%22%3a0.50000%2c%22User%22%3a%7b%22AccountType%22%3a%22Group%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22UserIP%22%3a%2210.18.17.187%22%7d%2c%22TransferOutAccountsStatus%22%3a%5b%5d%7d'
#


# 测试剩下所有的链接


# 查看原文的链接  给链接增加了link算法的
# '/F/view/%E5%B0%81%E9%9D%A2.aspx?ID=LocalChronicleItem_2293311'


# 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/F/Download.aspx?transaction=%7b%22ExtraData%22%3a%5b%5d%2c%22IsCache%22%3afalse%2c%22Transaction%22%3a%7b%22DateTime%22%3a%22%5c%2fDate(1568635412622%2b0800)%5c%2f%22%2c%22Id%22%3a%22636f82a0-23b6-41f4-b714-aaca014a902c%22%2c%22Memo%22%3anull%2c%22ProductDetail%22%3a%22LocalChronicleItem_2293311%22%2c%22SessionId%22%3a%22e4a7c97c-eeb9-4362-b572-3c86ce55079a%22%2c%22Signature%22%3a%22UO8JTvqKk1SP9acKOSVwMaCjiPRGRIOaPMyzuCFjtck%2bEWFcQIzRGEXLZJxvyHgc%22%2c%22TransferIn%22%3a%7b%22AccountType%22%3a%22Income%22%2c%22Key%22%3a%22LocalChronicleItemFulltext%22%7d%2c%22TransferOut%22%3a%7b%22AccountType%22%3a%22GBalanceLimit%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22Turnover%22%3a0.50000%2c%22User%22%3a%7b%22AccountType%22%3a%22Group%22%2c%22Key%22%3a%22zjlib2%22%7d%2c%22UserIP%22%3a%2210.18.17.187%22%7d%2c%22TransferOutAccountsStatus%22%3a%5b%5d%7d'


# 尝试用selenium模拟人手动点击下载？
# 还是无法直接跳转到最终的页面， 因为是带着浙江图书馆的Ip访问万方数据库的
# 尝试在新页面连续点击？？

# 'http://61.175.198.136:8083/rwt/243/http/GEZC6MJZFZZUPLSSGMZUVPBRHA6A/D/LocalChronicleItem_2293311.aspx'

