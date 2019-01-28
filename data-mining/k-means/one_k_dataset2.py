from collections import defaultdict
import sys
import math
import random
import numpy as np


def load_data(filename):
    datadic = {}
    with open(filename)as f:
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
    p = [(x1 - x2) ** 2 for (x1, x2) in zip(p1, p2)]
    distance = math.sqrt(sum(p))
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
    for i in range(0, k - 1):
        clusters[features[i]] = [features[i]]
    clusters[features[k - 1]] += features[k:]
    for j in xrange(70):
        newclusters = getclusters(clusters)
        newclusters = updateclusters(newclusters)
        if newclusters == clusters:
            return clusters
        else:
            clusters = newclusters
    return clusters


def costsum(centers):
    sum = 0
    for center in centers.keys():
        for x in centers[center]:
            sum += get_distance_between_points(x, center)
    return sum


def main():
    filename = sys.argv[1]
    k = int(sys.argv[2])
    outputfilename = sys.argv[3]
    data = load_data(filename)
    features = data.keys()
    sum = float('inf')

    clusters = {}

    for i in xrange(30):
        tempclusters = kmeans(features, k)
        ktempsum = costsum(tempclusters)
        random.shuffle(features)
        if ktempsum < sum:
            sum = ktempsum
            clusters = tempclusters

    outputlist = []
    thefile = open(outputfilename, 'w')
    for i in range(1, len(clusters) + 1):
        for center in clusters:
            for x in clusters[center]:
                outputlist.append((i, x))
    for item in outputlist:
        thefile.write("%s\n" % str(item))

    print('Hello,please check the output file in the same folder,thanks!')


if __name__ == "__main__":
    main()