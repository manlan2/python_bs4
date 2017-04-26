from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_list']
item_info = tongcheng['item_info']


# 在最左边是在python 中对象的名称，后面的是在数据库中的名称
# spider 1
def get_links_from(channel, pages, who_sells=0):
    # td.t 没有这个就终止
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            get_item_info(item_link)
            print(item_link)
            # return urls
    else:
        # It's the last page !
        pass

# spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
    no_longer_exist = '很遗憾！您浏览的页面不存在' in wb_data.text
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price.c_f50')[0].text if soup.find_all('span', 'c_f50') else None
        date = soup.select('.time')[0].text if soup.find_all('li', 'time') else None
        area = list(soup.select('.c_25d a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
        item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
        print({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})

