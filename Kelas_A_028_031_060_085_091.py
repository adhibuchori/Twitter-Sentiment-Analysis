# -*- coding: utf-8 -*-
"""Kelas_A_028_031_060_085_091.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RWAn07mXTbW4_kFzxkCVfTrvW2b6WCja

# Required Libraries
"""

pip install preprocessor

pip install googletrans==3.1.0a0

pip install sastrawi

pip install scikeras[tensorflow]

# Dataframe
import pandas as pd
import csv
from collections import Counter

# Crawling Data
import tweepy

# Text Preprocessing
import re
import preprocessor as p
import numpy as np
import nltk

nltk.download('stopwords')
nltk.download('punkt')

import string
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from googletrans import Translator
from nltk.tokenize import word_tokenize

# Split Data
from sklearn.model_selection import train_test_split

# Preprocessing, Layer, and Prediction
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Dense, Embedding, Dropout
from keras.models import Sequential
from scikeras.wrappers import KerasClassifier
from tensorflow.keras.optimizers import Adam, RMSprop

# Plotting
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from plotly import graph_objs as go
import plotly.express as px
from palettable.colorbrewer.qualitative import Pastel1_7

# Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns
sns.set(style = 'whitegrid')
from sklearn.metrics import accuracy_score

"""# Crawling Twitter Dataset"""

api_key = "rDaxsP3YqLQCjovabjW1sUw2X"
api_secret_key = "mrKlrDtyfK6shAxZA5SF1j0EKPJYFjlRkSIohKSoDDuog8FM2Z"
access_token = "1203295790162014208-4kODNCqXR7UiVNE8l8XpOKfABaQ3wl"
access_token_secret = "QtMUhiP9CDUJmRwtwfIvfzkBU6SD6gmAWLKPFFiUP6UGp"

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

search_key = "kuliah offline"

csvFile = open('OfflineLectures.csv', 'a+', newline='', encoding='utf-8')

csvWriter = csv.writer(csvFile)
d = []
sn = []
n = []
t = []

for status in tweepy.Cursor(api.search_tweets, 
                            q=search_key, 
                            count=100, 
                            lang="id",
                            result_type="mixed",
                            until="2022-05-29").items():

                           d.append(status.created_at)
                           sn.append(status.user.screen_name)
                           n.append(status.user.name)
                           t.append(status.text)

                           print(status.created_at, 
                                 status.user.screen_name, 
                                 status.user.name, 
                                 status.text)
                                 
                           tweets = [status.created_at, 
                                     status.user.screen_name, 
                                     status.user.name, 
                                     status.text]
                                     
                           csvWriter.writerow(tweets)

