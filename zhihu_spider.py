# -*-coding:utf-8-*-
import urllib2
import urllib
from selenium import webdriver
from xlwt import Workbook
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_urls(keyword):
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=option)
    code_keyword = urllib.quote(keyword)
    source_url = 'https://www.zhihu.com/search?type=content&q=' + code_keyword
    driver.get(source_url)  # 打开网址
    time.sleep(1)
    driver.refresh()    # 这里要刷新一下，不然第一次加载没反应
    driver.implicitly_wait(2)   # 隐性等待2秒
    for i in range(50):  # 知乎属于向下滑动加载下一页，这里设定的是滑动50次
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)
    time.sleep(3)
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    soup = BeautifulSoup(html, "lxml")
    urllist = {}
    for div in soup.find_all('div', class_="ContentItem AnswerItem"):
        name = div.get("name")
        meta_url = div.find('meta', itemprop="url")
        meta_tiitle = div.find('meta', itemprop="name")
        url = meta_url.get("content")
        title = meta_tiitle.get("content")
        title = str(title).replace('<em>', '')
        title = str(title).replace('</em>', '')
        # https://www.zhihu.com/question/26047889/answer/42431974
        urllist[title] = url+"/answer/"+name
    return urllist
    driver.quit()

def getcommit(urllist):
    book = Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('1', cell_overwrite_ok=True)
    num = 0
    for title in urllist.keys():
        url = urllist[title]
        print url
        for trynum in range(10):  # 网络环境不好的情况下要try十次
            try:
                req = urllib2.urlopen(url)
                html = req.read()
                soup = BeautifulSoup(html, 'html.parser')
                break
            except:
                continue
        try:
            a = soup.find('a', class_="QuestionMainAction")
            stra = str(a.text).encode('gbk')
            itemnum = filter(str.isdigit, stra)
        except:
            itemnum = 0
        sheet.write(num, 0, title)
        sheet.write(num, 1, url)
        sheet.write(num, 2, itemnum)
        num = num+1
    book.save('zhihu.xls')

if __name__ == '__main__':
    keyword = '高铁'   # 关键字
    urllist = {}
    urllist = get_urls(keyword)
    getcommit(urllist)
