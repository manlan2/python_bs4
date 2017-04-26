import requests
from bs4 import BeautifulSoup

str = "hello world"

# print("he" in str)

url = 'http://bj.58.com/yishu/2312770932851x.shtml'

wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
# price = soup.select('span.price.c_f50')[0].text # if soup.find_all('span', 'c_f50') else None

print(soup.select('ghspan.price.c_f50'))

# print(price)
