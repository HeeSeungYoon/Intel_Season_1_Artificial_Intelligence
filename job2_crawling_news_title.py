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

for c in range(3,len(category)):
    titles = []
    df_titles = pd.DataFrame()
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(c)
    for page in range(1,pages[c]+1):
        url = section_url+'#&date=%2000:00:00&page={}'.format(page)
        driver.get(url)
        time.sleep(0.5)
        for ul in range(1,5):
            for li in range(1,6):
                try:
                    title = driver.find_element('xpath','//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(ul, li)).text
                    title = re.compile('[^가-힣|a-z|A-Z]').sub(' ',title)
                    titles.append(title)
                except:
                    print('error {} {}page {} {}'.format(category[c],page,ul,li))

        if page % 10 == 0:
            df_section_title = pd.DataFrame(titles,columns=['titles'])
            df_section_title['category']=category[c]
            df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
            df_titles.to_csv('./crawling_data/naver_news_{}_{}_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d'),category[c],page), index=False)
            titles = []

    df_section_title = pd.DataFrame(titles, columns=['titles'])
    df_section_title['category'] = category[c]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
    df_titles.to_csv('./crawling_data/naver_news_{}_{}_last.csv'.format(datetime.datetime.now().strftime('%Y%m%d'), category[c]), index=False)

# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="paging"]/a[1]
# //*[@id="paging"]/a[2]
# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a