import pandas as pd
import numpy as np
from scipy.stats import laplace
from sklearn.metrics import accuracy_score
from collections import deque
import matplotlib.pyplot as plt
import sys

def divide_buckets_recursion(matrix,min,num_feature,sortindex,res):
    size=len(matrix)
    if size == 0: return
    if size<=min:
        res.append(matrix)
        return
    sorted_matrix=sorted(matrix,key=lambda x: x[sortindex])
    mid_num=sorted_matrix[size/2][sortindex]
    left_matrix=[]
    right_matrix = []
    for i in range(0,size):
        if sorted_matrix[i][sortindex]<=mid_num:
            left_matrix.append(sorted_matrix[i])
        else:
            right_matrix.append(sorted_matrix[i])

    nextsortindex=sortindex+1
    if nextsortindex==num_feature:
        nextsortindex=0


    if len(left_matrix)!=0:  divide_buckets_recursion (left_matrix, min, num_feature, nextsortindex, res)
    if len(right_matrix)!=0: divide_buckets_recursion (right_matrix, min, num_feature, nextsortindex, res)

    return


def baseline(matrix,min,maxiter):
    res=[]
    num_feature=len(matrix[0])
    sortindex=0
    queue = deque ()
    twohalf=iterativehelper(matrix,sortindex)
    queue.append(twohalf[0])
    queue.append(twohalf[1])
    track=0
    while len(queue)!=0 and track<maxiter:
        #print "iteration",track
        #print "sortindex",sortindex
        sortindex = sortindex + 1
        if sortindex == num_feature:
            sortindex = 0
        for i in range(0,len(queue)):
            head=queue.popleft()
            #print "len(head)",len(head)
            if(len(head)>0 and len(head)<=min):
                #print "len(head)>0 and len(head)<min"
                #print head
                res.append(head)
            elif(len(head)>min):
                temptwohalf=iterativehelper(head,sortindex)
                if len(temptwohalf[0])!=0:
                    #print temptwohalf[0]
                    queue.append(temptwohalf[0])
                if len(temptwohalf[1])!=0:queue.append(temptwohalf[1])
        track=track+1

    while len(queue)!=0:
        head = queue.popleft ()
        res.append (head)

    return res

def iterativehelper(matrix,sortindex):
    landr=[]
    size = len (matrix)
    #print "sortindex__________",sortindex
    sorted_matrix = sorted (matrix, key=lambda x: x[sortindex])
    testlist=[]
    for i in range(len(sorted_matrix)):
        testlist.append(sorted_matrix[i][sortindex])
    #print testlist
    mid_num = sorted_matrix[size / 2][sortindex]
    mid_num=(sorted_matrix[size-1][sortindex]+sorted_matrix[0][sortindex])/2
    left_matrix = []
    right_matrix = []
    for i in range (0, size):
        if sorted_matrix[i][sortindex] <= mid_num:
            left_matrix.append (sorted_matrix[i])
        else:
            right_matrix.append (sorted_matrix[i])
    landr.append(left_matrix)
    landr.append (right_matrix)
    return landr

def add_noise(res,epsilon):
    fakedata=[]
    sum=0
    for matrix in res:
        sum=sum+len(matrix)
        #print"length of matrix is: ",len(matrix)
        dif = laplace (epsilon)
        #print"noise is: ",dif
        if dif == 0:
            for tuple in matrix:
                fakedata.append (tuple)
        elif dif<0 and len(matrix)+dif<=0:
            continue
        elif dif>0:
            for tuple in matrix:
                fakedata.append (tuple)
            minlist = np.amin (matrix, axis=0)
            maxlist = np.amax (matrix, axis=0)
            for i in range(0,dif):
                temp=[]
                for i in range(0,len(minlist)):
                    temp.append(np.random.random_integers(minlist[i],maxlist[i]))
                fakedata.append(temp)
        else:
            removeindex=[]
            for i in range (0, dif):
                removeindex.append(np.random.random_integers(0,len(matrix)-1))
            for j in range(0,len(matrix)):
                if j  in removeindex:
                    continue
                else:
                    fakedata.append (matrix[j])
    #print "length of data after divided",sum
    return fakedata

