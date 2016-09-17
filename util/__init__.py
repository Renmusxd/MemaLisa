import numpy
import os
from scipy import misc, stats

RATIO = (36,48)
MULT = 2

IMAGE_X = RATIO[0] * MULT
IMAGE_Y = RATIO[1] * MULT

ADJ_MAT = []
for i in [-1,0,1]:
    for j in [-1,0,1]:
        if not (j==0 and i==0):
            ADJ_MAT.append((i,j))

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

    # "Gradient of image"
    tot = 0
    for i in range(shape[0]):
        for j in range(shape[1]):
            tot += meanPixDist(i,j,imagearr)
    tot /= float(shape[0]*shape[1])

    imagearr = imagearr.reshape((shape[0]*shape[1]*shape[2],-1))
    vec = [stats.mstats.mode(imagearr)[0],tot]
    return vec

def meanPixDist(i,j,imgarr):
    selcol = imgarr[i,j]
    shape = imgarr.shape

    tot = 0
    counted = 0
    for adj in ADJ_MAT:
        di = i+adj[0]
        dj = j+adj[1]
        if (0<=di<shape[0]) and (0<=dj<shape[1]):
            dcol = imgarr[di,dj]
            deltcol = dcol - selcol
            dsquared = sum([x**2 for x in deltcol])
            tot += dsquared
            counted += 1
    return tot/float(counted)



def getClasses(dirname):
    print("[*] Loading training data")
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
    print("[+] Loaded {} objects into memory".format(len(labels)))
    return classes, data, labels