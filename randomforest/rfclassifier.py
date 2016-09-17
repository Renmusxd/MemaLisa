import os

from sklearn.ensemble import RandomForestClassifier
from util import vectorize, getClasses

class RFClassifier:
    def __init__(self,trainingdir,k=3):
        self.classes, self.data, self.labels = getClasses(trainingdir)
        self.clasifier = RandomForestClassifier()
        self.clasifier.fit(self.data, self.labels)
        self.k = k

    def classifyVec(self, vec):
        ind = self.clasifier.predict(vec)
        return self.classes[ind[0]]

    def classifyImage(self, imagearr):
        imagevec = vectorize(imagearr)
        return self.classifyVec(imagevec)
