from sklearn import metrics
import numpy  as  np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.metrics import fbeta_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn import model_selection
from numpy import random as rd
from sklearn import model_selection
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
#read data
data=pd.read_csv("allhyper.data.txt",sep=',', na_values=["NA"],engine='python')
#print data.shape
#print data.head()
#print data['0']
dataname=data.columns
data.columns = [str(i) for i in range(0,30)]
'''process missing values'''
all_feature=[i for i in range(0,30)]
numeric_feature=[0,17,19,21,23,25]
string_feature=[i for i in all_feature if not i in numeric_feature]
#print string_feature

'''replace numeric feature with mean'''
for i in numeric_feature:
    mean_imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    data[str(i)] = mean_imp.fit_transform(data[[str(i)]] ).ravel()
#print data.head()

from sklearn.base import TransformerMixin
class ModeImputer(TransformerMixin):
    def __init__(self):
        "replace missing value with most frequent items"
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)
        return self
    def transform(self, X, y=None):
        return X.fillna(self.fill)
'''replace string feature with most frequent value'''
for j in string_feature:
    data[str(j)] = ModeImputer().fit_transform(data[[str(j)]])
#print data.head()
#print X.head()
#print y.head()
"""get dummies of string feature"""
dummies=[]
dummies.append(data)
for j in string_feature :
    dummies.append(pd.get_dummies(data[str(j)],prefix=dataname[j]).iloc[:, 1:])
data = pd.concat(dummies, axis=1)
data.drop(data.columns[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,28,29,-1,-3]], axis=1, inplace=True)
#print data.columns
#print data.head()

convert_name_list_index=[0,17,19,21,23,25,26,27]
for i in range(0,8):
    data.columns.values[i]=dataname[convert_name_list_index[i]]
#print data.columns
def f2_score(y_true, y_pred):
    y_true, y_pred, = np.array(y_true), np.array(y_pred)
    return fbeta_score(y_true, y_pred, beta=2)

y =data['class_hyperthyroid.']
X = data.drop(data.columns[[-1,6,7]], axis=1)
trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.3)

#linear kernel on train set
clf = SVC(C=784.75997, kernel='linear')
clf.fit(trainX, trainy)
pre = clf.predict(trainX)
linear_f2 = f2_score(trainy,pre)
linear_accuracy=accuracy_score(trainy,pre)
error_rate=1-linear_accuracy
linear_f1=f1_score(trainy,pre)
print "linear kernel on train set:F2 score is ",linear_f2
print "linear kernel on train set:F1 score is ",linear_f1
print "linear kernel on train set:misclassification rate is ",error_rate

#linear kernel on test set
clf = SVC(C=784.75997, kernel='linear')
clf.fit(trainX, trainy)
pre = clf.predict(testX)
linear_f2 = f2_score(testy,pre)
linear_accuracy=accuracy_score(testy,pre)
error_rate=1-linear_accuracy
linear_f1=f1_score(testy,pre)
print "linear kernel on test set:F2 score is ",linear_f2
print "linear kernel on test set:F1 score is ",linear_f1
print "linear kernel on test set:misclassification rate is ",error_rate

#poly kernel on train set
clf = SVC(C=10, kernel='poly',degree=5)
clf.fit(trainX, trainy)
pre = clf.predict(trainX)
poly_f2 = f2_score(trainy,pre)
poly_accuracy=accuracy_score(trainy,pre)
error_rate=1-poly_accuracy
poly_f1=f1_score(trainy,pre)
print "poly kernel on train set:F2 score is ",poly_f2
print "poly kernel on train set:F1 score is ",poly_f1
print "poly kernel on train set:misclassification rate is ",error_rate

#poly kernel on test set
clf = SVC(C=10, kernel='poly',degree=5)
clf.fit(trainX, trainy)
pre = clf.predict(testX)
poly_f2 = f2_score(testy,pre)
poly_accuracy=accuracy_score(testy,pre)
error_rate=1-poly_accuracy
poly_f1=f1_score(testy,pre)
print "poly kernel on test set:F2 score is ",poly_f2
print "poly kernel on test set:F1 score is ",poly_f1
print "poly kernel on test set:misclassification rate is ",error_rate

#rbf kernel on train set
clf = SVC(C=1e+20, kernel='rbf',gamma=0.0001)
clf.fit(trainX, trainy)
pre = clf.predict(trainX)
rbf_f2 = f2_score(trainy,pre)
rbf_accuracy=accuracy_score(trainy,pre)
error_rate=1-rbf_accuracy
rbf_f1=f1_score(trainy,pre)
print "rbf kernel on train set:F2 score is ",rbf_f2
print "rbf kernel on train set:F1 score is ",rbf_f1
print "rbf kernel on train set:misclassification rate is ",error_rate

#rbf kernel on test set
clf = SVC(C=1e+20, kernel='rbf',gamma=0.0001)
clf.fit(trainX, trainy)
pre = clf.predict(testX)
rbf_f2 = f2_score(testy,pre)
rbf_accuracy=accuracy_score(testy,pre)
error_rate=1-rbf_accuracy
rbf_f1=f1_score(testy,pre)
print "rbf kernel on test set:F2 score is ",rbf_f2
print "rbf kernel on test set:F1 score is ",rbf_f1
print "rbf kernel on test set:misclassification rate is ",error_rate








