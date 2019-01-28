from collections import Counter, defaultdict
import sys
import math
import numpy as np
from sklearn.metrics import roc_auc_score

def getlikelihood(lable,feature):
    lablelist=getlablelist(lable)
    priors=getpriors(lable)
    likelihood = defaultdict(Counter)
    clist=[]
    with open(feature) as f:
        i=1
        for line in f:
            words=line.split()
            if int(words[0]) == i:
                likelihood[lablelist[i - 1]][words[1]] += int(words[2])
            else:
                i=i+1
                likelihood[lablelist[i - 1]][words[1]] += int(words[2])
    return likelihood


def getlablelist(lable):
    likelihood = defaultdict(Counter)
    lablelist=[]
    with open(lable) as l:
        for line in l:
            words=line.split()
            lablelist.append(int(words[0]))
    return lablelist

def getpriors(lable):
    priors = Counter()
    lablelist=getlablelist(lable)
    for i in lablelist:
        priors[i] += 1
    return priors

def gettestfeature(filename):
    with open(filename) as f:
        testflist= defaultdict(Counter)
        i=1
        for line in f:
            words=line.split()
            if int(words[0]) == i:
                testflist[i - 1][words[1]] = int(words[2])
            else:
                i=i+1
                testflist[i - 1][words[1]] = int(words[2])
    return testflist

def classify_bayesian(singeldata, priors, likelihood):
    max_class=(-1E10, '')
    for c in priors:
        p = math.log(priors[c])
        n = float(sum(likelihood[c].values()))
        for wordid in singeldata:
            p = p + math.log(max(1E-10, likelihood[c][wordid] / n))
        if p > max_class[0]:
            max_class = (p, c)
    return max_class[1]

def getyscore(singeldata,priors,likelihood):
    n1 = float(sum(likelihood[1].values()))
    n0 = float(sum(likelihood[0].values()))
    p1 = math.log(priors[1])
    p0 = math.log(priors[0])
    for wordid in singeldata:
        p1 = p1 + math.log(max(1E-10, likelihood[1][wordid] / n1))
        p0 = p0 + math.log(max(1E-10, likelihood[0][wordid] / n0))
    A=max(p1,p0)
    Deominator=A+math.log(math.exp(p1-A)+math.exp(p0-A))
    return p1-Deominator

def main():
    trainfeature=sys.argv[1]
    trainlabel=sys.argv[2]
    testfeature = sys.argv[3]
    testlable=sys.argv[4]
    testlablelist=getlablelist(testlable)
    trainlablelist=getlablelist(trainlabel)
    priors=getpriors(trainlabel)
    likelihood=getlikelihood(trainlabel,trainfeature)
    testflist=gettestfeature(testfeature)
    result=[]
    num_correct = 0
    y_scores=[]

    for i in testflist:
        singeldata=testflist[i]
        oneresult=classify_bayesian(singeldata, priors, likelihood)
        result.append(oneresult)
        a=getyscore(singeldata,priors,likelihood)
        y_scores.append(a)

        if oneresult == testlablelist[i-1]:
            num_correct += 1
    print  result
    print ("there is %d correctly out of %d and the accuracy is %f"%(num_correct,len(testlablelist),float(num_correct) / len(testlablelist)))

    y_true_test = np.array(testlablelist)
    y_true_train= np.array(trainlablelist)
    print (" 'AUC' is %f"%(roc_auc_score(y_true_train, y_scores)))


if __name__ == "__main__":
    main()