def laplace(epsilon):
    s = np.random.laplace (0, 1 / epsilon, 1)
    return int(s[0])

def get_random_query(num_q,matrix):
    allquery=[]
    minlist = np.amin (matrix, axis=0)
    maxlist = np.amax (matrix, axis=0)
    for i in range(0,num_q):
        temp=[]
        for j in range(0,len(minlist)):
            subtemp=[]
            a=np.random.random_integers(minlist[j],maxlist[j])
            b=np.random.random_integers(minlist[j],maxlist[j])
            while a>b:
                a = np.random.random_integers (minlist[j], maxlist[j])
                b = np.random.random_integers (minlist[j], maxlist[j])
            subtemp.append(a)
            subtemp.append(b)
            temp.append(subtemp)
        allquery.append(temp)
    #print allquery
    return allquery

def answerquery(matrix,querylist,num_feature):
    count=0
    for i in range(0,len(matrix)):
        find=0
        for j in range(0,num_feature):
            if matrix[i][j]>=querylist[j][0] and matrix[i][j]<=querylist[j][1]:
                find=find+1
        if find==3:
            count=count+1
    return count

def getlable(num_q,matrix,fakedata):
    truecount = []
    fakecount = []
    allquery = get_random_query (num_q, matrix)
    for query in allquery:
        tempcount = answerquery (matrix, query, len (matrix[0]))
        truecount.append (tempcount)
        tempfakecount = answerquery (fakedata, query, len (fakedata[0]))
        fakecount.append (tempfakecount)
    lables=[]
    lables.append(truecount)
    lables.append(fakecount)
    return lables

def calculate_accuracy(lables):
    return accuracy_score(lables[0],lables[1])

def calculate_rerror(lables,sbound):
    truecount = lables[0]
    fakecount = lables[1]
    allerror=[]
    for i in range(0,len(truecount)):
        #print "truecount[i]",truecount[i]
        #print "fakecount[i]",fakecount[i]
        dif=abs(truecount[i]-fakecount[i])
        maxvalue=max(truecount[i],sbound)
        #print "dif",dif
        #print "maxvalue",maxvalue
        #print float(float(dif)/float(maxvalue))
        error=float(float(dif)/float(maxvalue))
        #print"error",error
        allerror.append(error)
    #print "----------allerror--------",allerror
    return np.mean(allerror)



def validation(oridata,epsilon,num_q,num_buckets,maxiter,sbound):
    res=divide_buckets_iterative (oridata,len (oridata) / num_buckets,maxiter)
    fakedata=add_noise(res,epsilon)
    lables=getlable(num_q,oridata,fakedata)
    accuracy=calculate_accuracy(lables)
    relativeerror=calculate_rerror(lables,sbound)
    print "********Accuracy score =",accuracy
    print "********RelativeError =", relativeerror


def plot_epsilon(oridata):
    res = divide_buckets_iterative (oridata, len (oridata) / 50, 50)
    epsilonlist=[]
    relist=[]
    for epsilon in np.arange(0.1, 1.0, 0.05):
        print"epsilon is",epsilon
        epsilonlist.append(epsilon)
        print"adding noise"
        fakedata = add_noise (res, epsilon)
        print"getting lables"
        lables = getlable (50, oridata, fakedata)
        relativeerror = calculate_rerror (lables,5)
        print"re is ",relativeerror
        relist.append(relativeerror)
    plt.xlabel ('epsilon')
    plt.ylabel ('RelativeError')
    plt.plot (epsilonlist, relist)
    plt.show ()

