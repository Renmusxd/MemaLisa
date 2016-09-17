import os

from sklearn import neighbors
from knn import vectorize
import numpy
from scipy import misc

def getClasses(dirname):
    classes = []
    labels = []
    data = []
    i = 0
    for classdir in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname,classdir)):
            classes.append(classdir)
            for image in os.listdir(os.path.join(dirname,classdir)):
                imagearr = misc.imread(os.path.join(dirname,classdir,image))
                imagevec = vectorize.convertImageToVector(imagearr)
                labels.append(i)
                data.append(imagevec)
            i += 1

    data = numpy.array(data)
    shape = data.shape
    data = data.reshape((shape[0],shape[1]))
    return classes, data, labels

class KNNClassifier:
    def __init__(self,trainingdir,k=3):
        self.classes, self.data, self.labels = getClasses(trainingdir)
        self.clasifier = neighbors.BallTree(self.data)
        self.k = k

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
        imagevec = vectorize.convertImageToVector(imagearr)
        self.classifyVec(imagevec)


knn = KNNClassifier("../data")
print(knn.classifyVec(numpy.array([200,0]).reshape(1,-1)))

