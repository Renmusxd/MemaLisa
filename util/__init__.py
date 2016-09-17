import numpy
import os
from scipy import misc, stats

RATIO = (36,48)
MULT = 2

IMAGE_X = RATIO[0] * MULT
IMAGE_Y = RATIO[1] * MULT

def vectorize(imagearr):
    return convertImageToVector(imagearr)

def convertImageToVector(imagearr):
    shape = imagearr.shape
    if IMAGE_X > IMAGE_Y and shape[0] < shape[1]:
        imagearr = imagearr.transpose()
    elif IMAGE_Y > IMAGE_X and shape[1] < shape[0]:
        imagearr = imagearr.transpose()

    imagearr = misc.imresize(imagearr,(IMAGE_X,IMAGE_Y))

    shape = imagearr.shape

    imagearr = imagearr.reshape((shape[0]*shape[1]*shape[2],-1))
    vec = [stats.mstats.mode(imagearr)[0],0]
    return vec

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
                imagevec = vectorize(imagearr)
                labels.append(i)
                data.append(imagevec)
            i += 1

    data = numpy.array(data)
    shape = data.shape
    data = data.reshape((shape[0],shape[1]))
    return classes, data, labels