with open('OfflineLectures.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('OfflineLectures.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Datetime','Screen Name', 'Name', 'Tweet'])
    w.writerows(data)

df = pd.read_csv('OfflineLectures.csv')
df

"""# Text Preprocessing"""

# Some functions for preprocessing text

def cleaningText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # remove mentions
    text = re.sub(r'#[A-Za-z0-9]+', '', text) # remove hashtag
    text = re.sub(r'RT[\s]', '', text) # remove RT
    text = re.sub(r"http\S+", '', text) # remove link
    text = re.sub(r'[0-9]+', '', text) # remove numbers

    text = text.replace('\n', ' ') # replace new line into space
    text = text.translate(str.maketrans('', '', string.punctuation)) # remove all punctuations
    text = text.strip(' ') # remove characters space from both left and right text
    return text

def casefoldingText(text): # Converting all the characters in a text into lower case
    text = text.lower() 
    return text

def tokenizingText(text): # Tokenizing or splitting a string, text into a list of tokens
    text = word_tokenize(text) 
    return text

def filteringText(text): # Remove stopwors in a text
    listStopwords = set(stopwords.words('indonesian'))
    filtered = []
    for txt in text:
        if txt not in listStopwords:
            filtered.append(txt)
    text = filtered 
    return text

def stemmingText(text): # Reducing a word to its word stem that affixes to suffixes and prefixes or to the roots of words
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = [stemmer.stem(word) for word in text]
    return text

def toSentence(list_words): # Convert list of words into sentence
    sentence = ' '.join(word for word in list_words)
    return sentence

def text_processing(text):
    text = text.apply(cleaningText)
    text = text.apply(casefoldingText)
    text = text.apply(tokenizingText)
    text = text.apply(filteringText)
    text = text.apply(stemmingText)
    return text

# Preprocessing tweets data

df['text_clean'] = df['Tweet'].apply(cleaningText)
df['text_clean'] = df['text_clean'].apply(casefoldingText)
df.drop(['Tweet'], axis = 1, inplace = True)

df['text_preprocessed'] = df['text_clean'].apply(tokenizingText)
df['text_preprocessed'] = df['text_preprocessed'].apply(filteringText)
df['text_preprocessed'] = df['text_preprocessed'].apply(stemmingText)

# drop duplicates/spams tweets
df.drop_duplicates(subset = 'text_clean', inplace = True)

df

# Export to csv file
df.to_csv(r'OfflineLectures-v2.csv', index = False, header = True,index_label=None)

"""# Twitter Sentiment Labelling Manually

Read the tweet dataset after the manual sentiment labeling process.
"""

tweets = pd.read_csv('OfflineLectures-v3.csv')

tweets

for i, text in enumerate(tweets['text_preprocessed']):
    tweets['text_preprocessed'][i] = tweets['text_preprocessed'][i].replace("'", "")\
                                            .replace(',','').replace(']','').replace('[','')
    list_words=[]
    for word in tweets['text_preprocessed'][i].split():
        list_words.append(word)
        
    tweets['text_preprocessed'][i] = list_words   
    
tweets

tweets.isna().sum()

tweets = tweets.dropna()
tweets.isna().sum()

tweets

"""### The Distribution of Tweets Dataset"""

temp = tweets.groupby('sentiment').count()['text_preprocessed'].reset_index().sort_values(by='text_preprocessed',ascending=False)
temp.style.background_gradient(cmap='Purples')

fig = go.Figure(go.Funnelarea(
    text =temp.sentiment,
    values = temp.text_preprocessed,
    title = {"position": "top center", "text": "Funnel-Chart of Sentiment Distribution"}
    ))
fig.show()

"""# Visualize Word Cloud

Since data discrepancies are only found in sentiment columns, we use only A dataset for word cloud visualization.

### Visualize All Word Cloud
"""

list_words = ''

for tweet in tweets['text_preprocessed']:
  for word in tweet:
    list_words += ' ' + (word)

wordcloud = WordCloud(width=700, 
                      height=500, 
                      background_color='white',
                      min_font_size=10).generate(list_words)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Word Cloud of Tweets Data', fontsize=18)
ax.grid(False)
ax.imshow((wordcloud))
fig.tight_layout(pad=0)
ax.axis('off')
plt.show()

"""### Visualize Positive Word Cloud"""

tweets_positive = tweets[tweets['sentiment'] == 'positive' ]

list_words = ''

for tweet in tweets_positive['text_preprocessed']:
  for word in tweet:
    list_words += ' ' + (word)

wordcloud = WordCloud(width=700, 
                      height=500, 
                      background_color='white',
                      min_font_size=10).generate(list_words)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Word Cloud of Tweets Data', fontsize=18)
ax.grid(False)
ax.imshow((wordcloud))
fig.tight_layout(pad=0)
ax.axis('off')
plt.show()

"""### Visualize Negative Word Cloud"""

tweets_negative = tweets[tweets['sentiment'] == 'negative' ]

list_words = ''

for tweet in tweets_negative['text_preprocessed']:
  for word in tweet:
    list_words += ' ' + (word)

wordcloud = WordCloud(width=700, 
                      height=500, 
                      background_color='white',
                      min_font_size=10).generate(list_words)

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Word Cloud of Tweets Data', fontsize=18)
ax.grid(False)
ax.imshow((wordcloud))
fig.tight_layout(pad=0)
ax.axis('off')
plt.show()

"""# Most Common Words in Our Tweet Text After Preprocessed.

Since data discrepancies are only found in sentiment columns, we use only A dataset for most common words visualization.
"""

top = Counter([item for sublist in tweets['text_preprocessed'] for item in sublist])
temp = pd.DataFrame(top.most_common(20))
temp.columns = ['Common_words','count']
temp.style.background_gradient(cmap='Purples')

fig = px.bar(temp, x="count", y="Common_words", title='Commmon Words in Selected Text', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

fig = px.treemap(temp, path=['Common_words'], values='count', title='Tree of Most Common Words')
fig.show()

"""# Most Common Words for Every Sentiment Label."""

positiveSentiment = tweets[tweets['sentiment']=='positive']
negativeSentiment = tweets[tweets['sentiment']=='negative']

"""### Most Common Positive Words."""

top = Counter([item for sublist in positiveSentiment['text_preprocessed'] for item in sublist])
temp_positive = pd.DataFrame(top.most_common(20))
temp_positive.columns = ['Common_words','count']
temp_positive.style.background_gradient(cmap='Greens')

fig = px.bar(temp_positive, x="count", y="Common_words", title='Most Commmon Positive Words', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

fig = px.treemap(temp_positive, path=['Common_words'], values='count',title='Tree Of Most Common Negative Words')
fig.show()

"""### Most Common Negative Words"""

top = Counter([item for sublist in negativeSentiment['text_preprocessed'] for item in sublist])
temp_negative = pd.DataFrame(top.most_common(20))
temp_negative.columns = ['Common_words','count']
temp_negative.style.background_gradient(cmap='Reds')

fig = px.bar(temp_negative, x="count", y="Common_words", title='Most Commmon Neutral Words', orientation='h', 
             width=700, height=700,color='Common_words')
fig.show()

fig = px.treemap(temp_negative, path=['Common_words'], values='count',title='Tree Of Most Common Negative Words')
fig.show()

"""# Natural Language Processing"""

# Make text preprocessed (tokenized) to untokenized with toSentence Function
X = tweets['text_preprocessed'].apply(toSentence)
max_features = 5000

# Tokenize text with specific maximum number of words to keep, based on word frequency
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(X.values)
X = tokenizer.texts_to_sequences(X.values)

X = pad_sequences(X)
X.shape

polarity_encode = {'positive' : 0, 'negative' : 1}
label = tweets['sentiment'].map(polarity_encode).values

label.shape

tweetText_train, tweetText_test, label_train, label_test = train_test_split(X, label, test_size=0.2, random_state=0)

print(tweetText_train.shape, label_train.shape)
print(tweetText_test.shape, label_test.shape)

tweetText_train.shape[1]

def create_model(embed_dim=16, hidden_unit=16, dropout_rate=0.2, optimizers='Adam', learning_rate=0.01):
    model = Sequential()
    model.add(Embedding(input_dim=max_features, output_dim=embed_dim, input_length=tweetText_train.shape[1]))
    model.add(LSTM(units=hidden_unit, activation = 'tanh'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(units=3, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizers(learning_rate=learning_rate), metrics=['accuracy'])
    print(model.summary())
    return model

model = KerasClassifier(model=create_model,
                        # Model Parameters
                        dropout_rate=0.2,
                        embed_dim=32,
                        hidden_unit=16,
                        optimizers=Adam,
                        learning_rate=0.01,
                   
                        # Fit Parameters
                        epochs=10, 
                        batch_size=128,
                        # Initiate validation data, which is 10% data from data train. It's used for evaluation model
                        validation_split=0.1)
                         

model_prediction = model.fit(tweetText_train, label_train)

fig, ax = plt.subplots(figsize = (10, 4))
ax.plot(model_prediction.history_['accuracy'], label = 'train accuracy')
ax.plot(model_prediction.history_['val_accuracy'], label = 'val accuracy')
ax.set_title('Model Accuracy')
ax.set_xlabel('Epoch')
ax.set_ylabel('Accuracy')
ax.legend(loc = 'upper left')
plt.show()

y_pred = model.predict(tweetText_test)
accuracy = accuracy_score(label_test, y_pred)
print('Model Accuracy on Test Data:', accuracy)
confusion_matrix(label_test, y_pred)

fig, ax = plt.subplots(figsize = (8,6))
sns.heatmap(confusion_matrix(y_true = label_test, y_pred = y_pred), fmt = 'g', annot = True)
ax.xaxis.set_label_position('top')
ax.xaxis.set_ticks_position('top')
ax.set_xlabel('Prediction', fontsize = 14)
ax.set_xticklabels(['positive', 'negative'])
ax.set_ylabel('Actual', fontsize = 14)
ax.set_yticklabels(['positive', 'negative'])
plt.show()

# Initializing and preprocessing new text data
otherData = pd.DataFrame()
otherData['text'] = ["kuliah offline seru banget", "tapi serius deh semakin kesini makin takut kuliah offline"]

otherData['text_clean'] = otherData['text'].apply(cleaningText)
otherData['text_clean'] = otherData['text_clean'].apply(casefoldingText)
otherData.drop(['text'], axis = 1, inplace = True)

otherData['text_preprocessed'] = otherData['text_clean'].apply(tokenizingText)
otherData['text_preprocessed'] = otherData['text_preprocessed'].apply(filteringText)
otherData['text_preprocessed'] = otherData['text_preprocessed'].apply(stemmingText)
otherData

# Preprocessing text data

# Make text preprocessed (tokenized) to untokenized with toSentence Function
X_otherData = otherData['text_preprocessed'].apply(toSentence)
X_otherData = tokenizer.texts_to_sequences(X_otherData.values)
X_otherData = pad_sequences(X_otherData, maxlen = X.shape[1])
X_otherData

# Results from prediction sentiment on text data

y_pred_otherData = model.predict(X_otherData)
otherData['Result Prediction'] = y_pred_otherData

polarity_decode = {0 : 'positive', 1 : 'negative'}
otherData['Result Prediction'] = otherData['Result Prediction'].map(polarity_decode)
otherData