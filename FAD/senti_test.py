import pandas as pd
import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from google_play_scraper import Sort, reviews
from sklearn.metrics import accuracy_score
import play_scraper
import eel
from textblob import TextBlob
import datetime

eel.init('web')

def get_reviews(url):
    result = reviews(
    url,
    lang='en', 
    country='us', 
    sort=Sort.NEWEST,
    count=200,
    )
    f=[]
    for i in result:
        f.append(i['content'])
    return f  

df = pd.read_csv("web/training.txt", sep='\t', names=['liked','txt'])
df.head()
stopset = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(use_idf=True, lowercase=True, strip_accents='ascii', stop_words=stopset)
y = df.liked
x = vectorizer.fit_transform(df.txt.values.astype('U'))
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42)
clf = naive_bayes.MultinomialNB()
clf.fit(X_train, y_train)

@eel.expose
def scrap_review(appname):
    a = datetime.datetime.now()
    print("start",a.second)
    raw_review = get_reviews(appname)
    app_reviews_array = np.array(raw_review)
    app_review_vector = vectorizer.transform(app_reviews_array)
    predicts = clf.predict(app_review_vector)
    save_scrapped_result(raw_review,appname,predicts)
    slice_count=[0,0]
    for i in predicts:
        if i==1:
            slice_count[0] +=1
        else:
            slice_count[1] +=1
    b = datetime.datetime.now()
    c = b - a
    print(c.seconds)
    print(slice_count)
    
    return [slice_count,[(sum(predicts)/len(predicts))*100,sum(predicts)/len(predicts)]]

def save_scrapped_result(rrw,appname,predicts):
    review_sentiments = []
    review_polarity = []
    for i in range(len(rrw)):
            review_sentiments.append("{}\t{}\n".format('1' if predicts[i]==1 else '0',rrw[i]))
    f = open("results/"+appname+".txt", 'w', encoding="utf-8")
    g = open("results/polarity/"+appname+".txt", 'w', encoding="utf-8")
    for i in range(len(rrw)):
        pol = TextBlob(rrw[i]).sentiment.polarity
        review_polarity.append("{:>4}\t\t{}\t{}\n".format(round(pol,1),(1|predicts[i]) if pol>0 else '0',rrw[i]))
    for i in review_polarity:
        g.write(i)
    for i in review_sentiments:
        f.write(i)
    f.close()

@eel.expose
def search_app(query):
    app_data = []
    search_result=play_scraper.search(query, page=1)
    for app in search_result[:8 if len(search_result) > 8 else len(search_result)]:
        app_data.append([app['title'],app['icon'],app['app_id'],app['developer']])
    return app_data

eel.start('index.html', size=(1200,600))

