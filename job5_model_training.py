import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping

X_train, X_test, Y_train, Y_test = np.load('./models/news_data_max_23_wordsize_12361.npy', allow_pickle=True)
print(X_train.shape, X_test.shape)
print(Y_train.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(12361, 300, input_length=23)) # 차원 축소 레이어
model.add(Conv1D(32, kernel_size=5, padding='same',activation='relu'))
model.add(MaxPooling1D(pool_size=1)) # Conv 레이어와 세트 - 지금은 아무 일도 하지 앟음
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='auto')
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=10, validation_data=(X_test, Y_test), callbacks=[early_stopping])
model.save('./models/news_category_classification_model_%.5f.h5'%fit_hist.history['val_accuracy'][-1])
plt.plot(fit_hist.history['val_accuracy'], label='validation accuracy')
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()