from collections import defaultdict
import math
import random
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    datadic = {}
    with open('data2.txt')as f:
        features = []
        labels = []
        for line in f:
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.replace('?', '0')
            words = line.split(',')
            features.append(tuple(map(float, line.split(',')[1:])))
            features = [i for i in features if i != ( )]
            labels.append([line.split(',')[0]])
            datadic[words[0]] = [word for word in words if word != words[0]]
    return dict(zip(features, labels))

def get_distance_between_points(p1, p2):
    p =[(x1 - x2)**2 for (x1, x2) in zip(p1,p2)]
    distance=math.sqrt(sum(p))
    return distance

def getclusters(clusters):
    newclusters = defaultdict(list)
    for cluster in clusters.values():
        for x in cluster:
            temp = float('inf')
            for c in clusters.keys():
                distance = get_distance_between_points(x, c)
                if distance < temp:
                    temp = distance
                    min = c
            newclusters[min].append(x)
    return newclusters

def updateclusters(clusters):
    newclusters = {}
    for center in clusters.keys():
        newclusters[tuple(np.mean(clusters[center], axis=0))] = clusters[center]
    return newclusters

def kmeans(features, k):
    clusters = defaultdict(list)
    for i in range(0,k-1):
        clusters[features[i]]=[features[i]]
    clusters[features[k-1]] += features[k:]
    for j in xrange(50):
        newclusters = getclusters(clusters)
        newclusters = updateclusters(newclusters)
        if  newclusters==clusters:
            return clusters
        else:
            clusters = newclusters
    return clusters

def costsum(centers):
    sum=0
    for center in centers.keys():
        for x in centers[center]:
            sum +=  get_distance_between_points(x, center)
    return sum

def main():
    data = load_data()
    features = data.keys()
    sum=float('inf')
    klist=[]
    costlist=[]
    for k in range(2,20):
        for i in xrange(20):
            random.shuffle(features)
            tempclusters = kmeans(features, k)
            ktempsum = costsum(tempclusters)
            if ktempsum < sum:
                sum = ktempsum
                clusters=tempclusters
        klist.append(k)
        costlist.append(sum)

    outputlist=[]
    thefile = open('output_for_optimal_k.txt', 'w')
    for i in range(1,len(clusters)+1):
        for center in clusters:
            for x in clusters[center]:
                outputlist.append((i, x))
    for item in outputlist:
        thefile.write("%s\n" % str(item))
    print ("min SSE value is %f and k equals to %s"%(sum,len(clusters)) )
    print costlist

    import matplotlib.pyplot as plt
    plt.xlabel('number of k')
    plt.ylabel('cost of clusters')
    plt.title('relationship between number of k and cost')
    plt.plot(klist, costlist)
    plt.axis([2, len(clusters) + 1, 0, 3* sum])
    plt.show()

if __name__ == "__main__":
    main()