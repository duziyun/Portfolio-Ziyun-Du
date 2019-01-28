import numpy  as  np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn import model_selection
from numpy import random as rd
from sklearn import model_selection
from sklearn import tree
from sklearn.metrics import accuracy_score
from collections import defaultdict
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
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

y =data['class_hyperthyroid.']
X = data.drop(data.columns[[-1,6,7]], axis=1)

trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.3)
#print X.columns
#print y.head()
#print X.head()
#print X.shape
#print y.shape

def get_subset_validation(X,y):
    trainX, valX, trainy, valy = model_selection.train_test_split(X, y, test_size=0.37)
    sample=pd.concat([trainX,trainy], axis=1)
    subset=sample.sample(frac=1/0.63, replace=True)
    validation=pd.concat([valX,valy], axis=1)
    return subset,validation

def random_forest(X,y,nest,criterion,maxDepth,minSamplesLeaf):
    feature_name=X.columns
    sub_feature_lenth=int(len(feature_name)**0.5)
    data=pd.concat([X,y], axis=1)
    treelist=[]
    oob_accuracy=[]
    choosen_features_list=[]
    feature_importance=defaultdict(list)

    for i in range(nest):
        data=data.sample(frac=1)
        newX=data.drop(data.columns[[-1]], axis=1)
        newy=data[data.columns.values[-1]]
        subset, validation=get_subset_validation(newX,newy)
        subsetX=subset.drop(data.columns[[-1]], axis=1)
        subsety=subset[subset.columns.values[-1]]
        valX = validation.drop(validation.columns[[-1]], axis=1)
        valy = validation[validation.columns.values[-1]]

        choosen_feature_index=rd.choice(range(len(feature_name)), sub_feature_lenth, replace=False)
        choosen_feature_name=[]
        for index in choosen_feature_index:
            choosen_feature_name.append(feature_name[index])
        choosen_subsetX_list=[subsetX[x]for x in choosen_feature_name]
        choosen_subsetX=pd.concat(choosen_subsetX_list, axis=1)
        sub_val_list=[valX[ii]for ii in choosen_feature_name]
        sub_valX=pd.concat(sub_val_list, axis=1)

        clf = tree.DecisionTreeClassifier(max_depth=maxDepth, min_samples_leaf=minSamplesLeaf,criterion=criterion)
        clf.fit(choosen_subsetX, subsety)
        val_predict = clf.predict(sub_valX)
        accuracyscore=accuracy_score(valy, val_predict )
        treelist.append(clf)
        oob_accuracy.append(accuracyscore)
        choosen_features_list.append(choosen_feature_name)

        for j in choosen_feature_name:
            sub_valX[j]=np.random.permutation(sub_valX[j])
            newclf = tree.DecisionTreeClassifier(max_depth=maxDepth, min_samples_leaf=minSamplesLeaf,
                                                 criterion=criterion)
            newclf.fit(choosen_subsetX, subsety)
            newval_predict = clf.predict(sub_valX)
            new_accuracyscore = accuracy_score(valy, newval_predict)
            difference=new_accuracyscore-accuracyscore
            #print new_accuracyscore
            #print "difference",difference
            feature_importance[j].append(difference)
    return treelist,choosen_features_list,oob_accuracy,feature_importance

def random_forest_predict(treelist,choosen_features_list,testX):
    label_lsit=[]
    for i in range(0,len(treelist)):
        treemodel=treelist[i]
        features=choosen_features_list[i]
        sub_features_list=[testX[j] for j in features]
        sub_testX=pd.concat(sub_features_list, axis=1)
        predict=treemodel.predict(sub_testX)
        label_lsit.append(predict)

    final_predict=[]
    label_length=len(label_lsit[0])
    labellist_length=len(label_lsit)
    for n in range(label_length):
        templabeln=[]
        for index in range(labellist_length):
            templabeln.append(label_lsit[index][n])
        counter = Counter(templabeln)
        max_count = max(counter.values())
        modelist = [k for k, v in counter.items() if v == max_count]
        mode=modelist[0]
        final_predict.append(mode)
    return final_predict

def getfeature_importance_order(feature_importance):
    featuredic={}
    for feature in feature_importance:
        templist=feature_importance[feature]
        mean_difference=np.mean(templist)
        featuredic[feature]=mean_difference
    sortedfeature=sorted(featuredic.items(), key=lambda x:x[1])
    return sortedfeature

treelist,choosen_features_list,oob_accuracy,feature_importance=random_forest(trainX,trainy,10,"entropy",23,8)
final_predict=random_forest_predict(treelist,choosen_features_list,testX)
finalaccuracy=accuracy_score(testy,final_predict)
mean_oob_accuracy=np.mean(oob_accuracy)

sortedfeature=getfeature_importance_order(feature_importance)
print "#######result for question c########"
print "test data accuracy:",finalaccuracy
print "mean of OOB sample accuracy is ",mean_oob_accuracy
print "OOB sample accuracy list is",oob_accuracy
print "#######result for question d########"
print sortedfeature


















