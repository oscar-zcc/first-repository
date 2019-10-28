from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from multiprocessing import Pool
import pymysql
#获取索引页
def index_page():
    chrom_options = webdriver.ChromeOptions()
    chrom_options.add_argument('--headless')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
        }
    }
    chrom_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrom_options)
    # browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    url = 'https://www.csdn.net/nav/python'
    browser.get(url)
    # print(browser.page_source)
    get_info(browser)

list = []
list2 = []
# 获取信息
def get_info(browser):
    # browser.execute_script('window.scrollTo(0,10000)')
    browser.implicitly_wait(10)
    name = browser.find_elements_by_css_selector('main ul.feedlist_mod li .list_con dl.list_userbar .name a:link, '
    'main ul.feedlist_mod li .list_con dl.list_userbar .name a:visited')
    title = browser.find_elements_by_css_selector('main ul.feedlist_mod li .list_con h2 a')
    abstract = browser.find_elements_by_css_selector('main ul.feedlist_mod li .list_con .summary')
    href = browser.find_elements_by_css_selector('main ul.feedlist_mod li .list_con h2 a')
    for i in range(0,1):
        url = href[i].get_attribute('href')
        list.append(url)
        print('作者:'+name[i].text)
        print('标题:'+title[i].text)
        print('简介:'+abstract[i].text)
        print('链接:'+href[i].get_attribute('href'))
        print('----------------------------------------------------------------------')
        list2.append({'作者': name[i].text,
                      '标题': title[i].text,
                      '简介': abstract[i].text,
                      '链接': href[i].get_attribute('href')})
    browser.close()

def get_time(url,i):
    chrom_options = webdriver.ChromeOptions()
    # chrom_options.add_argument('--headless')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
        }
    }
    chrom_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(chrome_options=chrom_options)
    # browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    # browser.set_page_load_timeout(5)
    try:
        browser.get(url)
        date = browser.find_element_by_css_selector('main div.blog-content-box .article-header-box .article-header '
        'div.article-info-box div.article-bar-top span.time')
        print(date.text)
        list2[i]['日期'] = date.text
        print(list2)
        # list3.append({'日期':time.text})
    except:
        get_time(url,i)
        print('timeout')
        browser.execute_script('window.stop()')
def save_info():
    db = pymysql.connect(user = 'root',
                         passwd = '123456',
                         database = 'item',
                         charset = 'utf8')
    cur = db.cursor()
    for i in list2:
        date = i['日期'].split(' ')
        date = date[0]
        print(date)
        author = i['作者']
        title = i['标题']
        abstract = i['简介']
        interlinkage = i['链接']
        sql = 'insert into spider (date,author,title,abstract,interlinkage)values(%s,%s,%s,%s,%s)'
        cur.execute(sql,[date,author,title,abstract,interlinkage])
    try:
        db.commit()
    except Exception as e:
        db.rollback()



if __name__ == '__main__':
    index_page()
    # print(list)
    # pool = Pool()
    for i in range(len(list)):
        get_time(list[i],i)
    save_info()
    # save_info2()
    # pool.map(get_time,list)


