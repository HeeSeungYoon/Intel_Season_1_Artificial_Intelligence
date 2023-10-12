import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width',True)
df=pd.read_csv('./crawling_data/naver_news_titles_20231012.csv')

X = df['titles']
Y = df['category']

# 뉴스 카테고리를 라벨링하여 onehot Encoding
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform((Y))
label = encoder.classes_
onehot_Y = to_categorical(labeled_Y)
with open('./models/encoder.pickle','wb') as f:
    pickle.dump(encoder, f)

# 기사 제목을 형태소 단위로 분리
okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

# 한 글자 형태소 및 불용어 제거
stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)
for i in range(len(X)):
    words = []
    for j in range(len(X[i])):
        if len(X[i][j]) > 1:
            if X[i][j] not in list(stopwords['stopword']):
                words.append(X[i][j])
    # print('title {} : {} words'.format(i+1, len(words)))
    X[i] = ' '.join(words)

# 불용어가 제거된 제목을 토큰화 => 단어, 형태소를 숫자로 매칭(라벨링)
token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index)+1

with open('./models/news_token.pickle','wb') as f:
    pickle.dump(token, f)

# 제일 긴 문장의 길이에 맞게 다른 문장들을 패딩
max = len(max(tokened_X, key=len))
tokened_X_pad = pad_sequences(tokened_X, max)

# train, test 데이터 생성 및 저장
train_X, test_X, train_Y, test_Y = train_test_split(tokened_X_pad, onehot_Y, test_size=0.2)
print(train_X.shape, train_Y.shape)
print(test_X.shape, test_Y.shape)

xy = train_X, test_X, train_Y, test_Y
np.save('./models/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)



