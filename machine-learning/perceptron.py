from collections import Counter
from sklearn import model_selection
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
with open('spamAssassin.data.txt', 'r') as f:
    worddic={}
    label=[]
    emailid_list=[]
    email_id=0
    for line in f:
        line=line.split()
        emailid_list.append(email_id)
        label.append(int(line[0]))
        worddic[email_id]=set([line[i] for i in range(1,len(line))])
        email_id+=1

for i in range(len(label)):
    if label[i] == 0:
        label[i] = -1
    else:
        label[i] = 1

trainXdic={}
for a in range(0,4200):
    trainXdic[a]=worddic[a]

def get_wordscounter(worddic):
    wordscounter = Counter()
    for id, words_set in worddic.items():
        for word in words_set:
            wordscounter[word]+= 1
    return wordscounter

def get_highfrequency_words_list(wordscounter):
    good_words = []
    for word, count in wordscounter.items():
        if count >= 30:
            good_words.append(word)
    return good_words

def get_data(worddic,good_words):
    data=[]
    for i  in range(len(worddic)):
        each_eamail = []
        for word in good_words:
            if word in worddic[i]:
                each_eamail.append(1)
            else:
                each_eamail.append(0)
        data.append(each_eamail)
    data = np.array(data)
    return data

def sign(f):
    if f>=0:
        s=1
    else:
        s=-1
    return s

def perceptron(data,label,epoch_number):
    n_of_feature=len(data[0])
    n_of_email=len(data)
    W=[0.0001]*n_of_feature
    mistakelist=[]
    newdata = np.zeros((n_of_email, n_of_feature + 1))
    newdata[:, 0:n_of_feature] = data
    newdata[:, -1] = label
    for epoch in range(epoch_number):
        np.random.shuffle(newdata)
        X = newdata[:, 0:n_of_feature]
        y = newdata[:, -1]
        mistake = 0
        for e in range(n_of_email):
            sum = 0
            for v in range(n_of_feature):
                sum += X[e][v] * W[v]
            print "before sign,sum is",sum
            sum = sign(sum)
            print "after sign, sum is",sum
            print "label[e] is",y[e]
            if sum == y[e]:
                continue
            else:
                for each_w in range(n_of_feature):
                    W[each_w] += X[e][each_w] * y[e]
                mistake += 1
        mistakelist.append(mistake)
    return mistakelist,W

def average_perceptron(data,label,epoch_number):
    n_of_feature=len(data[0])
    n_of_email=len(data)
    W=[0.0001]*n_of_feature
    mistakelist=[]
    newdata=np.zeros((n_of_email,n_of_feature+1))
    newdata[:,0:n_of_feature]=data
    newdata[:,-1]=label
    Wsum=[0]*n_of_feature
    Wnumber=0
    for epoch in range(epoch_number):
        np.random.shuffle(newdata)
        X=newdata[:,0:n_of_feature]
        y=newdata[:,-1]
        mistake = 0
        for e in range(n_of_email):
            sum = 0
            for v in range(n_of_feature):
                sum += X[e][v] * W[v]
            print "before sign,sum is",sum
            sum = sign(sum)
            print "after sign, sum is",sum
            print "label[e] is",y[e]
            if sum == y[e]:
                for every_w in range(n_of_feature):
                    Wsum[every_w]+=W[every_w]
                    Wnumber+=1
                continue
            else:
                for each_w in range(n_of_feature):
                    W[each_w] += X[e][each_w] * y[e]
                mistake += 1
                for every_w in range(n_of_feature):
                    Wsum[every_w]+=W[every_w]
                    Wnumber+=1
        mistakelist.append(mistake)
    finalW=[w/Wnumber for w in Wsum]
    return mistakelist,finalW

def predict(X,W):
    number_of_email=len(X)
    number_of_feature=len(X[0])
    predictlist=[]
    for i in range(number_of_email):
        sum=0
        for j in range(number_of_feature):
            sum+=X[i][j]*W[j]
        sum=sign(sum)
        predictlist.append(sum)
    return predictlist

def get_error(ytrue, ypredict):
    accuracy=accuracy_score(ytrue, ypredict)
    error=1-accuracy
    return error

trainwordscounter=get_wordscounter(trainXdic)
good_words=get_highfrequency_words_list(trainwordscounter)
X=get_data(worddic,good_words)
y=label
trainX, testX, trainy, testy = model_selection.train_test_split(X, y, test_size=0.3)
sub_trainX,valX,sub_trainy,valy=model_selection.train_test_split(trainX, trainy, test_size=0.3)

epochlist=range(1,15)

sub_trainXerror=[]
for i in epochlist:
    sub_trainX_mistake, sub_trainX_Weight=perceptron(sub_trainX,sub_trainy,i)
    sub_trainX_predict=predict(sub_trainX,sub_trainX_Weight)
    sub_trainX_error=get_error(sub_trainy,sub_trainX_predict)
    sub_trainXerror.append(sub_trainX_error)

aver_sub_trainXerror=[]
for i in epochlist:
    aver_sub_trainX_mistake, aver_sub_trainX_Weight=average_perceptron(sub_trainX,sub_trainy,i)
    aver_sub_trainX_predict=predict(sub_trainX,aver_sub_trainX_Weight)
    aver_sub_trainX_error=get_error(sub_trainy,aver_sub_trainX_predict)
    aver_sub_trainXerror.append(aver_sub_trainX_error)

val_Xerror=[]
for i in epochlist:
    val_mistake, val_Weight=perceptron(valX,valy,i)
    val_predict=predict(valX,val_Weight)
    val_error=get_error(valy,val_predict)
    val_Xerror.append(val_error)

aver_val_Xerror=[]
for i in epochlist:
    aver_val_mistake, aver_val_Weight=perceptron(valX,valy,i)
    aver_val_predict=predict(valX,aver_val_Weight)
    aver_val_error=get_error(valy,aver_val_predict)
    aver_val_Xerror.append(aver_val_error)


ax = plt.gca()
plt.xlabel('number epoch')
plt.ylabel('error')
ax.plot(epochlist,sub_trainXerror)
ax.plot(epochlist,aver_sub_trainXerror)
ax.plot(epochlist,val_Xerror)
ax.plot(epochlist,aver_val_Xerror)

plt.axis('tight')
plt.title('error with different number of epoch')
plt.legend(['perceptron on train set','averaged perceptron on train set','perceptron on validation set','averaged perceptron on validation set'], loc='upper right')
plt.show()

print "trainX.shape",trainX.shape
print "trainy.shape",len(trainy)
print "testX.shape",testX.shape
print "testy.shape",len(testy)
print "sub_trainX.shape",sub_trainX.shape
print "sub_trainy.shape",len(sub_trainX)
print "valX.shape",valX.shape
print "valy.shape",len(valy)


















