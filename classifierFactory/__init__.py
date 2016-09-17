from knn import knnclassifier
from randomforest import rfclassifier

TRAINING_DIR = "data"

def getRFClassifier():
    return rfclassifier.RFClassifier(TRAINING_DIR)

def getKNNClassifier():
    return knnclassifier.KNNClassifier(TRAINING_DIR)