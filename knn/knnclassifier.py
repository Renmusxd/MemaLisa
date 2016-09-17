import os

from sklearn import neighbors
from util import imagevectorize, getClasses
import numpy
from scipy import misc

class KNNClassifier:
    def __init__(self,trainingdir,cachedir='cache',k=3):
        print("[*] Creating KNN Classifier...")
        self.classes, self.data, self.labels = getClasses(trainingdir,cachedir)
        self.clasifier = neighbors.BallTree(self.data)
        self.k = k
        print("[+] Classifier created!")

    def classifyVec(self, vec):
        dist, ind = self.clasifier.query(vec,k=self.k)
        classes = [self.classes[self.labels[i]] for i in ind[0]]
        buckets = [0 for x in range(len(self.classes))]
        highest_count = 0
        highest_class = None
        for c in classes:
            for i in range(len(self.classes)):
                if c == self.classes[i]:
                    buckets[i] += 1
                    if buckets[i]>highest_count:
                        highest_class = c
                        highest_count = buckets[i]
                    break
        return highest_class

    def classifyImage(self, imagearr):
        imagevec = imagevectorize(imagearr)
        return self.classifyVec(imagevec)
