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
print dataDF.columns
#print dataDF.head()
y =dataDF[">50K"]
X = dataDF.drop(dataDF.columns[[-1]], axis=1)
#print X.head()
trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.4)

List=[]
for depth in range(1,31):
    list=[]
    for num_leaf in range(1,51):
        clf = tree.DecisionTreeClassifier(max_depth=depth,min_samples_leaf=num_leaf)
        accuracy_scores = model_selection.cross_val_score(clf, trainX, trainy, cv=4,scoring='accuracy')
        accuracy_score_mean = np.mean(accuracy_scores, axis=0)
        list.append(accuracy_score_mean)
    List.append(list)
print List


maxaccuracy=0
bestdepth=0
bestleaf=0
for i in List:
    leaftrack=0
    for j in i:
        leaftrack+=1
        if j>maxaccuracy:
            maxaccuracy=j
            bestdepth=List.index(i)+1
            bestleaf=leaftrack
print "maxaccuracy is", maxaccuracy
print "best depth is ", bestdepth
print "best leaf is", bestleaf

xlable=[]
ylable=[]
zlable=[]

for i in List:
    leaftrack=0
    for j in i:
        xlable.append(List.index(i)+1)
        ylable.append(leaftrack+1)
        leaftrack+=1
        zlable.append(j)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(xlable, ylable, zlable, c='r', marker='o')

ax.set_xlabel('depth')
ax.set_ylabel('leaf_number')
ax.set_zlabel('accuracy')

plt.show()



