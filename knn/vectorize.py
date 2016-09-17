import numpy
from scipy import misc, stats

RATIO = (36,48)
MULT = 2

IMAGE_X = RATIO[0] * MULT
IMAGE_Y = RATIO[1] * MULT

def convertImageToVector(imagearr):
    shape = imagearr.shape

    if IMAGE_X > IMAGE_Y and shape[0] < shape[1]:
        imagearr = imagearr.transpose()
    elif IMAGE_Y > IMAGE_X and shape[1] < shape[0]:
        imagearr = imagearr.transpose()

    imagearr = misc.imresize(imagearr,(IMAGE_X,IMAGE_Y))

    imagearr = imagearr.reshape((shape[0]*shape[1]*shape[2],))
    vec = [stats.mstats.mode(imagearr)[0],0]
    return vec

