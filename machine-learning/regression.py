import numpy as np
from sklearn import linear_model
from sklearn import model_selection
import math

train_features=[[0]*2500 for _ in range(700)]
train_label=[]

with open("train-features.txt") as f:
    for line in f:
        words = line.split()
        train_features[int(words[0])-1][int(words[1])-1]=+ float(words[2])

with open("train-labels.txt") as l:
    for line in l:
        words=line.split()
        train_label.append(float(words[0]))

trian_features=np.array(train_features)
train_lable=np.array(train_label)

for i in range(len(trian_features)):
    for j in range(len(trian_features[i])):
        trian_features[i][j]=math.log(trian_features[i][j]+0.1)

#best lamda for ridge regression
rid_lambda_range = np.logspace(-1,-5,30)
rid_lambda_accuracy_scores = []
for regParam in rid_lambda_range:
    ridge_lr_model = linear_model.LogisticRegression(C=regParam,penalty='l2')
    rid_accuracy_scores = model_selection.cross_val_score(ridge_lr_model, train_features, train_label, cv=10, scoring='accuracy')
    rid_accuracy_scores=np.array(rid_accuracy_scores)
    rid_lambda_accuracy_scores.append( rid_accuracy_scores .mean())
max_rid_accuracy_score=max(rid_lambda_accuracy_scores)
index_bestlam_rid=rid_lambda_accuracy_scores.index(max_rid_accuracy_score)
bestlam_rid=rid_lambda_range[index_bestlam_rid]
'''print("ridge regression: accuracy scores list of varying lamda is",rid_lambda_accuracy_scores)'''
print("lamda selection: ridge regression: max accuracy score  of varying lamda is %f"%(max_rid_accuracy_score))
print("lamda selection: ridge regression: best lamda is %f"%(bestlam_rid))

#best lamda for lasso regression
las_lambda_range = np.logspace(-0.1,-2,30)
las_lambda_accuracy_scores = []
for regParam in las_lambda_range:
    lasso_lr_model = linear_model.LogisticRegression(C=regParam,penalty='l1')
    las_accuracy_scores = model_selection.cross_val_score(lasso_lr_model, train_features, train_label, cv=10, scoring='accuracy')
    las_accuracy_scores=np.array(las_accuracy_scores)
    las_lambda_accuracy_scores.append( las_accuracy_scores .mean())
max_las_accuracy_score=max(las_lambda_accuracy_scores)
index_bestlam_las=las_lambda_accuracy_scores.index(max_las_accuracy_score)
bestlam_las=las_lambda_range[index_bestlam_las]
'''print("lasso regression: accuracy scores list of varying lamda is",las_lambda_accuracy_scores)'''
print("lamda selection: lasso regression: max accuracy score  of varying lamda is %f"%(max_las_accuracy_score))
print("lamda selection: lasso regression: best lamda is %f"%(bestlam_las))

#compare model
#1>standard regression
std_lr_model = linear_model.LogisticRegression(C=1e5)
std_accuracy_scores = model_selection.cross_val_score(std_lr_model, train_features,train_label, cv=5, scoring='accuracy')
std_accuracy_scores=np.array(std_accuracy_scores)
std_accuracy_score_mean=np.mean(std_accuracy_scores,axis=0)
std_err_rate=1-std_accuracy_score_mean
std_auc_scores=model_selection.cross_val_score(std_lr_model, train_features,train_label, cv=5, scoring='roc_auc')
std_auc_scores=np.array(std_auc_scores)
std_auc_scores_mean=np.mean(std_auc_scores,axis=0)

print ("model comparison: standard regression: accuracy score is %f"%(std_accuracy_score_mean))
print ("model comparison: standard regression: accuracy error rate of is %f"%(std_err_rate))
print ("model comparison: standard regression: AUC is %f"%(std_auc_scores_mean))

#2>ridge regression
ridge_lr_model=linear_model.LogisticRegression(C=bestlam_rid,penalty='l2')
ridge_accuracy_scores = model_selection.cross_val_score(ridge_lr_model, train_features,train_label, cv=5, scoring='accuracy')
ridge_accuracy_scores=np.array(ridge_accuracy_scores)
ridge_accuracy_score_mean=np.mean(ridge_accuracy_scores,axis=0)
ridge_err_rate=1-ridge_accuracy_score_mean
ridge_auc_scores=model_selection.cross_val_score(ridge_lr_model, train_features,train_label, cv=5, scoring='roc_auc')
ridge_auc_scores=np.array(ridge_auc_scores)
ridge_auc_scores_mean=np.mean(ridge_auc_scores,axis=0)
print ("model comparison: ridge regression: accuracy score is %f"%(ridge_accuracy_score_mean))
print ("model comparison: ridge regression: accuracy error rate of is %f"%(ridge_err_rate))
print ("model comparison: ridge regression: AUC is %f"%(ridge_auc_scores_mean))

#3>lasso regression
lasso_lr_model=linear_model.LogisticRegression(C=bestlam_las,penalty='l1')
lasso_accuracy_scores = model_selection.cross_val_score(lasso_lr_model, train_features,train_label, cv=5, scoring='accuracy')
lasso_accuracy_scores=np.array(lasso_accuracy_scores)
lasso_accuracy_score_mean=np.mean(lasso_accuracy_scores,axis=0)
lasso_err_rate=1-lasso_accuracy_score_mean
lasso_auc_scores=model_selection.cross_val_score(lasso_lr_model, train_features,train_label, cv=5, scoring='roc_auc')
lasso_auc_scores=np.array(lasso_auc_scores)
lasso_auc_scores_mean=np.mean(lasso_auc_scores,axis=0)
print ("model comparison: lasso regression: accuracy score is %f"%(lasso_accuracy_score_mean))
print ("model comparison: lasso regression: accuracy error rate of is %f"%(lasso_err_rate))
print ("model comparison: lasso regression: AUC is %f"%(lasso_auc_scores_mean))
