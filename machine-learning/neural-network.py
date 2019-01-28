
from sklearn.neural_network import MLPClassifier
import numpy  as  np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.metrics import fbeta_score
from sklearn import model_selection
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import time
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
trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.3,random_state=0)

kf = KFold(n_splits = 3,random_state=1, shuffle=False)
bestf2=0
alphalist=np.arange(0.00001,0.0001,0.00001)
for a in alphalist:
    print "working on alpha =", a
    f2_list = []
    for train_index, validation_index in kf.split(trainX):
        sub_trainX = trainX.iloc[train_index]
        validationX = trainX.iloc[validation_index]
        sub_trainy = trainy.iloc[train_index]
        validationy = trainy.iloc[validation_index]
        clf = MLPClassifier(hidden_layer_sizes=(20, 15), alpha=a, random_state=1,max_iter=500)
        clf.fit(sub_trainX, sub_trainy)
        val_pre = clf.predict(validationX)
        F2 = f2_score(validationy, val_pre)
        f2_list.append(F2)
    mean_f2 = np.mean(f2_list)
    if mean_f2 > bestf2:
        bestf2 = F2
        bestalpha = a
print "best alpha is:",bestalpha," and the f2_score for that is:",bestf2
start_time = time.time()
clf = MLPClassifier(hidden_layer_sizes=(20,15),alpha=bestalpha,random_state=1,max_iter=500)
clf.fit(trainX, trainy)
pre_train=np.array(clf.predict(trainX))
F1_train=f1_score(np.array(trainy),pre_train)
F2_train=f2_score(np.array(trainy),pre_train)
train_accuracy=accuracy_score(trainy,pre_train)
error_rate=1-train_accuracy
print "Neural Network:F1_score of train set is:",F1_train
print "Neural Network:F2_score of train set is:",F2_train
print "Neural Network:misclassification rate of train set is:",error_rate
pre_test=np.array(clf.predict(testX))
F1_test=f1_score(np.array(testy),pre_test)
F2_test=f2_score(np.array(testy),pre_test)
test_accuracy=accuracy_score(testy,pre_test)
error_rate=1-test_accuracy

print "Neural Network:F1_score of test set is:",F1_test
print "Neural Network:F2_score of test set is:",F2_test
print "Neural Network:misclassification rate of test set is:",error_rate
end_time = time.time()
print("Neural Network costs %g seconds" % (end_time - start_time))
