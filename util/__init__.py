import numpy
import os
from scipy import misc, stats
import multiprocessing.dummy

RATIO = (36,48)
MULT = 3

IMAGE_X = RATIO[0] * MULT
IMAGE_Y = RATIO[1] * MULT

FEATURES = None

def imagevectorize(imagearr):
    return convertImageToVector(imagearr)

def convertImageToVector(imagearr):
    global FEATURES

    shape = imagearr.shape
    if IMAGE_X > IMAGE_Y and shape[0] < shape[1]:
        imagearr = imagearr.transpose()
    elif IMAGE_Y > IMAGE_X and shape[1] < shape[0]:
        imagearr = imagearr.transpose()

    imagearr = misc.imresize(imagearr,(IMAGE_X,IMAGE_Y))
    shape = imagearr.shape

    vec = []

    # "Gradient of image"
    for fnum in range(2,5):
        tot = 0
        size = 2**fnum
        for i in range(int(shape[0]/size)):
            for j in range(int(shape[1]/size)):
                tot += meanPixDist(i,j,imagearr,size)
        tot /= float(shape[0]*shape[1])
        vec.append(tot)

    # Row differences
    for numcuts in range(2,5):
        vsize = int(shape[1]/numcuts)
        colorscheme = []
        for cut in range(numcuts):
            basecol = imagearr[0,cut*vsize - 1]
            colorscheme.append(averagecolRect(
                (0,cut*vsize),(shape[0],(cut+1)*vsize),
                imagearr,basecol))
        totdistsqrd = 0
        maxdist = 0
        for i in range(len(colorscheme)):
            for j in range(len(colorscheme)):
                d = colorscheme[i] - colorscheme[j]
                if type(d) == numpy.uint8:
                    dsqrd = d ** 2
                else:
                    dsqrd = sum([x ** 2 for x in d])
                if dsqrd > maxdist:
                    maxdist = dsqrd
                totdistsqrd += dsqrd
        vec.append(totdistsqrd)
        vec.append(maxdist)

    # Col differences
    for numcuts in range(2, 5):
        hsize = int(shape[0] / numcuts)
        colorscheme = []
        for cut in range(numcuts):
            basecol = imagearr[cut * hsize - 1, 0]
            colorscheme.append(averagecolRect(
                (cut * hsize, 0), ((cut + 1) * hsize, shape[1]),
                imagearr, basecol))
        totdistsqrd = 0
        maxdist = 0
        for i in range(len(colorscheme)):
            for j in range(len(colorscheme)):
                d = colorscheme[i] - colorscheme[j]
                if type(d) == numpy.uint8:
                    dsqrd = d ** 2
                else:
                    dsqrd = sum([x ** 2 for x in d])
                if dsqrd > maxdist:
                    maxdist = dsqrd
                totdistsqrd += dsqrd
        vec.append(totdistsqrd)
        vec.append(maxdist)

    # Most common color
    size = 1
    for i in range(len(shape)):
        size *= shape[i]
    imagearrflat = imagearr.reshape((size,-1))
    vec += stats.mstats.mode(imagearrflat)

    # Average color
    avgc = sum(imagearrflat)/len(imagearrflat)
    vec += avgc

    # Return vector
    if FEATURES is None:
        FEATURES = len(vec)
    else:
        assert FEATURES == len(vec)
    vec = numpy.array(vec).reshape(1,FEATURES)
    return vec

def inrange(x,y,imgarr):
    shape = imgarr.shape
    return (0<=x<shape[0]) and (0<=y<shape[1])


def averagecolRect(start,end,imgarr,basecol):
    si, sj = start
    fi, fj = end

    ctot = 0*basecol
    counts = 0
    for dx in range(si, fi):
        for dy in range(sj, fj):
            if inrange(dx, dy, imgarr):
                ctot += imgarr[dx,dy]
                counts += 1
    if counts>0:
        return ctot / counts
    else:
        return basecol

def averagecol(i,j,imgarr,size,basecol):
    halfsize = int(size / 2)
    return averagecolRect((i-halfsize,j-halfsize),
                          (i+halfsize,j+halfsize),
                          imgarr,basecol)

def meanPixDist(i,j,imgarr, size):
    selcol = averagecol(i,j,imgarr,size,imgarr[i,j])

    tot = 0
    counted = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx==0 and dy==0: continue

            dcol = averagecol(i + size*dx, j + size*dy, imgarr, size, selcol)
            deltcol = dcol - selcol
            if type(deltcol) == numpy.uint8:
                dsquared = deltcol ** 2
            else:
                dsquared = sum([x ** 2 for x in deltcol])
            tot += dsquared
            counted += 1
    return tot/float(counted)

def processImageTup(tup):
    return processImage(*tup)

def processImage(dirname,classdir,image,cachedir,labels,data,i):
    print("[*]\tLoading from {}".format(image))
    cachename = os.path.join(cachedir, classdir, image)
    imagevec = None

    if os.path.exists(cachename + ".npy"):
        imagevec = numpy.load(cachename + ".npy")

    if imagevec is None or imagevec.shape[1] != FEATURES:
        try:
            imagearr = misc.imread(os.path.join(dirname, classdir, image))
        except:
            return False

        imagevec = imagevectorize(imagearr)

        if not os.path.isdir(os.path.join(cachedir, classdir)):
            os.mkdir(os.path.join(os.path.join(cachedir, classdir)))
        numpy.save(cachename, imagevec)

    return i, imagevec

def imageLabelFilenames(dirname):
    print("[*] Loading training data")
    classes = []
    labels = []
    data = []
    i = 0
    for classdir in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname, classdir)) and classdir[0] != '_':
            print("[*] Loading from {}".format(classdir))
            classes.append(classdir)
            for image in os.listdir(os.path.join(dirname, classdir)):
                labels.append(i)
                data.append(os.path.join(dirname, classdir, image))
            i += 1
    return classes, labels, data

def getClasses(dirname,cachedir,limit=None):
    print("[*] Loading training data")
    classes = []
    labels = []
    data = []
    i = 0
    function_args = []

    if FEATURES is None:
        print("[*] Loading new feature vector for size calculations")
        arr = numpy.zeros((3, 3, 3))
        imagevectorize(arr)

    for classdir in os.listdir(dirname):
        countdown = limit if limit is not None else -1
        if os.path.isdir(os.path.join(dirname,classdir)) and classdir[0]!='_':
            print("[*] Loading from {}".format(classdir))
            classes.append(classdir)
            for image in os.listdir(os.path.join(dirname,classdir)):
                if countdown == 0:
                    break
                countdown -= 1
                #function_args.append((dirname,classdir,image,cachedir,labels,data,i))
                l, v = processImage(dirname,classdir,image,cachedir,labels,data,i)
                labels.append(l)
                data.append(v)
            i += 1

    # p = multiprocessing.dummy.Pool(24)
    # out = p.map(processImageTup, function_args)
    # for tup in out:
    #     labels.append(tup[0])
    #     data.append(tup[1])

    data = numpy.array(data)
    shape = data.shape
    data = data.reshape((shape[0],shape[2]))
    print("[+] Loaded {} objects into memory".format(len(labels)))
    return classes, data, labels