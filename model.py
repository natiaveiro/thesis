# data is more or less balanced, 406 for 1 and 440 for 0
import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC

stop_words = ["не", "ви", "са", "ни", "го", "си", "ги", "на", "по", "за", "да", "че", "от", "до", "се", "им", "ми",
              "му", "тези", "нас", "ще", "как", "ако", "но"]

vectorizer = TfidfVectorizer(ngram_range=(2, 2),max_features=1000, stop_words=stop_words)

train = pd.read_csv('big_file.csv', usecols=['Article', 'Label'])
train.Article = train.Article.str.replace('[^\u0430-\u044F\u0410-\u042F]', ' ').str.strip()
train.Article = train.Article.str.replace(r"\b[\u0430-\u044F\u0410-\u042F]\b", "")
# print(train)
# print(train.Article.to_string(index=False))


# sns.countplot(x='Label', data=train)
# plt.show()
# train['Uppercase'] = train['Article'].str.findall(r'\b[\u0410-\u042F]+\b').str.len()/len(train['Article'])
# train['exclamation'] = train['Article'].str.findall(r'[^\w\s]').str.len()
# train['comma'] = train['Article'].str.findall(r'[^\w\s]').str.len()

# print(train)
# sns.countplot(x='Label', hue='Uppercase', data=train)
# sns.boxplot(x='Label', y='Uppercase', data=train, showfliers=False)
# plt.show()


train_corpus, test_corpus, train_labels, test_labels = train_test_split(train['Article'],
                                                                        train['Label'], test_size=0.30, random_state=42)

X_train = vectorizer.fit_transform(train_corpus)
X_test = vectorizer.transform(test_corpus)
X_train = scipy.sparse.csr_matrix(X_train)
# print(X_train.shape)
y_train = np.array(train_labels, dtype=float)
X_test = scipy.sparse.csr_matrix(X_test)
y_test = np.array(test_labels, dtype=float)

logmodel = LogisticRegression()
svcmodel = LinearSVC()
svcmodel.fit(X_train, y_train)
predictions = svcmodel.predict(X_test)
# print(classification_report(y_test,predictions))
#
# indices = np.argsort(vectorizer.idf_)[::-1]
# features = vectorizer.get_feature_names()
# top_n = 20
# top_features = [features[i] for i in indices[:top_n]]
# print(top_features)
#
# print(X_train.shape[0])
# print(X_test.shape[0])

# y_pred = logmodel.predict(X_test)  # predicted class of instance x
score = svcmodel.score(X_test, y_test)
conf_m = confusion_matrix(y_test, predictions)
report = classification_report(y_test, predictions)
feature_names = vectorizer.get_feature_names()
coefs_with_fns = sorted(zip(svcmodel.coef_[0], feature_names))
top = zip(coefs_with_fns[:100], coefs_with_fns[:-(100 + 1):-1])
for (coef_1, fn_1), (coef_2, fn_2) in top:
    print("\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2))

# print('train_x:', X_train, sep='\n')
# print('train_y:', y_train, sep='\n', end='\n\n')
# print('test_x:', X_test, sep='\n')
# print('test_y:', y_test, sep='\n', end='\n\n')
# print('p_pred:', p_pred, sep='\n', end='\n\n')
# print('y_pred:', y_pred, end='\n\n')
print('score_:', score, end='\n\n')
print('conf_m:', conf_m, sep='\n', end='\n\n')
print('report:', report, sep='\n')
