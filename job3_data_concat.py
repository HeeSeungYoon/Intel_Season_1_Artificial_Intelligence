import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_title = pd.read_csv(path)
    df = pd.concat([df, df_title], ignore_index=True)

print(df['category'].value_counts())
df.info()
df.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),index=False)
