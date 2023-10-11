from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
options.add_argument('user-agent='+user_agent)
options.add_argument('lang=ko_KR')
# options.add_argument('window-size=1920x1080')
# options.add_argument('disable-gpu')
# options.add_argument('--no-sandbox')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

category = ['Politics','Economic','Social','Culture','World','Science']
pages = [110, 110, 110, 75, 110, 72]
df_titles = pd.DataFrame()

for l in range(len(category)):
    titles = []
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    for k in range(1, pages[l]+1):
        url = section_url+'#&date=%2000:00:00&page={}'.format(k)
        driver.get(url)
        time.sleep(0.5)
        for i in range(1, 6):
            for j in range(1, 6):
                try:
                    title = driver.find_element('xpath','//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i+1, j+1)).text
                    title = re.compile('[^가-힣]').sub(' ',title)
                    titles.append(title)
                except:
                    print('error {} {} {} {}'.format(l, k, i, j))
    if k % 10 ==0:
        df_section_title = pd.DataFrame(titles, columns=['titles'])
        df_section_title['category'] = category[l]
        df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
        df_titles.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(l, k), index=False)


    df_section_title = pd.DataFrame(titles,columns=['titles'])
    df_section_title['category']=category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)

print(df_titles.head(30))
print(df_titles.info())
print(df_titles['category'].value_counts())
#df_titles.to_csv('./crawling_data/naver_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')))


# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="paging"]/a[1]
# //*[@id="paging"]/a[2]
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a