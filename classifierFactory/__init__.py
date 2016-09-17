from knn import knnclassifier

TRAINING_DIR = "data"

def getClassifier():
    return knnclassifier.KNNClassifier(TRAINING_DIR)