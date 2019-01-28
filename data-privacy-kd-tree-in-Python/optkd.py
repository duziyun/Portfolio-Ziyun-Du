import pandas as pd
import numpy as np
from scipy.stats import laplace
from sklearn.metrics import accuracy_score
from collections import deque
import matplotlib.pyplot as plt
import sys
def variance(matrix,thres):
    dic={}
    for eachrow in matrix:
        #print eachrow
        t=tuple(eachrow)
        if t in dic:
            dic[t]+=1
        else:
            dic[t]=1
    #print dic
    values=dic.values()
    avg=np.mean(values)

    var=0
    for value in values:
        #print np.absolute(value-avg)
        var+=np.absolute(value-avg)
    #print "var is",var,"when thre is",thres
    if var>thres:
        return False
    else:
        return True

def divide_buckets_iterative(matrix,min,maxiter,varthre):
    res=[]
    num_feature=len(matrix[0])
    sortindex=0
    queue = deque ()
    twohalf=iterativehelper(matrix,sortindex)
    queue.append(twohalf[0])
    queue.append(twohalf[1])
    track=0
    countforuniform=0
    countfornonuniform=0
    sum=0
    while len(queue)!=0 and track<maxiter:
        #print "iteration",track
        #print "sortindex",sortindex
        sortindex = sortindex + 1
        if sortindex == num_feature:
            sortindex = 0
        size=len(queue)
        for i in range(0,size):
            head=queue.popleft()
            #print "len(head)",len(head)
            uniform=variance(head,varthre)
            if(len(head)>0 and len(head)<=min and uniform):
                #print "len(head)>0 and len(head)<min"
                #print head
                #print "uniform:",len(head)
                countforuniform+=1
                res.append(head)
                sum+=len(head)
            else:
                temptwohalf=iterativehelper(head,sortindex)
                if len(temptwohalf[0])!=0:
                    #print temptwohalf[0]
                    queue.append(temptwohalf[0])
                if len(temptwohalf[1])!=0:
                    queue.append(temptwohalf[1])
        track=track+1
    size=len(queue)
    print "after k-d,queue's size is",size
    for i in range(size):
        head = queue.popleft ()
        sum += len(head)
        countfornonuniform+=1
        #print"non-uniform",len(head)
        #print head
        res.append (head)
    print "after k-d partition,len od data is",sum
    print"count:uni",countforuniform
    print"count:non-uni",countfornonuniform
    return res


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
    #mid_num = sorted_matrix[size / 2][sortindex]
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
    print "length of data after reproduce",sum
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

def getkeys(res):
    keys=[]
    for matrix in res:
        temp=[]
        minlist = np.amin (matrix, axis=0)
        maxlist = np.amax (matrix, axis=0)
        temp.append(minlist)
        temp.append(maxlist)
        keys.append(temp)
    return keys

def partition_with_key(matrix,keys):
    dic={}
    for tuple in matrix:
        for i in range(len(keys)):
            minlist=keys[i][0]
            maxlist=keys[i][1]
            count=0
            for j in range(len(minlist)):
                if(tuple[j]>=minlist[j] and tuple[j]<=maxlist[j]):
                    count+=1
                else: break
            if count==len(minlist):
                if i in dic:
                    dic[i].append(tuple)
                else:
                    dic[i]=[]
                    dic[i].append(tuple)
                break
    sum=0
    for i in dic:
        sum+=len(dic[i])
    print "after partition_with_key, length of data is",sum
    #print dic
    fakeres=[]
    for x in dic:
        fakeres.append(dic[x]) 
    return fakeres

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

def answerquery(matrix,querylist):
    num_feature=len(matrix[0])
    count=0
    for i in range(0,len(matrix)):
        find=0
        for j in range(0,num_feature):
            if matrix[i][j]>=querylist[j][0] and matrix[i][j]<=querylist[j][1]:
                find=find+1
        if find==num_feature:
            count=count+1
    return count

def getlable(matrix,fakedata,allquery):
    truecount = []
    fakecount = []
    #allquery = get_random_query (num_q, matrix)
    for query in allquery:
        tempcount = answerquery (matrix, query)
        truecount.append (tempcount)
        tempfakecount = answerquery (fakedata, query)
        fakecount.append (tempfakecount)
    lables=[]
    lables.append(truecount)
    lables.append(fakecount)
    return lables

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


def laplace(epsilon):
    s = np.random.laplace (0, 1 / epsilon, 1)
    return int(s[0])

def plot_variance(oridata,sysdata,allquery):
    varlist=[]
    errorlist=[]
    for i in np.arange(10,200,20):
        print("var=",i)
        varlist.append(i)
        sysres = divide_buckets_iterative (sysdata, len (sysdata) / 100, 50, i)
        syskeys = getkeys (sysres)
        oriparti = partition_with_key (oridata, syskeys)
        fakedata_repro = reproduce (oriparti, 0.5 / 2)
        lables_repro = getlable (oridata, fakedata_repro, allquery)
        error=calculate_rerror (lables_repro, 50)
        errorlist.append(error)
        print("error=",error)
    plt.xlabel ('Variance Thresshold')
    plt.ylabel ('RelativeError')
    plt.plot (varlist, errorlist)
    plt.show ()

