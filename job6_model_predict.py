import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

df = pd.read_csv('./crawling_data/naver_headline_news_20231012.csv')
df.info()

X = df['title']
Y = df['category']

with open('./models/encoder.pickle','rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_Y)
label = encoder.classes_

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i],stem=True)
stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)

for i in range(len(X)):
    words = []
    for j in range(len(X[i])):
        if len(X[i][j]) > 1:
            if X[i][j] not in list(stopwords['stopword']):
                words.append(X[i][j])
    X[i] = ' '.join(words)

with open('./models/news_token.pickle','rb') as f:
    token = pickle.load(f)

tokened_x = token.texts_to_sequences(X)
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 23:
        tokened_x[i] = tokened_x[i][:24]
tokened_x_pad = pad_sequences(tokened_x, 23)

model = load_model('./models/news_category_classification_model_0.71788.h5')
preds= model.predict(tokened_x_pad)
predicts = []
second_predicts = []
for pred in preds:
    category = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second_category = label[np.argmax(pred)]
    predicts.append([category, second_category])
df['predict'] = predicts
df.to_csv('./predict.csv',index=False)

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i,'OX'] = 'O'
    else:
        df.loc[i,'OX'] = 'X'
print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))
for i in range(len(df)):
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])
