import os

from sklearn.ensemble import RandomForestClassifier
from util import imagevectorize, getClasses

class RFClassifier:
    def __init__(self,trainingdir,cachedir='cache',k=3):
        print("[*] Creating RFClassifier...")
        self.classes, self.data, self.labels = getClasses(trainingdir,cachedir,limit=200)
        self.clasifier = RandomForestClassifier()
        self.clasifier.fit(self.data, self.labels)
        self.k = k
        print("[+] Classifier created!")

    def classifyVec(self, vec):
        ind = self.clasifier.predict(vec)
        return self.classes[ind[0]]

    def classifyImage(self, imagearr):
        imagevec = imagevectorize(imagearr)
        return self.classifyVec(imagevec)