def plot_numofbuckets(oridata):
    numlist=[]
    relist = []
    for num_buckets in np.arange(10,100,5):
        print"num fo buckets",num_buckets
        numlist.append(num_buckets)
        print"dividing buckets..."
        res = divide_buckets_iterative (oridata, len (oridata) / num_buckets, 50)
        print"adding noise..."
        fakedata = add_noise (res,0.5)
        print"getting lables"
        lables = getlable (50, oridata, fakedata)
        relativeerror = calculate_rerror (lables, 5)
        print"re is ", relativeerror
        relist.append (relativeerror)
    plt.xlabel ('number of buckets')
    plt.ylabel ('RelativeError')
    plt.plot (numlist, relist)
    plt.show ()

def reproduce(res,epsilon):
    fakedata=[]
    sum=0
    for matrix in res:
        #sum=sum+len(matrix)
        #print"length of matrix is: ",len(matrix)
        dif = laplace (epsilon)
        #print"noise is: ",dif
        if dif == 0:
            sum+=len(matrix)
            for tuple in reproduce_helper(matrix,len(matrix)):
                fakedata.append (tuple)
        elif dif<0 and len(matrix)+dif<=0:
            continue
        else:
            sum+=(len (matrix)+dif)
            for tuple in reproduce_helper(matrix,len(matrix)+dif):
                fakedata.append (tuple)
    print "length of data after divided",sum
    return fakedata

def reproduce_helper(matrix,num):
    fake=[]
    minlist = np.amin (matrix, axis=0)
    maxlist = np.amax (matrix, axis=0)
    for i in range (0, num):
        temp = []
        for i in range (0, len (minlist)):
            temp.append (np.random.random_integers (minlist[i], maxlist[i]))
        fake.append (temp)
    return fake

def plot_sbound(oridata):
    res = divide_buckets_iterative (oridata, len (oridata) / 50, 50)
    fakedata = add_noise (res, 0.5)
    lables = getlable (100, oridata, fakedata)
    sboundlist = []
    relist = []
    for s in np.arange(1,100,1):
        sboundlist.append(s)
        relativeerror = calculate_rerror (lables, s)
        print"re is ", relativeerror
        relist.append (relativeerror)
    plt.xlabel ('sbound')
    plt.ylabel ('RelativeError')
    plt.plot (sboundlist, relist)
    plt.show ()

#oridataframe = pd.read_csv ("data.csv")
# oridata= oridataframe.as_matrix (columns=None)
#plot_numofbuckets(oridata)
#validation(oridata,epsilon,num_q,num_buckets,maxiter,sbound)
#validation(oridata,0.5,100,600,100,1)
#plot_epsilon(oridata)
#plot_sbound(oridata)


if __name__ == "__main__":
    filename = "data.csv"
    #filename = sys.argv[1]
    oridataframe = pd.read_csv (filename)
    oridata= oridataframe.as_matrix (columns=None)
    #print"length of original data is",len(oridata)
    #epsilon = float (sys.argv[2])
    res = baseline(oridata, len (oridata) / 70, 50)
    fakedata = reproduce (res, 0.25)
    #lables = getlable (100,oridata, fakedata)
    #relativeerror = calculate_rerror (lables, 5)
    #print relativeerror



    for i in np.arange(0.1,1.1,0.1):
        outputfilename =str(int(i*10))+"fake"+".csv"
        #print outputfilename
        fakedata = reproduce(res,i/2)
        fakedata = pd.DataFrame (fakedata)
        fakedata.columns = oridataframe.columns
        fakedata.to_csv (outputfilename, index=False)

    """
    num_q=int(sys.argv[4])
    res = divide_buckets_iterative (oridata, len (oridata) / 50, 50)
    fakedata = add_noise (res, epsilon)
    lables = getlable (num_q, oridata, fakedata)
    accuracy = calculate_accuracy (lables)
    relativeerror = calculate_rerror (lables, 5)
    fakedata = pd.DataFrame (fakedata)
    fakedata.columns = oridataframe.columns
    fakedata.to_csv (outputfilename, index=False)
    #print "num of buckets is",len(res)
    #print "Accuracy Score is ",accuracy
    print "Relative Error is",relativeerror
    """