def plot_minimumcount(oridata,sysdata,allquery):
    countlist=[]
    errorlist=[]
    for i in np.arange(10,200,20):
        print("bucket number=",i)
        countlist.append(len (sysdata) / i)
        sysres = divide_buckets_iterative (sysdata, len (sysdata) / i, 50, 30)
        syskeys = getkeys (sysres)
        oriparti = partition_with_key (oridata, syskeys)
        fakedata_repro = reproduce (oriparti, 0.5 / 2)
        lables_repro = getlable (oridata, fakedata_repro, allquery)
        error=calculate_rerror (lables_repro, 50)
        errorlist.append(error)
        print("error=",error)
    plt.xlabel ('Minmum count Thresshold')
    plt.ylabel ('RelativeError')
    plt.plot (countlist, errorlist)
    plt.show ()

def plot_height(oridata,sysdata,allquery):
    heightlist=[]
    errorlist=[]
    for i in np.arange(5,12,1):
        print"####################max iterater=",i,"#######################"
        #print("max iterater=",i)
        heightlist.append(i)
        sysres = divide_buckets_iterative (sysdata, len (sysdata) / 100, i, 30)
        syskeys = getkeys (sysres)
        oriparti = partition_with_key (oridata, syskeys)
        fakedata_repro = reproduce (oriparti, 0.5 / 2)
        lables_repro = getlable (oridata, fakedata_repro, allquery)
        error=calculate_rerror (lables_repro, 300)
        errorlist.append(error)
        print("error=",error)
    plt.xlabel ('Height of tree')
    plt.ylabel ('RelativeError')
    plt.plot (heightlist, errorlist)
    plt.show ()


def plot1dhis(matrix,index,title):
    dic={}
    for tuple in matrix:
        if tuple[index] in dic:
            dic[tuple[index]]+=1
        else:
            dic[tuple[index]]=1
    x=[]
    y=[]
    for f in dic:
        x.append(f)
        y.append(dic[f])
    plt.title(title)
    plt.plot (x, y)
    plt.show ()

def plot_base_kd(oridata,allquery):
    epslist=[]
    base=[]
    kd=[]
    baseres = baseline (oridata, len(oridata)/100, 30)
    for i in np.arange(0.1,1.0,0.1):
        print "###########eps=",i,"################"
        epslist.append(i)
        fakebase = reproduce (baseres,i)
        lables_base= getlable (oridata, fakebase, allquery)
        baseerror = calculate_rerror (lables_base, 50)
        print "********base line error",baseerror,"**********"
        base.append(baseerror)
        stepone=reproduce (baseres,i/2)
        sysres = divide_buckets_iterative (stepone, len (stepone) / 100, 30, 30)
        syskeys = getkeys (sysres)
        oriparti = partition_with_key (oridata, syskeys)
        fakedata_kd = reproduce (oriparti, i / 2)
        lables_kd = getlable (oridata, fakedata_kd, allquery)
        kderror = calculate_rerror (lables_kd, 50)
        print "********kd error", kderror, "**********"
        kd.append(kderror)
    plt.xlabel ('Epsilon')
    plt.ylabel ('RelativeError')
    plt.plot (epslist, base)
    plt.plot (epslist, kd)
    plt.legend (['baseline', 'k-d tree'], loc='upper left')
    plt.show ()







if __name__ == "__main__":
    datapath = "data.csv"
    #filename = sys.argv[1]
    oridataframe = pd.read_csv (datapath)
    oridata= oridataframe.as_matrix (columns=None)
    #plot1dhis (oridata,0,"original data")
    allquery = get_random_query (100, oridata)
    plot_base_kd (oridata, allquery)
    """
    sysdatapath = "5fake.csv"
    # filename = sys.argv[1]

    sysdataframe = pd.read_csv (sysdatapath)
    sysdata = sysdataframe.as_matrix (columns=None)
    #plot1dhis (sysdata, 0,"step one data")
    print"length of original data is",len(oridata)
    print"length of sysginal data is", len (sysdata)
    #variance(oridata,1)
    allquery = get_random_query (100, oridata)
    plot_variance (oridata, sysdata, allquery)
    plot_minimumcount(oridata, sysdata, allquery)
    #plot_height(oridata, sysdata, allquery)


    sysres=divide_buckets_iterative (sysdata, len(sysdata)/100, 20, 30)
    #print res
    #fakedata = reproduce (res, 0.1)
    syskeys=getkeys (sysres)
    oriparti=partition_with_key (oridata, syskeys)
    fakedata_repro=reproduce(oriparti, 0.5/2)
    #plot1dhis (fakedata_repro, 0, "step two data")

    
    fakedata_addnoise = add_noise (oriparti, 0.5 / 2)
    allquery=get_random_query(500,oridata)
    lables_repro=getlable(oridata,fakedata_repro,allquery)
    lables_noise = getlable (oridata,fakedata_addnoise,allquery)
    print "repro erroris",calculate_rerror (lables_repro,100)
    print "noise erroris", calculate_rerror (lables_noise,100)

    #plot1dhis (oridata, 0)
    #plot1dhis (fakedata_repro, 0)
    #plot1dhis (fakedata_addnoise, 0)
    #print"length of fake data is", len (fakedata)
    """
