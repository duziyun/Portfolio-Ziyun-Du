




import scipy.sparse as sp
import numpy  as  np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn import model_selection
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.externals.six import StringIO
import pydotplus
from IPython.display import Image
from sklearn import metrics

'''read data and add headers'''
traindata=pd.read_csv("adult.data.txt",sep=',\s', na_values=["?"],engine='python',names = ["age","workclass","fnlwgt","education","education-num","maritalstatus","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","nativecountry","salary"])
#data.drop(data.columns[[1,2,4,7,11]], axis=1, inplace=True)
testdata=pd.read_csv("adult.test.txt",sep=',\s', na_values=["?"],engine='python',names = ["age","workclass","fnlwgt","education","education-num","maritalstatus","occupation","relationship","race","sex","capital-gain","capital-loss","hours-per-week","nativecountry","salary"])
datalist= [traindata,testdata]
data=pd.concat(datalist)
'''processing missing values'''
mean_imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
data["age"]=mean_imp.fit_transform(data[["age"]]).ravel()
data["capital-gain"]=mean_imp.fit_transform(data[["capital-gain"]]).ravel()
data["hours-per-week"]=mean_imp.fit_transform(data[["hours-per-week"]]).ravel()
data["fnlwgt"]=mean_imp.fit_transform(data[["fnlwgt"]]).ravel()
data["education-num"]=mean_imp.fit_transform(data[["education-num"]]).ravel()
data["capital-loss"]=mean_imp.fit_transform(data[["capital-loss"]]).ravel()

'''imputer to process missing value by replacing with mode'''
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

data["occupation"]=ModeImputer().fit_transform(data[["occupation"]])
data["nativecountry"]=ModeImputer().fit_transform(data[["nativecountry"]])
data["education"]=ModeImputer().fit_transform(data[["education"]])
data["race"]=ModeImputer().fit_transform(data[["race"]])
data["sex"]=ModeImputer().fit_transform(data[["sex"]])
data["maritalstatus"]=ModeImputer().fit_transform(data[["maritalstatus"]])
data["workclass"]=ModeImputer().fit_transform(data[["workclass"]])
data["relationship"]=ModeImputer().fit_transform(data[["relationship"]])


sexDummies = pd.get_dummies(data.sex).iloc[:, 1:]
raceDummies = pd.get_dummies(data.race,prefix='race').iloc[:, 1:]
educationDummies=pd.get_dummies(data.education,prefix='education').iloc[:, 1:]
maritalstatusDummies=pd.get_dummies(data.maritalstatus,prefix='maritalstatus').iloc[:, 1:]
nativecountryDummies=pd.get_dummies(data.nativecountry,prefix='nativecountry').iloc[:, 1:]
occupationDummies=pd.get_dummies(data.occupation,prefix='occupation').iloc[:, 1:]
workclassDummies=pd.get_dummies(data.workclass,prefix='workclass').iloc[:, 1:]
relationshipDummies=pd.get_dummies(data.relationship,prefix='relationship').iloc[:, 1:]
salaryDummies=pd.get_dummies(data.salary).iloc[:, 1:]
dataDF = pd.concat([data,sexDummies,educationDummies,maritalstatusDummies,raceDummies,nativecountryDummies,occupationDummies,workclassDummies,relationshipDummies,salaryDummies], axis=1)
dataDF.drop(dataDF.columns[[1,3,5,6,7,8,9,13,14]], axis=1, inplace=True)
#print dataDF.columns
#print dataDF.head()
y =dataDF[">50K"]
X = dataDF.drop(dataDF.columns[[-1]], axis=1)
#print X.head()
trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.4)
clf = tree.DecisionTreeClassifier(max_depth=11,min_samples_leaf=24)
clf.fit(trainX, trainy)
yTrainHat=clf.predict(trainX)
yTestHat = clf.predict(testX)
print "test report", metrics.classification_report(testy, yTestHat)

dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data,
                     feature_names=trainX.columns,
                     class_names=["more than 5000", "less than 5000"],
                     filled=True, rounded=True, special_characters=True,max_depth=3)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.write_pdf("tree_picture"))





