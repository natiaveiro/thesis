# data is more or less balanced, 406 for 1 and 440 for 0
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

vectorizer = TfidfVectorizer(ngram_range=(2, 2), max_features=200)


train = pd.read_csv('big_file.csv')
# print(train.head())

# sns.countplot(x='Label', data=train)
# plt.show()

train_corpus, test_corpus, train_labels, test_labels = train_test_split(train['Article'],
                                                    train['Label'], test_size=0.30, random_state=101)

X_train = vectorizer.fit_transform(train_corpus)
X_test = vectorizer.transform(test_corpus)
X_train = scipy.sparse.csr_matrix(X_train)
# print(X_train.shape)
y_train = np.array(train_labels, dtype=float)
X_test = scipy.sparse.csr_matrix(X_test)
y_test = np.array(test_labels, dtype=float)


logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)
predictions = logmodel.predict(X_test)
print(classification_report(y_test,predictions))

indices = np.argsort(vectorizer.idf_)[::-1]
features = vectorizer.get_feature_names()
top_n = 20
top_features = [features[i] for i in indices[:top_n]]
print(top_features)