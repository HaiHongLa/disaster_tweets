from joblib import dump, load
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# df = pd.read_csv("../train.csv")
# df = df.drop(['id', 'keyword', 'location'], axis=1)
# X = df['text']
# y = df['target']

# tfidf = TfidfVectorizer(stop_words='english')
# tfidf.fit(X)
# X_train_tfidf = tfidf.transform(X)

# nb = MultinomialNB()
# nb.fit(X_train_tfidf, y)

# pipe = Pipeline([('tfidf',TfidfVectorizer(stop_words='english')),('scaler', StandardScaler(with_mean=False)), ('svc', SVC())])
# pipe.fit(X, y)

# dump(pipe, 'pipe.joblib')

pipe = load('pipe.joblib')

print(pipe.predict(['Forest fire near La Ronge Sask. Canada	'])[0])