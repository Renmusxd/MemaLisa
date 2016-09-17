import os

from sklearn.ensemble import RandomForestClassifier
from util import vectorize, getClasses

class RFClassifier:
    def __init__(self,trainingdir,cachedir='cache',k=3):
        print("[*] Creating RFClassifier...")
        self.classes, self.data, self.labels = getClasses(trainingdir,cachedir)
        self.clasifier = RandomForestClassifier()
        self.clasifier.fit(self.data, self.labels)
        self.k = k
        print("[+] Classifier created!")

    def classifyVec(self, vec):
        ind = self.clasifier.predict(vec)
        return self.classes[ind[0]]

    def classifyImage(self, imagearr):
        imagevec = vectorize(imagearr)
        return self.classifyVec(imagevec)
