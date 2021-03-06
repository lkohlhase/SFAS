import generate_data
import numpy as np
import mdp
import matplotlib.pyplot as plt
import random
import sklearn.cluster as cluster
import toydatatests
import matplotlib.patches as patches
import pickle
import os
import dtw
import time
import math
from procedures import *

def second_attempt(): #1 34, 2 34, 3 34, 5 34, 6 34 
    for j in range(60):
        print(j+3)
        samplenum=j+3
        sample=6
        data=generate_data.readSample(sample)
        transitions=generate_data.segmentations['86 0'+str(sample)]
        timesteps=20
        numfeatures=3
        testdata = np.array([k[:samplenum] for k in data[:transitions[1]['upper']]])
        sfanode=mdp.nodes.SFANode()
        expansionnode=mdp.nodes.PolynomialExpansionNode(2)
        testdata=expansionnode.execute(testdata)
        print(testdata.shape)
        sfanode.train(testdata)
        sfanode.stop_training()
        feature_values=sfanode.execute(testdata,n=3)
        distmatrix=generate_data.simmatrix2(numfeatures,feature_values,timesteps)
        clusterer=cluster.SpectralClustering(n_clusters=2,affinity='precomputed')
        binarylist=clusterer.fit_predict(distmatrix)
        binarylist=generate_data.reorder(binarylist)
        boundary=generate_data.find_boundary(binarylist)
        print(boundary)
def third_attempt():


    for j in range(9):
        file = open('valuelog'+str(j+1)+'.txt', 'w')
        print('Looking at sample '+str(j+1))
        file.write('Looking at sample'+str(j+1)+'\n')
        transitions = generate_data.segmentations['86 0' + str(j+1)]
        file.write("We are expecting a boundary from "+str(transitions[0]['lower'])+' to '+str(transitions[0]['upper'])+" \n")

        for i in range(40):
            print('Condensed down to'+str(i+3))
            sample=j+1
            timesteps = 20
            numfeatures = 3
            reducenumber=i+3
            numclusters=2
            boundary,binarylist,feature_values=GetClustering(numclusters,numfeatures, reducenumber, sample, timesteps)
            file.write('Reducing from 62 to '+str(reducenumber)+'\n')
            file.write(str(boundary)+'\n')
        file.close()


def windowsizetest():
    tobesaved={}
    boundariesmiddle2=[]
    boundarieslower2=[]
    boundariesupper2=[]
    boundariesterrible2=[]
    plt.figure()
    numsamples=7
    for j in range(numsamples):
        boundariesmiddle2.append([])
        boundarieslower2.append([])
        boundariesupper2.append([])
        boundariesterrible2.append([])
        sample=j+3
        print('Working on sample '+str(sample))
        data = generate_data.readSample(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper'] for x in transitions]
        testdatamiddle = np.array([k for k in data[:transitions[1]]])
        testdatalower = np.array([k for k in data[:(transitions[1]+transitions[0])/2]])
        testdataupper = np.array([k for k in data[:(transitions[1]+transitions[2])/2]])
        testdataterrible = np.array([k for k in data[:transitions[2]]])
        plt.subplot(numsamples, 4,j*4+1 )
        print('Working on the right windowsize')
        for i in range(5):
            boundariesmiddle2[-1].append([])
            reducenumber=10+i*5
            print('Reducing from 62 to '+str(reducenumber))
            clusteringdata=GetClusteringFromData(testdatamiddle,numclusters=2,numfeatures=3,reducenumber=reducenumber,timesteps=20)
            boundariesmiddle2[-1][-1].append(clusteringdata[0])
            boundariesmiddle=clusteringdata[0][0]
            plt.plot(boundariesmiddle,reducenumber,'x')
        plt.plot([0,0],[0,35])
        plt.plot([transitions[0],transitions[0]],[0,35],'b')
        plt.plot([transitions[1],transitions[1]],[0,35],'r')
        plt.subplot(numsamples,4,j*4+2)
        print('Working on a too small windowsize')
        for i in range(5):
            boundarieslower2[-1].append([])
            reducenumber=10+i*5
            print('Reducing from 62 to '+str(reducenumber))
            clusteringdata = GetClusteringFromData(testdatalower, numclusters=2, numfeatures=3, reducenumber=reducenumber, timesteps=20)
            boundarieslower2[-1][-1].append(clusteringdata[0])
            boundarieslower = clusteringdata[0][0]
            plt.plot(boundarieslower,reducenumber,'x')
        plt.plot([0,0],[0,35])
        plt.plot([transitions[0],transitions[0]],[0,35],'b')
        plt.plot([transitions[1],transitions[1]],[0,35],'r')
        plt.plot([(transitions[1]+transitions[0])/2,(transitions[1]+transitions[0])/2],[0,35],'g')
        plt.subplot(numsamples,4,j*4+3)
        print('Working on a too big windowsize')
        for i in range(5):
            boundariesupper2[-1].append([])
            reducenumber=10+i*5
            print('Reducing from 62 to '+str(reducenumber))
            clusteringdata = GetClusteringFromData(testdataupper, numclusters=2, numfeatures=3, reducenumber=reducenumber, timesteps=20)
            boundariesupper2[-1][-1].append(clusteringdata[0])
            boundariesupper = clusteringdata[0][0]
            plt.plot(boundariesupper,reducenumber,'x')
        plt.plot([0,0],[0,35])
        plt.plot([transitions[0],transitions[0]],[0,35],'b')
        plt.plot([transitions[1],transitions[1]],[0,35],'r')
        plt.plot([(transitions[1]+transitions[2])/2,(transitions[1]+transitions[2])/2],[0,35],'g')
        plt.subplot(numsamples,4,j*4+4)
        print('Working on a terrible windowsize')
        for i in range(5):
            boundariesterrible2[-1].append([])
            reducenumber=10+i*5
            print('Reducing from 62 to '+str(reducenumber))
            clusteringdata = GetClusteringFromData(testdataterrible, numclusters=2, numfeatures=3, reducenumber=reducenumber, timesteps=20)
            boundariesterrible2[-1][-1].append(clusteringdata[0])
            boundariesterrible = clusteringdata[0][0]
            plt.plot(boundariesterrible,reducenumber,'x')
        plt.plot([0,0],[0,35])
        plt.plot([transitions[0],transitions[0]],[0,35],'b')
        plt.plot([transitions[1],transitions[1]],[0,35],'r')
        plt.plot([(transitions[2]+transitions[2])/2,(transitions[2]+transitions[2])/2],[0,35],'g')
    plt.show()
    tobesaved['boundariesmiddle']=boundariesmiddle2
    tobesaved['boundariesupper']=boundariesupper2
    tobesaved['boundarieslower']=boundarieslower2
    tobesaved['boundariesterrible']=boundariesterrible2
    pickle.dump(tobesaved,open('Logs/windowsizetest','wb'))
def minibatchprettypicture():
    tobesaved=[['Transition points found by minibatch'],['Errors for those transitions']]
    counter=logcounter('prettypicturecounter')
    windowsize=[1200,2000,2000,2000,2000,1800,2000,1800,2000]
    boundaries=[]
    boundaries2=[]
    errors2=[]
    axis=[]
    numsamples=7
    #plt.figure()
    for j in range(numsamples):
        boundaries2.append([])
        errors2.append([])
        sample = j + 3
        #plt.subplot(numsamples,1,j+1)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        boundaries.append([])
        axis.append([])
        print('Looking at sample'+str(sample)+'\n')
        for i in range(5):
            reducenumber=10+i*5
            print('Reducing from 62 to '+str(reducenumber))
            bndrys,errors=minibatchfromsample(sample, windowsize[sample - 1], reducenumber=reducenumber)
            boundaries[-1].append(bndrys)
            axis[-1].append([reducenumber for i in boundaries[-1][-1]])
            for k in range(len(bndrys)):
                value=50*(1-float(errors[k]))
                print('*'*50)
                print(value)
                #plt.scatter(bndrys[k],reducenumber,'x',s=value)
            boundaries2[-1].append(boundaries)
            errors2[-1].append(errors)
        transitionaxis=[x['middle'] for x in transitions]
        for point in transitionaxis:
            plt.plot([point,point],[0,35],'b')
    #plt.show()
    tobesaved.append(boundaries2)
    tobesaved.append(errors2)

    pickle.dump(tobesaved, open('Logs/prettypicture' + str(counter), 'wb'))


def minibatchtest():
    for i in range(4):
        print(10+i*5)
        print(minibatchfromsample(5, 1400, reducenumber=(10 + i * 5)))
def GetClustering(numclusters=2,numfeatures=3, reducenumber=10, sample=1, timesteps=20):
    '''
    Takes parameters and automatically finds boundary, featurevalues, and clustering for the first points from the CMU data set
    :param numclusters: How many clusters it makes
    :param numfeatures: Number of features to be used in vectors for similarity matrix
    :param reducenumber: number of dimensions to reduce data to
    :param sample: What sample we're looking at
    :param timesteps: Number of timesteps to be used in vectors for similarity matrix
    :return: feature values, list of clustering and boundary
    '''
    feature_values = GetSFAValues(numclusters,numfeatures, reducenumber, sample)
    distmatrix = generate_data.simmatrix2(numfeatures, feature_values, timesteps)
    clusterer=cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
    binarylist=clusterer.fit_predict(distmatrix)
    binarylist=generate_data.reorder(binarylist)
    if numclusters==2:
        boundary=generate_data.find_boundary(binarylist)
    else:
        boundary=generate_data.find_boundariesold(binarylist)
    return boundary,binarylist,feature_values


def minibatchfromsample(sample, steplength, numfeatures=3, reducenumber=10, timesteps=10, numclusters=2):
    print(reducenumber)
    data=generate_data.readSample(sample)
    transitions=generate_data.segmentations['86 0'+str(sample)]
    currentmiddleboundary=0
    boundaries=[]
    errors=[]
    while (currentmiddleboundary+steplength<len(data)):
        currentdata=data[currentmiddleboundary:currentmiddleboundary+steplength]
        currentdata=np.array([k for k in currentdata])
        boundary,binlist,featurevalues=GetClusteringFromData(currentdata,reducenumber=reducenumber)

        currentmiddleboundary+=boundary[0]
        errors.append(boundary[1])
        print(currentmiddleboundary)
        print(boundary )
        boundaries.append(currentmiddleboundary)
    return boundaries,errors

def GetSFAValuesFromData(data,numfeatures=3, reducenumber=10):
    testdata=pca_reduce(data,reducenumber)
    sfanode=mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata = expansionnode.execute(testdata)
    print(testdata.shape)
    sfanode.train(testdata)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata, n=numfeatures)
    return feature_values

def GetClusteringFromData(data, numclusters=2,numfeatures=3, reducenumber=10, timesteps=20):
    '''
    Same as GetClustering, except inputs arbitrary data. Has to be formatted correctly though, so big np.array() with rows being data points
    '''
    featurevalues=GetSFAValuesFromData(data,numfeatures,reducenumber)
    distmatrix = generate_data.simmatrix2(numfeatures, featurevalues, timesteps)
    clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
    binarylist = clusterer.fit_predict(distmatrix)
    binarylist = generate_data.reorder(binarylist)
    if numclusters == 2:
        boundary = generate_data.find_boundary(binarylist)
    else:
        boundary = generate_data.find_boundariesold(binarylist)
    return boundary, binarylist, featurevalues

def GetSFAValues(numclusters=2,numfeatures=3, reducenumber=10, sample=1):
    data = generate_data.readSample(sample)
    transitions = generate_data.segmentations['86 0' + str(sample)]
    testdata = np.array([k for k in data[:transitions[numclusters-1]['upper']]])
    testdata = pca_reduce(testdata, reducenumber)
    sfanode = mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata = expansionnode.execute(testdata)
    sfanode.train(testdata)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata, n=numfeatures)
    return feature_values


def pca_reduce(testdata,numdimensions):
    '''
    Takes testdata in the form needed for mdp nodes and then uses pca to reduce it down to numdimensions
    '''
    pcanode=mdp.nodes.PCANode(output_dim=numdimensions)
    pcanode.train(testdata)
    pcanode.stop_training()
    return pcanode.execute(testdata)
def first_attempt():
    file=open('valuelog.txt' ,'w')

    for j in range(15):
        file.write('*'*50)
        file.write('New File here')
        file.write(str(j))
        for i in range(15):
            print(i+10)
            file.write(str(i+10))
            samplenum=j+1
            data=generate_data.readSample(samplenum)
            if samplenum<10:
                transitions=generate_data.segmentations['86 0'+str(samplenum)]
            else:
                transitions=generate_data.segmentations['86 '+str(samplenum)]
            timesteps=20
            numfeatures=3
            testdata=np.array([k[:10+i] for k in data[:transitions[1]['upper']]])
            sfanode=mdp.nodes.SFANode()
            expansionnode=mdp.nodes.PolynomialExpansionNode(2)
            testdata=expansionnode.execute(testdata)
            print(testdata.shape)
            file.write(str(testdata.shape))
            sfanode.train(testdata)
            sfanode.stop_training()
            feature_values=sfanode.execute(testdata,n=3)
            distmatrix=generate_data.simmatrix2(numfeatures,feature_values,timesteps)
            plt.matshow(distmatrix)
            clusterer=cluster.SpectralClustering(n_clusters=2,affinity='precomputed')
            binarylist=clusterer.fit_predict(distmatrix)
            binarylist=generate_data.reorder(binarylist)
            print(binarylist)
            boundary=generate_data.find_boundary(binarylist)
            print(boundary)
            file.write(str(boundary))


def manywindows():
    counter=logcounter('manywindowscounter')
    tobesaved=[['testdata','feature_values','binarylist']]
    num_cluster=10
    blksize=250
    testdata,boundaries=generate_data.toydata2(blocksize=blksize,numblocks=num_cluster,noise=0.0001,numfeatures=20)
    tobesaved.append(testdata)
    sfanode=mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata2 = expansionnode.execute(testdata)

    print(testdata2.shape)
    sfanode.train(testdata2)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata2, n=5)
    tobesaved.append(feature_values)
    distmatrix = generate_data.simmatrix2(5, feature_values, 20)
    plt.matshow(distmatrix)
    plt.show()
    clusterer = cluster.SpectralClustering(n_clusters=num_cluster, affinity='precomputed')
    binarylist = clusterer.fit_predict(distmatrix)
    binarylist = generate_data.reorder(binarylist)
    tobesaved.append(binarylist)
    tobesaved.append(distmatrix)
    pickle.dump(tobesaved,open('Logs/manywindows'+str(counter),'wb'))
    plt.plot(range(len(binarylist)),binarylist,'x')
    for boundary in boundaries:
        plt.plot([boundary,boundary],[0,10])
    plt.show()
    # print(binarylist)
    # plt.figure(1)
    # plt.plot(range(len(binarylist)),binarylist,'x')
    # plt.figure(2)
    # toydatatests.show_features(testdata,feature_values)
    # plt.show()
    # print(minibatch(testdata,2*blksize,numfeatures=5))


def logcounter(filename):
    file = open('Logs/'+filename, 'r')
    counter = int(file.read())
    file.close()
    file = open('Logs/'+filename, 'w')
    file.write(str(counter + 1))
    file.close()
    return counter


def numfeaturesminibatch():
    num_cluster = 10
    noises=[0.0001,0.01,0.02,0.03,0.04,0.05,0.06]
    blksize = 500
    plt.figure()
    for j in range(len(noises)):
        testdata2, boundaries = generate_data.toydata2(blocksize=blksize, numblocks=num_cluster, noise=noises[j], numfeatures=30)
        plt.subplot(len(noises), 1, j + 1)
        plt.title('Noise: '+str(noises[j]))
        for i in range(5):
            numfeatures = 5 + i * 3
            testdata=np.array([k[:numfeatures] for k in testdata2])
            print('Working on noise '+str(noises[j]))
            asdf = minibatch(testdata, 2 * blksize, reducenumber=5)
            for i in boundaries:
                plt.plot([i,i],[0,30])
            for i in asdf:
                plt.plot(i,numfeatures,'x')
    plt.show()
def windowsize2():
    dic=pickle.load(open('Logs/windowsizetest','rb'))

    plt.figure()
    for i in range(7):
        sample = i + 3
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper'] for x in transitions]
        plt.subplot(7,4,i*4+1)
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        for j in range(5):
            reducenumber=10+j*5
            boundary=dic['boundariesmiddle'][i][j]
            print(boundary[0][1])
            plt.scatter(boundary[0][0],reducenumber,marker='x',s=boundary[0][1]**2*1000+20)
        plt.subplot(7,4,i*4+2)
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        plt.plot([(transitions[1] + transitions[0]) / 2, (transitions[1] + transitions[0]) / 2], [0, 35], 'g')
        for j in range(5):
            reducenumber=10+j*5
            boundary=dic['boundarieslower'][i][j]
            print(boundary[0][1])
            plt.scatter(boundary[0][0],reducenumber,marker='x',s=boundary[0][1]**2*1000+20)
        plt.subplot(7,4,i*4+3)
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        plt.plot([(transitions[1] + transitions[2]) / 2, (transitions[1] + transitions[2]) / 2], [0, 35], 'g')
        for j in range(5):
            reducenumber=10+j*5
            boundary=dic['boundariesupper'][i][j]
            print(boundary[0][1])
            size=(1-boundary[0][1])**2*1000
            plt.scatter(boundary[0][0],reducenumber,marker='x',s=boundary[0][1]**2*1000+20)
        plt.subplot(7,4,i*4+4)
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        plt.plot([(transitions[2] + transitions[2]) / 2, (transitions[2] + transitions[2]) / 2], [0, 35], 'g')
        for j in range(5):
            reducenumber=10+j*5
            boundary=dic['boundariesterrible'][i][j]
            print(boundary[0][1])
            plt.scatter(boundary[0][0],reducenumber,marker='x',s=boundary[0][1]**2*1000+20)
    plt.show()
def prettypicture2():
    dict=pickle.load(open('Logs/prettypicture10','rb'))
    plt.figure()
    for i in range(7):
        pass
    plt.show()
def first_attempt_fix_valuelog():
    file=open('valuelog.txt','r')
    file2=open('valuelog2.txt','w')
    asdf=file.readline()
    kk=asdf.split('here')
    kkk=[i.split(')') for i in kk]
    print(kkk[1])
    for orders in kkk:
        for i in orders:
            file2.write(str(i))
            file2.write('\n')

def exactboundaries():
    tobesaved={}
    tobesaved['description']='tobesaved[i][j] contains a list of boundaries for sample i+3, with j+3 slow features'
    for i in range(7):
        sample=i+3
        data = generate_data.readSample(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]

        print('Working on sample '+str(sample))
        tobesaved[i]=[]
        for j in range(5):
            currentmiddleboundary = 0
            tobesaved[i].append([])
            reducenumber=10+j*5
            print('Using '+str(reducenumber)+' as reducenumber')
            while(currentmiddleboundary+800<transitions[-1]['upper']):
                for k in range(len(transitions)):
                    if currentmiddleboundary+200<transitions[k]['upper']: #We do the +300 thing so that we always have a reasonable transition.
                        if k+1<len(transitions):
                            endpoint=k+1
                        else:
                            endpoint=len(transitions)-1
                        break
                currentdata=data[currentmiddleboundary:transitions[endpoint]['upper']]
                print('Using window '+str(currentmiddleboundary)+' to '+str(transitions[endpoint]['upper']))
                currentdata=np.array([k for k in currentdata])
                boundary,binlist,featurevalues=GetClusteringFromData(currentdata,numfeatures=3,reducenumber=reducenumber)
                tobesaved[i][-1].append(boundary)
                boundaryvalue=boundary[0]
                if boundary[0]==0:
                    print('0 boundary detected. Artificially setting it to 50 to get things rolling')
                    boundaryvalue=50
                currentmiddleboundary=currentmiddleboundary+boundaryvalue
                print(currentmiddleboundary)
        os.remove('Logs/exactboundaries2')
        pickle.dump(tobesaved,open('Logs/exactboundaries2','wb'))
        print('*'*50)
        print('dumping')
        print('*'*50)
def exactboundariespicture():
    dic=pickle.load(open('Logs/exactboundaries2'))
    plt.figure()
    for i in range(len(dic.keys())-1):
        sample=i+3
        transitions = generate_data.segmentations['86 0' + str(sample)]
        plt.subplot(7,1,i+1)
        for j in range(len(dic[i])):
            numfeatures=10+j*5
            boundaries=dic[i][j]
            currentboundary=0
            actualboundaries=[]
            for boundary,error in boundaries:
                currentboundary+=boundary
                plt.scatter(currentboundary,numfeatures,marker='x',s=error**2*1000+20)
        for transition in transitions:
            plt.plot([transition['middle'],transition['middle']],[0,30])
    plt.show()

def windowsizeminibatch():
    tobesaved={}
    counter=logcounter('windowsizeminibatch')
    noise=0.01
    numblocks=15
    blocksize=500
    numfeatures=5
    tobesaved['data']=[]
    tobesaved['rightwindow']=[]
    tobesaved['smallwindow']=[]
    tobesaved['bigwindow']=[]
    tobesaved['terriblewindow']=[]
    for i in range(7):
        print('='*80)
        print(i)
        print('='*80)
        testdata,boundaries=generate_data.toydata2(noise=noise,numblocks=numblocks,blocksize=blocksize,numfeatures=numfeatures)
        tobesaved['data'].append((testdata,boundaries))
        print('Doing right window size')
        tobesaved['rightwindow'].append(minibatch(testdata,steplength=2*blocksize,numfeatures=numfeatures))
        print('Doing small window size')
        tobesaved['smallwindow'].append(minibatch(testdata,steplength= 2 * 0.75 * blocksize,numfeatures=numfeatures))
        print('Doing big window size')
        tobesaved['bigwindow'].append(minibatch(testdata, steplength=2 *1.25 * blocksize,numfeatures=numfeatures))
        print('Doing terrible window size')
        tobesaved['terriblewindow'].append(minibatch(testdata,steplength= 2 * 1.5* blocksize,numfeatures=numfeatures))
    pickle.dump(tobesaved,open('Logs/windowsizeminibatch'+str(counter),'wb'))

def windowsizeminibatch2():
    asdf=pickle.load(open('Logs/windowsizeminibatch2','rb'))
    plt.figure()
    plt.title('2=smallwindow, 4=right window, 6=slightly too big window, 8=way too big window')

    numsamples=len(asdf['rightwindow'])
    for i in range(numsamples):
        realboundaries=asdf['data'][i][1]
        plt.subplot(numsamples,1,i+1)
        plt.title('Random sample '+str(i+1))
        for boundary,error in asdf['smallwindow'][i]:
            print(error)
            plt.scatter(boundary,2,marker='x',s=(error**2*1000+20))
        for boundary,error in asdf['rightwindow'][i]:
            print(error)
            plt.scatter(boundary,4,marker='x',s=error**2*1000+20)
        for boundary,error in asdf['bigwindow'][i]:
            plt.scatter(boundary,6,marker='x',s=error**2*1000+20)
        for boundary,error in asdf['terriblewindow'][i]:
            plt.scatter(boundary,8,marker='x',s=error**2*1000+20)
        for boundary in realboundaries:
            plt.plot([boundary,boundary],[0,10])
    plt.show()

def highvariancedata(): #TODO rerun this. I am not willing to believe this is working correctly.
    counter=logcounter('highvariancedata')
    avgblocksize=250
    variance1=0.33
    variance2=0.66
    variance3=0
    tobesaveds=[]



    for i in range(6):
        print('In ' + str(i) + 'th iteration')
        tobesaved={}
        tobesaved['variance1'] = {}
        tobesaved['variance2'] = {}
        tobesaved['variance3'] = {}
        tobesaved['variance1']['data'] = []
        tobesaved['variance2']['data'] = []
        tobesaved['variance3']['data'] = []
        tobesaved['variance1']['boundaries'] = []
        tobesaved['variance2']['boundaries'] = []
        tobesaved['variance3']['boundaries'] = []
        tobesaved['variance1']['data'].append(generate_data.toydata2(numblocks=10, noise=0.001, variance=variance1, numfeatures=20, blocksize=avgblocksize))
        tobesaved['variance2']['data'].append(generate_data.toydata2(numblocks=10, noise=0.001, variance=variance2, numfeatures=20, blocksize=avgblocksize))
        tobesaved['variance3']['data'].append(generate_data.toydata2(numblocks=10, noise=0.001, variance=variance3, numfeatures=20, blocksize=avgblocksize))
        for j in range(5):
            scalefactor = 1 + (j - 2) * 0.1
            print('Using scalefactor:'+str(scalefactor))
            boundaries1=minibatch(tobesaved['variance1']['data'][-1][0],steplength=2*scalefactor*avgblocksize,numfeatures=5)
            print(boundaries1)
            tobesaved['variance1']['boundaries'].append(boundaries1)
            boundaries2=minibatch(tobesaved['variance2']['data'][-1][0],steplength=2*scalefactor*avgblocksize, numfeatures=5)
            tobesaved['variance2']['boundaries'].append(boundaries2)
            print(boundaries2)
            boundaries3=minibatch(tobesaved['variance3']['data'][-1][0], steplength=2*scalefactor*avgblocksize, numfeatures=5)
            tobesaved['variance3']['boundaries'].append(boundaries3)
            print(boundaries3)
        tobesaveds.append(tobesaved)
        pickle.dump(tobesaveds,open('Logs/highvariancedatavariablescalefactor','wb'))
def highvariancedata2():
    dic=pickle.load(open('Logs/highvariancedata2','rb'))
    numiterations=len(dic['variance1']['data'])
    plt.figure()
    for i in range(numiterations):
        plt.subplot(numiterations,3,i*3+1)
        trueboundaries=dic['variance1']['data'][i][1]
        print(dic['variance2']['boundaries'])
        for boundary,error in dic['variance1']['boundaries'][i]:
            plt.scatter(boundary,1,marker='x',s=error**2*1000+20)
        for boundary in trueboundaries:
            plt.plot([boundary,boundary],[0,2])
        plt.subplot(numiterations,3,i*3+2)
        trueboundaries=dic['variance2']['data'][i][1]
        for boundary,error in dic['variance3']['boundaries'][i]:
            plt.scatter(boundary,1,marker='x',s=error**2*1000+20)
        for boundary in trueboundaries:
            plt.plot([boundary,boundary],[0,2])
        plt.subplot(numiterations,3,i*3+3)
        trueboundaries=dic['variance3']['data'][i][1]
        for boundary,error in dic['variance3']['boundaries'][i]:
            plt.scatter(boundary,1,marker='x',s=error**2*1000+20)
        for boundary in trueboundaries:
            plt.plot([boundary,boundary],[0,2])
    plt.show()

def highvariancedatavariablesscalefactor():
    data=pickle.load(open('Logs/highvariancedatavariablescalefactor','rb'))
    plt.figure()
    for i in range(len(data[:-1])):
        dic=data[i]
        plt.subplot(len(data[:-1]),3,3*i+1)
        plt.ylabel('scalefactor')
        realboundaries1=dic['variance3']['data'][0][1]
        for boundary in realboundaries1:
            plt.plot([boundary,boundary],[0.8,1.2])
        for j in range(len(dic['variance3']['boundaries'])):
            boundaries=dic['variance3']['boundaries'][j]
            scalefactor = 1 + (j - 2) * 0.1
            for boundary in boundaries:
                plt.scatter(boundary,scalefactor,marker='x',s=125)
        plt.subplot(len(data[:-1]),3,3*i+2)
        plt.ylabel('scalefactor')
        realboundaries2 = dic['variance1']['data'][0][1]
        for boundary in realboundaries2:
            plt.plot([boundary,boundary],[0.7,1.3])
        for j in range(len(dic['variance1']['boundaries'])):
            boundaries=dic['variance1']['boundaries'][j]
            scalefactor = 1 + (j - 2) * 0.1
            for boundary in boundaries:
                plt.scatter(boundary,scalefactor,marker='x',s=125)
        plt.subplot(len(data[:-1]),3,3*i+3)
        plt.ylabel('scalefactor')
        realboundaries3 = dic['variance2']['data'][0][1]

        for boundary in realboundaries3:
            plt.plot([boundary, boundary], [0.7, 1.3])
        for j in range(len(dic['variance2']['boundaries'])):

            boundaries=dic['variance2']['boundaries'][j]
            scalefactor = 1 + (j - 2) * 0.1
            for boundary in boundaries:
                plt.scatter(boundary,scalefactor,marker='x',s=125)
    plt.show()

def highvariancedata3():
    maxiterations=7
    scalefactors=[0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
    variances=[0,0.2,0.4]
    tobesaved=[]
    for i in range(maxiterations):
        variancelists=[]
        for j in range(len(variances)):
            dic={}
            data,boundaries=generate_data.toydata2(noise=0.001,variance=variances[j],numfeatures=30)
            dic['data']=data
            dic['realboundaries']=boundaries
            dic['variance']=variances[j]
            dic['scalefactors']=[]
            for scalefactor in scalefactors:
                print('Scalefactor: '+str(scalefactor))
                print('Variance: '+str(variances[j]))
                print('Iteration: '+str(i))
                dic['scalefactors'].append({})
                dic['scalefactors'][-1]['scalefactor']=scalefactor
                dic['scalefactors'][-1]['boundarydata']=minibatch(data,steplength=2*500*scalefactor,numfeatures=5,reducenumber=15,timesteps=20,numclusters=2)
            variancelists.append(dic)
        tobesaved.append(variancelists)
        pickle.dump(tobesaved,open('Logs/newhighvariancedata','wb'))

def highvariancedata3graph():
    plt.figure()
    tobesaved=pickle.load(open('logs/newhighvariancedata','rb'))
    for j in range(len(tobesaved)):
        variancelists=tobesaved[j]
        for i in range(len(variancelists)):
            plt.subplot(len(tobesaved),3,j*3+i+1)
            dic=variancelists[i]
            realboundaries=dic['realboundaries']
            for boundary in realboundaries:
                plt.plot([boundary,boundary],[0.65,1.3])
            for newdic in dic['scalefactors']:
                scalefactor=newdic['scalefactor']
                for boundary,error in newdic['boundarydata']:
                    plt.scatter(boundary,scalefactor,marker='x',s=1000*error**2+20)
    plt.show()

def doubletripletest():
    tobesaved=[[],[],[],[]]
    variances=[0,0.2,0.4,0.6]
    for i in range(4):
        variance=variances[i]
        for j in range(10):
            asdf, boundaries = generate_data.toydata2(variance=variance)

            transitions = generate_data.segmentations['86 01']
            kkk=tripledouble(asdf, numfeatures=5, steplength=500, reducenumber=15, timesteps=20)
            minibatcherino=minibatch(asdf,numfeatures=5,steplength=500*2,reducenumber=15,timesteps=20)
            print(boundaries)
            tobesaved[i].append((kkk,minibatcherino,boundaries,asdf))
            pickle.dump(tobesaved,open('Logs/doubletripletest','wb'))
def doubletriplediagram():
    asdf = pickle.load(open('Logs/doubletripletest', 'rb'))
    plt.figure()
    for i in range(len(asdf)):
        listerino=asdf[i]
        for j in range(len(listerino)):
            tdboundaries, mboundaries, rboundaries, data=listerino[j]
            plt.subplot(len(listerino),3,i+1+j*3)
            for boundary,status in tdboundaries:
                if status=='proper':
                    plt.scatter(boundary,1,marker='x',s=100)
                else:
                    plt.scatter(boundary,1,marker='x',s=500)
            for boundary,error in mboundaries:
                plt.scatter(boundary,2,marker='.')
            for boundary in rboundaries:
                plt.plot([boundary,boundary],[0,3])
    plt.show()
def realdatacomparison():

    tobesaved = [['Transition points found by minibatch'], ['Errors for those transitions']]
    counter = logcounter('prettypicturecounter')
    windowsize = [1200, 2000, 2000, 2000, 2000, 1800, 2000, 1800, 2000]
    numsamples = 7

    for j in range(numsamples):
        sizerino=windowsize[j]
        sample = j + 3
        # plt.subplot(numsamples,1,j+1)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        print('Looking at sample' + str(sample) + '\n')
        data = generate_data.readSample(sample)
        testdata = np.array([k for k in data])
        print('='*50)
        print('minibatch right now')
        boundarymb=minibatchfromsample(sample,steplength=sizerino,reducenumber=15,numfeatures=5,timesteps=20)
        print('='*50)
        print('doubletriple right now')
        boundarydt=tripledouble(testdata,numfeatures=5,steplength=sizerino/2,reducenumber=15,timesteps=20)
        tobesaved.append((boundarymb,boundarydt))

        pickle.dump(tobesaved, open('Logs/doubletriplecomparisionrealdata', 'wb'))
def realdatacomparisondiagram():
    data=pickle.load(open('Logs/doubletriplecomparisionrealdata','rb'))
    realdata=data[2:]
    plt.figure()
    for j in range(len(realdata)):
        sample=j+3
        transitions = generate_data.segmentations['86 0' + str(sample)]
        plt.subplot(len(realdata),1,j+1)
        boundarymb,boundarydt=realdata[j]

        for point in boundarymb[0]:
            plt.scatter(point,2,marker='.')
        for point,status in boundarydt:
            if status == 'proper':
                plt.scatter(point, 1, marker='x', s=100)
            else:
                plt.scatter(point, 1, marker='x', s=500)
        for x in transitions:
            plt.plot([x['middle'],x['middle']],[0,3])
    plt.show()

def smoldatatest():
    windowsize = [1200, 2000, 2000, 2000, 2000, 1800, 2000, 1800, 2000]
    length=len(generate_data.othersegmentationstuff)

    # for i in range(length):
    #     plt.subplot(length,1,i+1)
    #     sample=i+1
    #     data=generate_data.smoldata(sample)
    #     haca=generate_data.othersegmentationstuff[i]
    #     for point in haca:
    #         plt.scatter(point,1,marker='x')
    #     mb=minibatch(data,windowsize[i]/4)
    #     for point,error in mb:
    #         plt.scatter(point,2,marker='x')
    for j in range(9):
        plt.figure()
        sample=1+j
        reducenumber=20
        groundtruth = generate_data.segmentations['86 0'+str(sample)]
        numclusters=len(groundtruth)
        num_clusters=[numclusters-2,numclusters-1,numclusters,numclusters+1,numclusters+2,numclusters+3,numclusters+3]
        print('Sample: '+str(sample))
        print('smol')
        data = np.array(generate_data.smoldata(sample))
        testdata = pca_reduce(data, reducenumber)
        haca = generate_data.othersegmentationstuff[sample - 1]
        sfanode = mdp.nodes.SFANode()
        expansionnode = mdp.nodes.PolynomialExpansionNode(2)
        testdata2 = expansionnode.execute(testdata)
        print(testdata2.shape)
        sfanode.train(testdata2)
        sfanode.stop_training()
        feature_values = sfanode.execute(testdata2, n=5)
        distmatrix = generate_data.simmatrix2(5, feature_values, 20)
        for i,clusternum in enumerate(num_clusters):
            plt.subplot(len(num_clusters),2,2*i+1)
            clusterer = cluster.SpectralClustering(n_clusters=clusternum, affinity='precomputed')
            binarylist = clusterer.fit_predict(distmatrix)
            binarylist = generate_data.reorder(binarylist)
            plt.scatter(range(len(binarylist)),binarylist,marker='x')

            groundtruth2=[point['middle']/4. for point in groundtruth]
            for point in groundtruth2:
                plt.plot([point,point],[0,10])

        print('big')
        data = np.array(generate_data.readSample(sample))
        testdata = pca_reduce(data, reducenumber)
        haca = generate_data.othersegmentationstuff[sample - 1]
        sfanode = mdp.nodes.SFANode()
        expansionnode = mdp.nodes.PolynomialExpansionNode(2)
        testdata2 = expansionnode.execute(testdata)
        print(testdata2.shape)
        sfanode.train(testdata2)
        sfanode.stop_training()
        feature_values = sfanode.execute(testdata2, n=5)
        distmatrix = generate_data.simmatrix2(5, feature_values, 20)
        for i, clusternum in enumerate(num_clusters):
            plt.subplot(len(num_clusters), 2, 2*i + 2)
            clusterer = cluster.SpectralClustering(n_clusters=clusternum, affinity='precomputed')
            binarylist = clusterer.fit_predict(distmatrix)
            binarylist = generate_data.reorder(binarylist)
            plt.scatter(range(len(binarylist)), binarylist, marker='x')

            groundtruth2 = [point['middle'] for point in groundtruth]
            for point in groundtruth2:
                plt.plot([point, point], [0, 10])
    plt.show()
def smoltest2():
    plt.figure()
    sample=8
    reducenumber = 20
    groundtruth = generate_data.segmentations['86 0' + str(sample)]
    numclusters = len(groundtruth)
    num_clusters = [numclusters - 2, numclusters - 1, numclusters, numclusters + 1, numclusters + 2, numclusters + 3, numclusters + 3]
    print('Sample: ' + str(sample))
    print('smol')
    data = np.array(generate_data.smoldata(sample))
    testdata = pca_reduce(data, reducenumber)
    haca = generate_data.othersegmentationstuff[sample - 1]
    sfanode = mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata2 = expansionnode.execute(testdata)
    print(testdata2.shape)
    sfanode.train(testdata2)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata2, n=5)
    distmatrix = generate_data.simmatrix2(5, feature_values, 20)
    expected_windowsize=1000/4 #specific value for sample 8
    for i, clusternum in enumerate(num_clusters):
        plt.subplot(len(num_clusters), 1, 1 * i + 1)
        clusterer = cluster.SpectralClustering(n_clusters=clusternum, affinity='precomputed')
        binarylist = clusterer.fit_predict(distmatrix)
        binarylist = generate_data.reorder(binarylist)
        binarylist=generate_data.reorder(binarylist)
        binarylist=generate_data.clusteringheuristic1(binarylist,expected_windowsize)
        binarylist=generate_data.clusteringheuristic2(binarylist,expected_windowsize,distmatrix)
        boundary1=generate_data.findbestcenterapproach(binarylist,clusternum,expected_windowsize)
        boundary2=generate_data.find_boundarieskmeans(binarylist,clusternum,expected_windowsize/2)

        plt.scatter(range(len(binarylist)), binarylist, marker='x')
        for boundary in boundary1:
            plt.plot([boundary[0],boundary[0]],[11,12],'red')
        for boundary in boundary2:
            plt.plot([boundary,boundary],[13,14],'blue')
        groundtruth2 = [point['middle']/4. for point in groundtruth]
        for point in groundtruth2:
            plt.plot([point, point], [0, 5])
        for point in haca:
            plt.plot([point,point],[5,10])
    plt.show()
def smoldtwtest():
    sample=8
    reducenumber=20
    expected_windowsize = 1000 / 3 # specific value for sample 8
    groundtruth = generate_data.segmentations['86 0' + str(sample)]
    numclusters = len(groundtruth)
    data = np.array(generate_data.smoldata(sample))
    testdata = pca_reduce(data, reducenumber)
    haca = generate_data.othersegmentationstuff[sample - 1]
    sfanode = mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata2 = expansionnode.execute(testdata)
    print(testdata2.shape)
    sfanode.train(testdata2)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata2, n=5)
    matrix1,matrix2,matrix3=pickle.load(open('logs/dtwstuff','rb'))
    #dumperino=[]
    #distmatrix1=generate_data.simmatrix2(5,feature_values,20)
    #dumperino.append(distmatrix1)
    #pickle.dump(dumperino,open('Logs/dtwstuff','wb'))
    newmatrix2=generate_data.hybriddtwmatrix(5,feature_values,20,expected_windowsize)
    #dumperino.append(distmatrix3)
    #pickle.dump(dumperino,open('logs/dtwstuff','wb'))

    #distmatrix2=generate_data.slowestdtwmatrix(5,feature_values,20)
    dumperino=[matrix1,newmatrix2,matrix3]
    pickle.dump(dumperino,open('Logs/dtwstuff','wb'))
    #plt.matshow(distmatrix1)
    #plt.matshow(distmatrix2)
    #plt.matshow(distmatrix3)
    #plt.show()
def makeclustersfromboundaries(binarylist,boundaries):
    clusters=[[] for boundary in boundaries]+[[]]
    for i,clustering in enumerate(binarylist):
        donezo=True
        for j,point in enumerate(boundaries):
            if i<point:
                clusters[j].append((i,clustering))
                donezo=False
                break
        if donezo:
            clusters[-1].append((i,clustering))
    return clusters


    pass
def clusterevaluation1(binarylist,clusters):
    '''
    Evaluates a clustering created by makeclustersfromboundaries, and a standard binarylist as everywhere else in these files. Evaluates it by seeing how homogenous it is, aka what ratio the most common has to everything else.
    Returns that ratio
    '''
    scores=[]
    for cluster in clusters:
        if cluster!=[]:
            clusteringlist=[x[1] for x in cluster]
            mostcommon=max(set(clusteringlist), key=clusteringlist.count)
            scores.append(clusteringlist.count(mostcommon)/float(len(clusteringlist)))
        else:
            scores.append(0)
    return scores

def clusterevaluation2(binarylist,clusters,distmatrix):
    '''
    Evaluates a clustering created by makeclustersfromboundaries, and a standard binarylist as everywhere else in these files, and the corresponding distance matrix. Computes the sum of the similarity scores of the clustering (box on distmatrix), then divides by n^2 (basically average similarity)
    '''
    scores=[]
    for cluster in clusters:
        if cluster!=[]:
            sum=0
            for point1 in cluster:
                coordinate1=point1[0]
                for point2 in cluster:
                    coordinate2=point2[0]
                    sum+=distmatrix.item(coordinate1,coordinate2)
            sum/=len(cluster)**2
            scores.append(sum)
        else:
            scores.append(0)
    return scores
def smoltest3():
    plt.figure()
    sample=8
    reducenumber = 20
    groundtruth = generate_data.segmentations['86 0' + str(sample)]
    numclusters = len(groundtruth)
    num_clusters = [numclusters - 2, numclusters - 1, numclusters, numclusters + 1, numclusters + 2, numclusters + 3, numclusters + 3]
    print('Sample: ' + str(sample))
    print('smol')
    data = np.array(generate_data.smoldata(sample))
    testdata = pca_reduce(data, reducenumber)
    haca = generate_data.othersegmentationstuff[sample - 1]
    sfanode = mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata2 = expansionnode.execute(testdata)
    print(testdata2.shape)
    sfanode.train(testdata2)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata2, n=5)
    distmatrix = generate_data.simmatrix2(5, feature_values, 20)
    expected_windowsize=1000/4 #specific value for sample 8
    for i, clusternum in enumerate(num_clusters):
        plt.subplot(len(num_clusters), 1, 1 * i + 1)
        clusterer = cluster.SpectralClustering(n_clusters=clusternum, affinity='precomputed')
        binarylist = clusterer.fit_predict(distmatrix)
        binarylist = generate_data.reorder(binarylist)
        binarylist=generate_data.reorder(binarylist)
        binarylist=generate_data.clusteringheuristic1(binarylist,expected_windowsize)
        binarylist=generate_data.clusteringheuristic2(binarylist,expected_windowsize,distmatrix)
        boundary1=generate_data.findbestcenterapproach(binarylist,clusternum,expected_windowsize)
        boundary2=generate_data.find_boundarieskmeans(binarylist,clusternum,expected_windowsize/2)
        boundary12=[x[0] for x in boundary1[1:]]
        clusters1=makeclustersfromboundaries(binarylist,boundary12)
        clusters2=makeclustersfromboundaries(binarylist,boundary2)
        evaloneone=clusterevaluation1(binarylist,clusters1)
        evaltwoone=clusterevaluation1(binarylist,clusters2)
        evalonetwo=clusterevaluation2(binarylist,clusters1,distmatrix)
        evaltwotwo=clusterevaluation2(binarylist,clusters2,distmatrix)
        plt.scatter(range(len(binarylist)), binarylist, marker='x')

        for i,boundary in enumerate(boundary1):
            plt.scatter(boundary[0],[11],marker='.',c='red',s=(1-evaloneone[i])**2*1000+30)
            plt.scatter(boundary[0],[15],marker='.',c='blue',s=(1-evalonetwo[i])**2*1000+30)
        for i,boundary in enumerate(boundary2):
            plt.scatter(boundary,[19],marker='x',c='red',s=(1-evaltwoone[i])**2*1000+30)
            plt.scatter(boundary,[23],marker='x',c='blue',s=(1-evaltwotwo[i])**2*1000+30)
        groundtruth2 = [point['middle']/4. for point in groundtruth]
        for point in groundtruth2:
            plt.plot([point, point], [0, 5])
        for point in haca:
            plt.plot([point,point],[5,10])
    plt.show()
def generatematrices():
    euclidmatrix,hybridmatrix,fulldtwmatrix=pickle.load(open('logs/dtwstuff','rb'))
    euclidwith0s=[]
    for i,row in enumerate(euclidmatrix):
        euclidwith0s.append([])
        for j,entry in enumerate(row.tolist()[0]):
            if abs(i-j)<400:
                euclidwith0s[-1].append(euclidmatrix.item(i,j))
            else:
                euclidwith0s[-1].append(0)
    euclidwith0s=np.matrix(euclidwith0s)
    dtwwith0s=[]
    for i,row in enumerate(euclidmatrix):
        dtwwith0s.append([])
        for j,entry in enumerate(row.tolist()[0]):
            if abs(i-j)<400:
                dtwwith0s[-1].append(fulldtwmatrix.item(i,j))
            else:
                dtwwith0s[-1].append(0)
    dtwwith0s=np.matrix(dtwwith0s)
    return[euclidmatrix,fulldtwmatrix,hybridmatrix,euclidwith0s,dtwwith0s]

def smoltest4():
    plt.figure()
    reducenumber = 20
    groundtruth = generate_data.segmentations['86 0' + str(8)]
    numclusters = len(groundtruth)
    haca = generate_data.othersegmentationstuff[8 - 1]
    sfanode = mdp.nodes.SFANode()
    expected_windowsize = 1000 / 4  # specific value for sample 8
    euclidmatrix,fulldtwmatrix,hybridmatrix,euclidwith0s,dtwwith0s=generatematrices()
    labels=['Full Euclidean','Full Dtw','Hybrid Euclidean and DTW','Euclidean with 0s','Dtw with 0s']
    matrices=[euclidmatrix,fulldtwmatrix,hybridmatrix,euclidwith0s,dtwwith0s]
    for i,distmatrix in enumerate(matrices):
        plt.subplot(len(matrices), 1, 1 * i + 1)
        clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
        binarylist = clusterer.fit_predict(distmatrix)
        binarylist = generate_data.reorder(binarylist)
        binarylist=generate_data.reorder(binarylist)
        binarylist=generate_data.clusteringheuristic1(binarylist,expected_windowsize)
        binarylist=generate_data.clusteringheuristic2(binarylist,expected_windowsize,distmatrix)
        boundary1=generate_data.findbestcenterapproach(binarylist,numclusters,expected_windowsize)
        boundary2=generate_data.find_boundarieskmeans(binarylist,numclusters,expected_windowsize/2)
        boundary12=[x[0] for x in boundary1[1:]]
        clusters1=makeclustersfromboundaries(binarylist,boundary12)
        clusters2=makeclustersfromboundaries(binarylist,boundary2)
        evaloneone=clusterevaluation1(binarylist,clusters1)
        evaltwoone=clusterevaluation1(binarylist,clusters2)
        evalonetwo=clusterevaluation2(binarylist,clusters1,distmatrix)
        evaltwotwo=clusterevaluation2(binarylist,clusters2,distmatrix)
        plt.title(labels[i])
        plt.scatter(range(len(binarylist)), binarylist, marker='x')

        for i,boundary in enumerate(boundary1):
            plt.scatter(boundary[0],[3.5],marker='.',c='b',s=250)
        for i,boundary in enumerate(boundary2):
            plt.scatter(boundary,[6.5],marker='x',c='b',s=250)
        groundtruth2 = [point['middle']/4. for point in groundtruth]
        for point in groundtruth2:
            plt.plot([point, point], [0, 11])
    plt.show()

def smoltest5():
    groundtruth = generate_data.segmentations['86 0' + str(8)]
    clusternums=[len(groundtruth)-2, len(groundtruth)-1,len(groundtruth),len(groundtruth)+1,len(groundtruth)+2,len(groundtruth)+3]
    plt.figure()
    for i,numclusters in enumerate(clusternums):
        reducenumber = 20
        sfanode = mdp.nodes.SFANode()
        expected_windowsize = 1000 / 4  # specific value for sample 8
        euclidmatrix,fulldtwmatrix,hybridmatrix,euclidwith0s,dtwwith0s=generatematrices()
        labels=['Full Euclidean','Full Dtw','Hybrid Euclidean and DTW','Euclidean with 0s','Dtw with 0s']
        matrices=[dtwwith0s]
        for distmatrix in matrices:
            plt.subplot(len(clusternums)/2, 2, 1 * i + 1)
            clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
            binarylist = clusterer.fit_predict(distmatrix)
            binarylist = generate_data.reorder(binarylist)
            binarylist=generate_data.reorder(binarylist)
            binarylist=generate_data.clusteringheuristic1(binarylist,expected_windowsize)
            binarylist=generate_data.clusteringheuristic2(binarylist,expected_windowsize,distmatrix)
            boundary1=generate_data.findbestcenterapproach(binarylist,numclusters,expected_windowsize)
            boundary2=generate_data.find_boundarieskmeans(binarylist,numclusters,expected_windowsize/2)
            boundary12=[x[0] for x in boundary1[1:]]
            plt.title(str(numclusters)+'/'+str(len(groundtruth)))
            plt.scatter(range(len(binarylist)), binarylist, marker='x')

            for i,boundary in enumerate(boundary1):
                plt.scatter(boundary[0],[11],marker='.',c='red',)
            for i,boundary in enumerate(boundary2):
                plt.scatter(boundary,[19],marker='x',c='red')
            groundtruth2 = [point['middle']/4. for point in groundtruth]
            for point in groundtruth2:
                plt.plot([point, point], [0, 5])
    plt.show()
def generate_features():
    for i in range(10):
        print(i)
        sample=i+1
        data,boundaries= generate_data.toydata2()
        testdata = pca_reduce(data, 20)
        sfanode = mdp.nodes.SFANode()
        expansionnode = mdp.nodes.PolynomialExpansionNode(2)
        testdata2 = expansionnode.execute(testdata)
        sfanode.train(testdata2)
        sfanode.stop_training()
        feature_values = sfanode.execute(testdata2, n=5)
        np.savetxt('Logs/truetoydata'+str(sample),data)
        np.savetxt('Logs/truetoydatafeatures'+str(sample),feature_values)
        np.savetxt('Logs/truetoydataboundaries'+str(sample),boundaries)


def windowsizetest3():
    tobesaved = {}
    boundariesmiddle2 = []
    boundarieslower2 = []
    boundariesupper2 = []
    boundariesterrible2 = []
    plt.figure()
    numsamples = 7
    for j in range(numsamples):
        plt.subplot(numsamples, 1, j + 1)
        boundariesmiddle2.append([])
        boundarieslower2.append([])
        boundariesupper2.append([])
        boundariesterrible2.append([])
        sample = j + 3
        print('Working on sample ' + str(sample))
        data = generate_data.readSample(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper'] for x in transitions]
        testdatamiddle = np.array([k for k in data[:transitions[1]]])
        testdatalower = np.array([k for k in data[:(transitions[1] + transitions[0]) / 2]])
        testdataupper = np.array([k for k in data[:(transitions[1] + transitions[2]) / 2]])
        testdataterrible = np.array([k for k in data[:transitions[2]]])
        print('Working on the right windowsize')
        boundariesmiddle2[-1].append([])
        reducenumber = 20
        clusteringdata = GetClusteringFromData(testdatamiddle, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesmiddle2[-1][-1].append(clusteringdata[0])
        boundariesmiddle = clusteringdata[0][0]
        plt.plot(boundariesmiddle, 10, 'x')
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        print('Working on a too small windowsize')
        boundarieslower2[-1].append([])
        reducenumber = 20
        clusteringdata = GetClusteringFromData(testdatalower, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundarieslower2[-1][-1].append(clusteringdata[0])
        boundarieslower = clusteringdata[0][0]
        plt.plot(boundarieslower, 15, '^')
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        boundariesupper2[-1].append([])
        reducenumber = 20
        print('Reducing from 62 to ' + str(reducenumber))
        clusteringdata = GetClusteringFromData(testdataupper, numclusters=2, numfeatures=3, reducenumber=reducenumber, timesteps=20)
        boundariesupper2[-1][-1].append(clusteringdata[0])
        boundariesupper = clusteringdata[0][0]
        plt.plot(boundariesupper, 20, 'v')
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        print('Working on a terrible windowsize')
        boundariesterrible2[-1].append([])
        reducenumber = 20
        print('Reducing from 62 to ' + str(reducenumber))
        clusteringdata = GetClusteringFromData(testdataterrible, numclusters=2, numfeatures=3, reducenumber=reducenumber, timesteps=20)
        boundariesterrible2[-1][-1].append(clusteringdata[0])
        boundariesterrible = clusteringdata[0][0]
        plt.plot(boundariesterrible, 25, '*')
        plt.plot([0, 0], [0, 35])
        plt.plot([transitions[0], transitions[0]], [0, 35], 'b')
        plt.plot([transitions[1], transitions[1]], [0, 35], 'r')
        plt.plot([(transitions[2] + transitions[2]) / 2, (transitions[2] + transitions[2]) / 2], [0, 35], 'g')
    plt.show()
    tobesaved['boundariesmiddle'] = boundariesmiddle2
    tobesaved['boundariesupper'] = boundariesupper2
    tobesaved['boundarieslower'] = boundarieslower2
    tobesaved['boundariesterrible'] = boundariesterrible2
    pickle.dump(tobesaved, open('Logs/windowsizetest', 'wb'))
def windowsizetest4():
    numsamples=7
    plt.figure()
    for j in range(numsamples):
        plt.subplot(numsamples,3,j*3+1)
        reducenumber=20
        sample = j + 3
        print('Working on sample ' + str(sample))
        data = generate_data.smoldata(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper']/4 for x in transitions]
        startpoint=transitions[0]
        testdatamiddle = np.array([k for k in data[startpoint:transitions[2]]])
        testdatalower = np.array([k for k in data[startpoint:(transitions[2] + transitions[1]) / 2]])
        testdataupper = np.array([k for k in data[startpoint:(transitions[2] + transitions[3]) / 2]])
        testdataterrible = np.array([k for k in data[startpoint:transitions[3]]])
        plt.plot([startpoint,startpoint],[0,35],':')
        plt.plot([transitions[0],transitions[0]],[0,35],'-')
        plt.plot([transitions[1],transitions[1]],[0,35],'-')
        plt.plot([transitions[2],transitions[2]],[0,35],'-')
        plt.plot([transitions[3], transitions[3]], [0, 35], '-')
        clusteringdata = GetClusteringFromData(testdatamiddle, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesmiddle = clusteringdata[0][0]
        plt.plot(startpoint+boundariesmiddle, 10, 'x',c='b')
        clusteringdata = GetClusteringFromData(testdatalower, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundarieslower = clusteringdata[0][0]
        plt.plot(startpoint+boundarieslower, 15, 'v')
        clusteringdata = GetClusteringFromData(testdataupper, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesupper = clusteringdata[0][0]
        plt.plot(startpoint+boundariesupper, 20, '^')
        clusteringdata = GetClusteringFromData(testdataterrible, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesterrible = clusteringdata[0][0]
        plt.plot(startpoint+boundariesterrible, 25, '*')
    for j in range(numsamples):
        plt.subplot(numsamples,3,j*3+2)
        reducenumber=20
        sample = j + 3
        print('Working on sample ' + str(sample))
        data = generate_data.smoldata(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper']/4 for x in transitions]
        startpoint=(transitions[0]+transitions[1])/2
        testdatamiddle = np.array([k for k in data[startpoint:(transitions[2]+transitions[3])/2]])
        testdatalower = np.array([k for k in data[startpoint:(transitions[2] + transitions[2]) / 2]])
        testdataupper = np.array([k for k in data[startpoint:(transitions[3] + transitions[3]) / 2]])
        testdataterrible = np.array([k for k in data[startpoint:(transitions[3]+transitions[4])/2]])
        plt.plot([startpoint,startpoint],[0,35],':')
        plt.plot([transitions[0], transitions[0]], [0, 35], '-')
        plt.plot([transitions[1],transitions[1]],[0,35],'-')
        plt.plot([transitions[2],transitions[2]],[0,35],'-')
        plt.plot([transitions[3], transitions[3]], [0, 35], '-')
        clusteringdata = GetClusteringFromData(testdatamiddle, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesmiddle = clusteringdata[0][0]
        plt.plot(startpoint+boundariesmiddle, 10, 'x',c='b')
        clusteringdata = GetClusteringFromData(testdatalower, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundarieslower = clusteringdata[0][0]
        plt.plot(startpoint+boundarieslower, 15, 'v')
        clusteringdata = GetClusteringFromData(testdataupper, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesupper = clusteringdata[0][0]
        plt.plot(startpoint+boundariesupper, 20, '^')
        clusteringdata = GetClusteringFromData(testdataterrible, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesterrible = clusteringdata[0][0]
        plt.plot(startpoint+boundariesterrible, 25, '*')
    for j in range(numsamples):
        plt.subplot(numsamples,3,j*3+3)
        reducenumber=20
        sample = j + 3
        print('Working on sample ' + str(sample))
        data = generate_data.smoldata(sample)
        transitions = generate_data.segmentations['86 0' + str(sample)]
        transitions = [x['upper']/4 for x in transitions]
        startpoint=transitions[0]/2
        testdatamiddle = np.array([k for k in data[startpoint:(transitions[2]+transitions[1])/2]])
        testdatalower = np.array([k for k in data[startpoint:(transitions[1] + transitions[1]) / 2]])
        testdataupper = np.array([k for k in data[startpoint:(transitions[2] + transitions[2]) / 2]])
        testdataterrible = np.array([k for k in data[startpoint:(transitions[3]+transitions[2])/2]])
        plt.plot([startpoint,startpoint],[0,35],':')
        plt.plot([transitions[0], transitions[0]], [0, 35], '-')
        plt.plot([transitions[1],transitions[1]],[0,35],'-')
        plt.plot([transitions[2],transitions[2]],[0,35],'-')
        plt.plot([transitions[3], transitions[3]], [0, 35], '-')
        clusteringdata = GetClusteringFromData(testdatamiddle, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesmiddle = clusteringdata[0][0]
        plt.plot(startpoint+boundariesmiddle, 10,'x',c='b')
        clusteringdata = GetClusteringFromData(testdatalower, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundarieslower = clusteringdata[0][0]
        plt.plot(startpoint+boundarieslower, 15, 'v')
        clusteringdata = GetClusteringFromData(testdataupper, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesupper = clusteringdata[0][0]
        plt.plot(startpoint+boundariesupper, 20, '^')
        clusteringdata = GetClusteringFromData(testdataterrible, numclusters=2, numfeatures=5, reducenumber=reducenumber, timesteps=20)
        boundariesterrible = clusteringdata[0][0]
        plt.plot(startpoint+boundariesterrible, 25, '*')
    plt.show()


def toydatapaper(): #TODO rerun this. I am not willing to believe this is working correctly.
    counter=logcounter('highvariancedata')
    avgblocksize=500
    variance1=0.33
    variance2=0.66
    variance3=0
    tobesaveds=[]



    for i in range(6):
        print('In ' + str(i) + 'th iteration')
        tobesaved={}
        tobesaved['variance1'] = {}
        tobesaved['variance2'] = {}
        tobesaved['variance3'] = {}
        tobesaved['variance1']['data'] = []
        tobesaved['variance2']['data'] = []
        tobesaved['variance3']['data'] = []
        tobesaved['variance1']['boundaries'] = []
        tobesaved['variance2']['boundaries'] = []
        tobesaved['variance3']['boundaries'] = []
        tobesaved['variance1']['scores'] = []
        tobesaved['variance2']['scores'] = []
        tobesaved['variance3']['scores'] = []
        testdata1,rboundaries1=generate_data.toydata2(numblocks=10, noise=0.001, variance=variance1, numfeatures=20, blocksize=avgblocksize)
        testdata2, rboundaries2 = generate_data.toydata2(numblocks=10, noise=0.001, variance=variance2, numfeatures=20, blocksize=avgblocksize)
        testdata3, rboundaries3 = generate_data.toydata2(numblocks=10, noise=0.001, variance=variance3, numfeatures=20, blocksize=avgblocksize)
        rboundariesrange1=[(x,(x-0.05*avgblocksize,x+0.05*avgblocksize)) for x in rboundaries1]
        rboundariesrange2=[(x,(x-0.05*avgblocksize,x+0.05*avgblocksize)) for x in rboundaries2]
        rboundariesrange3=[(x,(x-0.05*avgblocksize,x+0.05*avgblocksize)) for x in rboundaries3]
        scalefactor = 1.2
        print('Using scalefactor:'+str(scalefactor))
        boundaries1=minibatch(testdata1,steplength=2*scalefactor*avgblocksize,numfeatures=5)
        boundaries1=[x[0] for x in boundaries1]
        print('Variance = '+str(variance1))
        print(boundaries1)
        print(rboundariesrange1[1:-1])
        print('Score: '+str(boundaryevaluate(boundaries1,rboundariesrange1[1:-1])[0]))
        print('Missed:'+str(boundaryevaluate(boundaries1, rboundariesrange1[1:-1]))[1])
        tobesaved['variance1']['boundaries'].append(boundaries1)
        tobesaved['variance1']['scores'].append(boundaryevaluate(boundaries1, rboundariesrange1[1:-1]))
        boundaries2=minibatch(testdata2,steplength=2*scalefactor*avgblocksize, numfeatures=5)
        boundaries2 = [x[0] for x in boundaries2]
        tobesaved['variance2']['boundaries'].append(boundaries2)
        print('Variance = '+str(variance2))
        print(boundaries2)
        print(rboundariesrange2[1:-1])
        print('Score: '+str(boundaryevaluate(boundaries2,rboundariesrange2[1:-1])[0]))
        print('Missed:'+str(boundaryevaluate(boundaries2, rboundariesrange2[1:-1]))[1])
        tobesaved['variance2']['scores'].append(boundaryevaluate(boundaries2, rboundariesrange2[1:-1]))
        boundaries3=minibatch(testdata3, steplength=2*scalefactor*avgblocksize, numfeatures=5)
        boundaries3 = [x[0] for x in boundaries3]
        tobesaved['variance3']['boundaries'].append(boundaries3)
        print(boundaries3)
        print('Variance = '+str(variance3))
        print(rboundariesrange3[1:-1])
        print('Score: '+str(boundaryevaluate(boundaries3,rboundariesrange3[1:-1])[0]))
        print('Missed:'+str(boundaryevaluate(boundaries3, rboundariesrange3[1:-1]))[1])
        tobesaved['variance3']['scores'].append(boundaryevaluate(boundaries3, rboundariesrange3[1:-1]))
        tobesaveds.append(tobesaved)
        pickle.dump(tobesaveds,open('Logs/highvariancedatavariablescalefactor','wb'))
    print(tobesaved)

def varianceanalysis():
    starttime=time.time()
    iterations=10
    avgblocksize=500
    scalefactor=1.2
    variances=[0,0.06,0.12,0.18,0.24,0.3,0.36,0.42,0.48,0.54,0.6]
    tobesaved={}
    for variance in variances:
        timer=time.time()
        print("We're working on variance "+str(variance))
        tobesaved[variance]={}
        for i in range(iterations):

            tobesaved[variance][i]={}
            print("We're in iteration "+str(i))
            testdata,rboundaries=generate_data.toydata2(numblocks=10, noise=0.001, variance=variance, numfeatures=20, blocksize=avgblocksize)
            rboundariesrange=[(x,(x-0.05*avgblocksize,x+0.05*avgblocksize)) for x in rboundaries[1:-1]]
            minibatchstart=time.time()
            minibatchboundaries = minibatch(testdata, steplength=2 * scalefactor * avgblocksize, numfeatures=5)
            minibatchend=time.time()
            print('Minibatch took: '+str(minibatchend-minibatchstart))
            batchboundaries=FullBatch(testdata,numclusters=10,w=int(avgblocksize*1.5))
            batchend=time.time()
            print('Batch took: '+str(batchend-minibatchend))
            tobesaved[variance][i]['true']=rboundaries
            tobesaved[variance][i]['minibatch']={}
            tobesaved[variance][i]['minibatch']['boundaries']=[x[0] for x in minibatchboundaries]
            tobesaved[variance][i]['minibatch']['score'] = boundaryevaluate([x[0] for x in minibatchboundaries],rboundariesrange)
            tobesaved[variance][i]['minibatch']['time']=minibatchend-minibatchstart
            tobesaved[variance][i]['batch'] = {}
            tobesaved[variance][i]['batch']['boundaries'] = batchboundaries
            tobesaved[variance][i]['batch']['score'] = boundaryevaluate(batchboundaries, rboundariesrange)
            tobesaved[variance][i]['batch']['time']=batchend-minibatchend
            pickle.dump(tobesaved,open('Logs/varianceanalysis2','wb'))
            print('='*50)
        print('*'*50)

def erroranalysis():
    starttime = time.time()
    iterations = 10
    avgblocksize = 500
    scalefactor = 1.2
    variances = [ 0.2,0.4]
    errors=[0.001,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065]
    tobesaved = pickle.load(open('Logs/erroreanalysis','rb'))
    for variance in variances:
        timer = time.time()
        print("We're working on variance " + str(variance))
        tobesaved[variance] = {}
        for error in errors:
            tobesaved[variance][error]={}
            for i in range(iterations):
                tobesaved[variance][error][i] = {}
                print('Error: '+str(error))
                print('Variance '+str(variance))
                print("We're in iteration " + str(i))
                testdata, rboundaries = generate_data.toydata2(numblocks=10, noise=error, variance=variance, numfeatures=20, blocksize=avgblocksize)
                rboundariesrange = [(x, (x - 0.05 * avgblocksize, x + 0.05 * avgblocksize)) for x in rboundaries[1:-1]]
                minibatchstart = time.time()
                minibatchboundaries = minibatch(testdata, steplength=2 * scalefactor * avgblocksize, numfeatures=5)
                minibatchend = time.time()
                print('Minibatch took: ' + str(minibatchend - minibatchstart))
                print(minibatchboundaries)
                batchboundaries = FullBatch(testdata, numclusters=10, w=int(avgblocksize * 1.5))
                print(batchboundaries)
                batchend = time.time()
                print('Batch took: ' + str(batchend - minibatchend))
                tobesaved[variance][error][i]['true'] = rboundaries
                tobesaved[variance][error][i]['minibatch'] = {}
                tobesaved[variance][error][i]['minibatch']['boundaries'] = minibatchboundaries
                tobesaved[variance][error][i]['minibatch']['score'] = boundaryevaluate(minibatchboundaries, rboundariesrange)
                tobesaved[variance][error][i]['minibatch']['time'] = minibatchend - minibatchstart
                tobesaved[variance][error][i]['batch'] = {}
                tobesaved[variance][error][i]['batch']['boundaries'] = batchboundaries
                tobesaved[variance][error][i]['batch']['score'] = boundaryevaluate(batchboundaries, rboundariesrange)
                tobesaved[variance][error][i]['batch']['time'] = batchend - minibatchend
                pickle.dump(tobesaved, open('Logs/erroreanalysis', 'wb'))
                print('=' * 50)
            print('*' * 50)

def clusteringlistexplanation():
    data,boundaries=generate_data.toydata2()
    testdata=pca_reduce(data,10)
    foundboundaries=FullBatch(data,10,750)
    sfanode=mdp.nodes.SFANode()
    expansionnode=mdp.nodes.PolynomialExpansionNode(2)
    testdata=expansionnode.execute(testdata)
    sfanode.train(testdata)
    sfanode.stop_training()
    feature_values=sfanode.execute(testdata,n=5)
    S=MakeSimilarityMatrix(feature_values,750,config='euc0s')
    clusterer = cluster.SpectralClustering(n_clusters=10, affinity='precomputed')
    print('Clustering')
    clusterlabellist = clusterer.fit_predict(S)
    clusterlabellist = generate_data.reorder(clusterlabellist)
    plt.plot(range(len(clusterlabellist)),clusterlabellist,'x')
    plt.xlabel('time t')
    plt.ylabel('Clustering label c_i')
    for point in foundboundaries:
        plt.scatter([point],[5],marker='x',s=250)
    for point in boundaries:
        plt.plot([point,point],[0,10],'r')
    plt.show()

def toydataexample():
    coswave=generate_data.coswave(500,1)
    print(coswave)
    trianglewave=generate_data.trianglewave(500,1)
    stepwave=generate_data.stepwave(500,1)
    zigwave=generate_data.zigzagwave(500,1)
    rectwave=generate_data.rectwave(500,1)
    plt.figure()
    plt.plot(range(len(coswave)),coswave)
    plt.figure()
    plt.plot(range(len(trianglewave)),trianglewave)
    plt.figure()
    plt.plot(range(len(stepwave)),stepwave)
    plt.figure()
    plt.plot(range(len(zigwave)),zigwave)
    plt.figure()
    plt.plot(range(len(rectwave)),rectwave)
    plt.show()

def realdataclusterlists():
    for i in range(9):
        sample=i+1
        data=generate_data.smoldata(sample)
        groundtruth = generate_data.segmentations['86 0' + str(sample)]
        numclusters=len(groundtruth)
        print(numclusters)
        testdata=pca_reduce(data,10)
        sfanode=mdp.nodes.SFANode()
        expansionnode=mdp.nodes.PolynomialExpansionNode(2)
        testdata=expansionnode.execute(testdata)
        sfanode.train(testdata)
        sfanode.stop_training()
        feature_values=sfanode.execute(testdata,n=5)
        S=MakeSimilarityMatrix(feature_values,1.5*len(data)/numclusters,config='euc0s')
        clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
        print('Clustering')
        clusterlabellist = clusterer.fit_predict(S)
        clusterlabellist = generate_data.reorder(clusterlabellist)
        plt.figure()
        plt.plot(range(len(clusterlabellist)),clusterlabellist,'x')
        plt.xlabel('time t')
        plt.ylabel('Clustering label c_i')
    plt.show()

def toydataexample2():
    data, boundaries = generate_data.toydata2()
    testdata = pca_reduce(data, 10)
    foundboundaries = FullBatch(data, 10, 750)
    sfanode = mdp.nodes.SFANode()
    expansionnode = mdp.nodes.PolynomialExpansionNode(2)
    testdata = expansionnode.execute(testdata)
    sfanode.train(testdata)
    sfanode.stop_training()
    feature_values = sfanode.execute(testdata, n=5)
    S = MakeSimilarityMatrix(feature_values, 750, config='euclid')
    clusterer = cluster.SpectralClustering(n_clusters=10, affinity='precomputed')
    print('Clustering')
    clusterlabellist = clusterer.fit_predict(S)
    clusterlabellist = generate_data.reorder(clusterlabellist)
    plt.plot(range(len(clusterlabellist)), clusterlabellist, 'x')
    plt.xlabel('time t')
    plt.ylabel('Clustering label c_i')
    plt.show()

def boundarycomparisons():
    for i in range(5):
        data,trueboundaries=generate_data.toydata2(variance=0.3)
        numclusters=10
        numfeatures=5
        timesteps=20
        sfanode = mdp.nodes.SFANode()
        expansionnode = mdp.nodes.PolynomialExpansionNode(2)
        testdata = expansionnode.execute(data)
        print('After expansion of data, we have dimensions: ' + str(testdata.shape))
        sfanode.train(testdata)
        sfanode.stop_training()
        print('Constructing Feature Vectors')
        feature_values = sfanode.execute(testdata, n=numfeatures)
        print('Constructing Simlarity Matrix')
        S = MakeSimilarityMatrix(feature_values, 750, config='euc0s', numfeatures=numfeatures, timesteps=timesteps)

        clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
        print('Clustering')
        clusterlabellist = clusterer.fit_predict(S)
        clusterlabellist = generate_data.reorder(clusterlabellist)
        boundaries1=find_boundarieskmeans(clusterlabellist,10,250)
        print(boundaries1)
        boundaries2=generate_data.findbestcenterapproach(clusterlabellist,10,500)
        print(boundaries2)
        fig=plt.figure()
        ax=plt.subplot(111)
        plt.xlabel('time t',fontsize=24)
        plt.ylabel('Clustering label c_i',fontsize=24)
        plt.plot(range(len(clusterlabellist)),clusterlabellist,'x')
        for point in boundaries1:
            plt.scatter(point,3.5,marker='x',s=1000)
        for point in boundaries2:
            plt.scatter(point[0],6.5,marker='.',s=1000)
        for boundary in trueboundaries:
            plt.plot([boundary,boundary],[0,10],'r')
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(20)
    plt.show()

def smoltest6():
    plt.figure()
    reducenumber = 20
    groundtruth = generate_data.segmentations['86 0' + str(8)]
    numclusters = len(groundtruth)
    haca = generate_data.othersegmentationstuff[8 - 1]
    sfanode = mdp.nodes.SFANode()
    expected_windowsize = 1000 / 4  # specific value for sample 8
    euclidmatrix,fulldtwmatrix,hybridmatrix,euclidwith0s,dtwwith0s=generatematrices()
    matrices=[dtwwith0s]
    for i,distmatrix in enumerate(matrices):
        plt.subplot(len(matrices), 1, 1 * i + 1)
        clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
        binarylist = clusterer.fit_predict(distmatrix)
        binarylist = generate_data.reorder(binarylist)
        binarylist=generate_data.reorder(binarylist)
        binarylist=generate_data.clusteringheuristic1(binarylist,expected_windowsize)
        binarylist=generate_data.clusteringheuristic2(binarylist,expected_windowsize,distmatrix)
        boundary1=generate_data.findbestcenterapproach(binarylist,numclusters,expected_windowsize)
        boundary2=generate_data.find_boundarieskmeans(binarylist,numclusters,expected_windowsize/2)
        boundary12=[x[0] for x in boundary1[1:]]
        clusters1=makeclustersfromboundaries(binarylist,boundary12)
        clusters2=makeclustersfromboundaries(binarylist,boundary2)
        evaloneone=clusterevaluation1(binarylist,clusters1)
        evaltwoone=clusterevaluation1(binarylist,clusters2)
        evalonetwo=clusterevaluation2(binarylist,clusters1,distmatrix)
        evaltwotwo=clusterevaluation2(binarylist,clusters2,distmatrix)
        plt.scatter(range(len(binarylist)), binarylist, marker='x')
        for i,boundary in enumerate(boundary1):
            plt.scatter(boundary[0],[6.5],marker='.',c='b',s=250)
        for i,boundary in enumerate(boundary2):
            plt.scatter(boundary,[3.5],marker='x',c='b',s=250)
        groundtruth2 = [point['middle']/4. for point in groundtruth]
        for point in groundtruth2:
            plt.plot([point, point], [0, 11],'r')
    plt.show()

def clustertest():
    data,tboundaries=generate_data.toydata2()
    clusters=[7,8,9,10,11,12,13,14]
    plt.figure()
    for i,numclusters in enumerate(clusters):
        plt.subplot(4,2,i+1)
        testdata = pca_reduce(data, 10)
        sfanode = mdp.nodes.SFANode()
        expansionnode = mdp.nodes.PolynomialExpansionNode(2)
        testdata = expansionnode.execute(testdata)
        print('After expansion of data, we have dimensions: ' + str(testdata.shape))
        sfanode.train(testdata)
        sfanode.stop_training()
        print('Constructing Feature Vectors')
        feature_values = sfanode.execute(testdata, n=5)
        print('Constructing Simlarity Matrix')
        S = MakeSimilarityMatrix(feature_values, 750, config='euc0s', numfeatures=5, timesteps=20)

        clusterer = cluster.SpectralClustering(n_clusters=numclusters, affinity='precomputed')
        print('Clustering')
        clusterlabellist = clusterer.fit_predict(S)
        clusterlabellist = generate_data.reorder(clusterlabellist)
        clusterlabellist = clusteringheuristic1(clusterlabellist, int(750))
        clusterlabellist = clusteringheuristic2(clusterlabellist, int(750), S)
        print('Finding boundaries')
        boundaries = find_boundarieskmeans(clusterlabellist, numclusters, 750 / 2)
        plt.title(str(numclusters)+'/10')
        for point in tboundaries:
            plt.plot([point,point],[0,numclusters],'b')
        for point in boundaries:
            plt.scatter(point,numclusters/2,marker='x',s=250,c='red')
        plt.plot(range(len(clusterlabellist)),clusterlabellist,'x')
    plt.show()

def comparesegmentations(sample,stuff=[]):
    segmentstocompare=stuff
    segmentstocompare.append((generate_data.othersegmentationstuff[sample-1],'Boundaries found by Efficient Unsupervised'))
    segmentstocompare.append((generate_data.acaboundaries['aca'][sample-1],'Boundaries found by ACA'))
    segmentstocompare.append((generate_data.acaboundaries['haca'][sample-1],'Boundaries found by HACA'))
    segmentstocompare.append((generate_data.cmuboundaries[sample],'Groundtruth according to CMU'))
    showsegmentation(segmentstocompare,1)

def findbestminibatch(sample):
    data=generate_data.smoldata(sample)
    groundtruth=[x/4 for x in generate_data.cmuboundaries[sample]]
    groundtruthranges=[]
    segcompare=[]
    for point in generate_data.segmentations['86 0'+str(sample)][:-1]:
        groundtruthranges.append((point['middle']/4,(point['lower']/4,point['upper']/4)))
    windowsize=[200,250,300,350,400,450,500,550,600,650,700]
    boundaries={}
    for size in windowsize:
        boundaries[size]={}
        boundaries[size]['boundaries']=[1]+minibatch(data,size)+[groundtruth[-1]]
        boundaries[size]['score']=boundaryevaluate(boundaries[size]['boundaries'],groundtruthranges)
        segcompare.append((boundaries[size]['boundaries'],str(size)+' Score: '+str(boundaries[size]['score'][0])+'Missed: '+str(boundaries[size]['score'][1])))
    comparesegmentations(1,segcompare)
    print(boundaries)

def algcomparison():
    for i in range(9):
        segmentstocompare=[]
        sample=i+1

        groundtruth = [x / 4 for x in generate_data.cmuboundaries[sample]]
        groundtruthranges = [(1,(0,2))]
        segcompare = []
        segmentations=generate_data.segmentations['86 0'+str(sample)]
        for point in generate_data.segmentations['86 0' + str(sample)]:
            groundtruthranges.append((point['middle'] / 4, (point['lower'] / 4, point['upper'] / 4)))
        averagetruthranges=findtruthranges()
        acatruthranges=[]
        for j,point in enumerate(generate_data.acaboundaries['truth'][sample-1][1:-1]):
            acatruthranges.append((point,(point-averagetruthranges[i]/10,point+averagetruthranges[i]/10)))
        batchstart=time.time()
        fullbatchboundaries=[1]+FullBatch(generate_data.smoldata(sample),len(segmentations),(groundtruth[-1]/len(segmentations))*1.5)+[groundtruth[-1]]
        batchend=time.time()
        minibatchboundaries=[1]+minibatch(generate_data.smoldata(sample),bestminibatchsizes[i])+[groundtruth[-1]]
        minibatchend=time.time()
        print(batchend-batchstart)
        print(minibatchend-batchend)
        fullbatchscore=boundaryevaluate(fullbatchboundaries,groundtruthranges)
        fullbatchscore=[round(x,1) for x in fullbatchscore]
        minibatchscore=boundaryevaluate(minibatchboundaries,groundtruthranges)
        minibatchscore=[round(x,1) for x in minibatchscore]
        efficientscore=boundaryevaluate(generate_data.othersegmentationstuff[sample-1],groundtruthranges[:-1])
        efficientscore=[round(x,1) for x in efficientscore]
        acascore=boundaryevaluate(generate_data.acaboundaries['aca'][sample-1],acatruthranges)
        acascore=(float(groundtruth[-1])/generate_data.acaboundaries['aca'][sample-1][-1]*acascore[0],acascore[1])
        acascore=[round(x,1) for x in acascore]
        hacascore=boundaryevaluate(generate_data.acaboundaries['haca'][sample-1],acatruthranges)
        hacascore=(float(groundtruth[-1])/generate_data.acaboundaries['haca'][sample-1][-1]*hacascore[0],hacascore[1])
        hacascore=[round(x,1) for x in hacascore]
        segmentstocompare.append((fullbatchboundaries,'Batch',str(fullbatchscore)))
        segmentstocompare.append((minibatchboundaries,'Minibatch',str(minibatchscore)))
        segmentstocompare.append((generate_data.othersegmentationstuff[sample - 1],'KKV',str(efficientscore)))
        segmentstocompare.append((generate_data.acaboundaries['aca'][sample - 1], 'ACA',str(acascore)))
        segmentstocompare.append((generate_data.acaboundaries['haca'][sample - 1], 'HACA',str(hacascore)))
        comparetotruth((groundtruthranges,'Truth',''),segmentstocompare,1500)
    plt.show()
bestminibatchsizes=[400,450,450,450,450,450,550,450,550]

def findtruthranges():
    averageranges=[]
    for i in range(9):
        difference=0
        count=0
        sample=i+1
        for point in generate_data.segmentations['86 0' + str(sample)][:-1]:
            difference+=point['upper']-point['lower']
            count+=1
        averageranges.append(float(difference)/count)
    return averageranges

def erroranalysisdata():
    starttime = time.time()
    iterations = 1
    avgblocksize = 500
    scalefactor = 1.2
    variances = [ 0,0.2,0.4]
    errors=[0.001,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065]
    tobesaved = pickle.load(open('Logs/erroreanalysis','rb'))
    for i,variance in enumerate(variances):
        timer = time.time()
        print("We're working on variance " + str(variance))
        tobesaved[variance] = {}
        for j,error in enumerate(errors):
            tobesaved[variance][error]={}
            testdata, rboundaries = generate_data.toydata2(numblocks=10, noise=error, variance=variance, numfeatures=20, blocksize=avgblocksize)
            np.savetxt('Logs/erroranalysisdata' + str(i)+str(j), testdata)
            np.savetxt('Logs/erroranalysisdataboundaries'+str(i)+str(j),rboundaries)
            sfanode = mdp.nodes.SFANode()
            expansionnode = mdp.nodes.PolynomialExpansionNode(2)
            testdata = expansionnode.execute(testdata)
            sfanode.train(testdata)
            sfanode.stop_training()
            feature_values = sfanode.execute(testdata, n=5)
            np.savetxt('Logs/erroranalysisfeaturedata'+str(i)+str(j),feature_values)

def nosfatest():
    batches=[]
    nosfabatches=[]
    nosfabatches2=[]
    nosfabatches3=[]
    minis=[]
    nosfaminis=[]
    nosfaminis2=[]
    nosfaminis3=[]
    for i in range(3):
        sample=i+1
        data = generate_data.smoldata(sample)
        groundtruth = [x / 4 for x in generate_data.cmuboundaries[sample]]
        groundtruthranges = []
        segcompare = []
        segmentations = generate_data.segmentations['86 0' + str(sample)]
        for point in generate_data.segmentations['86 0' + str(sample)][:-1]:
            groundtruthranges.append((point['middle'] / 4, (point['lower'] / 4, point['upper'] / 4)))
        truthranges=groundtruthranges
        w=(groundtruth[-1] / len(segmentations))
        print(w)
        batchboundaries =[0]+ FullBatch(data, 10, w)
        sfafull =[0]+ noSFAFullBatch(data, 10, w)
        sfafull2=[0]+noSFAFullBatch2(data,10,w)
        sfafull3=[0]+noSFAFullBatch3(data,10,w)
        mini =[0]+ minibatch(data, 450)
        nosfamini =[0]+ noSFAminibatch(data, 450)
        nosfamini2 =[0]+ noSFAminibatch2(data, 450)
        nosfamini3 =[0]+ noSFAminibatch3(data, 450)
        batchscore=boundaryevaluate(batchboundaries,truthranges)
        batches.append(batchscore)
        sfafullscore=boundaryevaluate(sfafull,truthranges)
        nosfabatches.append(sfafullscore)
        sfafullscore2=boundaryevaluate(sfafull2,truthranges)
        nosfabatches2.append(sfafullscore2)
        sfafullscore3=boundaryevaluate(sfafull3,truthranges)
        nosfabatches3.append(sfafullscore3)
        miniscore=boundaryevaluate(mini,truthranges)
        minis.append(miniscore)
        nosfaminiscore=boundaryevaluate(nosfamini,truthranges)
        nosfaminis.append(nosfaminiscore)
        nosfaminiscore2=boundaryevaluate(nosfamini2,truthranges)
        nosfaminis2.append(nosfaminiscore2)
        nosfaminiscore3=boundaryevaluate(nosfamini3,truthranges)
        nosfaminis3.append(nosfaminiscore3)
    print('Full Batch')
    print(batches)
    print('PCA instead of SFA')
    print(nosfabatches)
    print('Take first 5')
    print(nosfabatches2)
    print('Take all values')
    print(nosfabatches2)
    print('minibatch')
    print(minis)
    print('pca instead of SFA')
    print(nosfaminis)
    print('take first 5')
    print(nosfaminis2)
    print('take all values')
    print(nosfaminis3)

def acasfatest():
    acascores=[]
    realacascores=[]
    featureacascores=[]
    hacascores=[]
    realhacascores=[]
    featurehacascores=[]
    for i in range(9):
        sample=i+1
        acaboundary=generate_data.acaboundaries['aca'][sample-1]
        realacaboundary=generate_data.realacaboundaries['aca'][sample-1]
        featureacaboundary=generate_data.featureacaboundaries['aca'][sample-1]
        hacaboundary=generate_data.acaboundaries['haca'][sample-1]
        realhacaboundary=generate_data.realacaboundaries['haca'][sample-1]
        featurehacaboundary=generate_data.featureacaboundaries['haca'][sample-1]
        acatruthranges = []
        averagetruthranges=findtruthranges()
        for j, point in enumerate(generate_data.acaboundaries['truth'][sample - 1][1:-1]):
            acatruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        acascores.append(boundaryevaluate(acaboundary,acatruthranges))
        realacascores.append(boundaryevaluate(realacaboundary,acatruthranges))
        featureacascores.append(boundaryevaluate(featureacaboundary,acatruthranges))
        hacascores.append(boundaryevaluate(acaboundary,acatruthranges))
        realhacascores.append(boundaryevaluate(realhacaboundary,acatruthranges))
        featurehacascores.append(boundaryevaluate(featurehacaboundary,acatruthranges))
    print(acascores)
    print(np.mean([x[0] for x in acascores]))
    print(np.mean([x[1] for x in acascores]))
    print(realacascores)
    print(np.mean([x[0] for x in realacascores]))
    print(np.mean([x[1] for x in realacascores]))
    print(featureacascores)
    print(np.mean([x[0] for x in featureacascores]))
    print(np.mean([x[1] for x in featureacascores]))
    print('*'*50)
    print(hacascores)
    print(np.mean([x[0] for x in hacascores]))
    print(np.mean([x[1] for x in hacascores]))
    print(realhacascores)
    print(np.mean([x[0] for x in realhacascores]))
    print(np.mean([x[1] for x in realhacascores]))
    print(featurehacascores)
    print(np.mean([x[0] for x in featurehacascores]))
    print(np.mean([x[1] for x in featurehacascores]))

def erroranalysisreworked():
    stuff = pickle.load(open('Logs/erroreanalysis', 'rb'))
    for key in stuff.keys():
        dic = stuff[key]
        for key2 in dic.keys():
            for key3 in dic[key2]:
                run = dic[key2][key3]

                truthranges = [(x, (x - 25, x + 25)) for x in run['true']]
                run['batch']['boundaries'] = [0] + run['batch']['boundaries'] + [run['true'][-1]]
                run['minibatch']['boundaries'] = [0] + run['minibatch']['boundaries'] + [run['true'][-1]]
                run['batch']['score'] = boundaryevaluate(run['batch']['boundaries'], truthranges)
                run['minibatch']['score'] = boundaryevaluate(run['minibatch']['boundaries'], truthranges)
    pickle.dump(stuff, open('Logs/erroranalysiscleaned', 'wb'))

def erroranalysisextra():
    stuff = pickle.load(open('Logs/erroranalysiscleaned', 'rb'))
    stuff2={}
    for variance in stuff.keys():
        stuff2[variance]={}
        for error in stuff[variance].keys():
            stuff2[variance][error]={}
            batchscores = []
            minibatchscores = []
            batchmisses = []
            minibatchmisses = []
            batchtimes=[]
            minibatchtimes=[]
            for run in stuff[variance][error].keys():
                batchscores.append(stuff[variance][error][run]['batch']['score'][0])
                batchmisses.append(stuff[variance][error][run]['batch']['score'][1])
                batchtimes.append(stuff[variance][error][run]['batch']['time'])
                minibatchscores.append(stuff[variance][error][run]['minibatch']['score'][0])
                minibatchmisses.append(stuff[variance][error][run]['minibatch']['score'][1])
                minibatchtimes.append(stuff[variance][error][run]['minibatch']['time'])
            stuff2[variance][error]['batchscores']=(batchscores,np.mean(batchscores),np.std(batchscores))
            stuff2[variance][error]['batchmisses']=(batchmisses,np.mean(batchmisses),np.std(batchmisses))
            stuff2[variance][error]['minibatchscores'] = (minibatchscores,np.mean(minibatchscores),np.std(minibatchscores))
            stuff2[variance][error]['minibatchmisses'] = (minibatchmisses,np.mean(minibatchmisses),np.std(batchmisses))
            stuff2[variance][error]['batchtimes']=(batchtimes,np.mean(batchtimes),np.std(batchtimes))
            stuff2[variance][error]['minibatchtimes']=(minibatchtimes,np.mean(minibatchtimes),np.std(minibatchtimes))
    pickle.dump(stuff2,open('Logs/erroranalysisanalysed','wb'))

def acawithwithoutsfa():
    averagetruthranges = findtruthranges()
    acascores = []
    hacascores=[]
    featureacascores = []
    featurehacascores=[]
    treducedsfafiveacascores =[]
    treducedsfafivehacascores=[]
    treducedsfatwentyhacascores=[]
    treducedsfatwentyacascores=[]
    treducedsfafullhacascores=[]
    treducedsfafullacascores=[]
    realacascores=[]
    realhacascores=[]
    for i in range(9):
        sample=i+1
        acatruthranges = []
        for j, point in enumerate(generate_data.acaboundaries['truth'][sample - 1][1:-1]):
            acatruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        featureacatruthranges = []
        for j, point in enumerate(generate_data.featureacaboundaries['truth'][sample - 1][1:-1]):
            featureacatruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        realacatruthranges = []
        for j, point in enumerate(generate_data.realacaboundaries['truth'][sample - 1][1:-1]):
            realacatruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        treducedfafivetruthranges = []
        for j, point in enumerate(generate_data.treducedsfafive['truth'][sample - 1][1:-1]):
            treducedfafivetruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        treducedfatwentytruthranges = []
        for j, point in enumerate(generate_data.treducedsfatwenty['truth'][sample - 1][1:-1]):
            treducedfatwentytruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
        treducedfafulltruthranges = []
        for j, point in enumerate(generate_data.treducedsfafull['truth'][sample - 1][1:-1]):
            treducedfafulltruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))

        acascore=boundaryevaluate(generate_data.acaboundaries['aca'][sample-1],acatruthranges)
        acascores.append(acascore)
        hacascore = boundaryevaluate(generate_data.acaboundaries['haca'][sample - 1], acatruthranges)
        hacascores.append(hacascore)
        featureacascore = boundaryevaluate(generate_data.featureacaboundaries['aca'][sample - 1], featureacatruthranges)
        featureacascores.append(featureacascore)
        featurehacascore = boundaryevaluate(generate_data.acaboundaries['haca'][sample - 1], featureacatruthranges)
        featurehacascores.append(featurehacascore)
        treducedsfafivescore = boundaryevaluate(generate_data.treducedsfafive['aca'][sample - 1], treducedfafivetruthranges)
        treducedsfafiveacascores.append(treducedsfafivescore)
        treducedsfafivehacascore = boundaryevaluate(generate_data.treducedsfafive['haca'][sample - 1], treducedfafivetruthranges)
        treducedsfafivehacascores.append(treducedsfafivehacascore)
        treducedsfafullhacascore = boundaryevaluate(generate_data.treducedsfafull['haca'][sample - 1], treducedfafulltruthranges)
        treducedsfafullhacascores.append(treducedsfafullhacascore)
        treducedsfatwentyhacascore = boundaryevaluate(generate_data.treducedsfatwenty['haca'][sample - 1], treducedfatwentytruthranges)
        treducedsfatwentyhacascores.append(treducedsfatwentyhacascore)
        treducedsfafullacascore = boundaryevaluate(generate_data.treducedsfafull['aca'][sample - 1], treducedfafulltruthranges)
        treducedsfafullacascores.append(treducedsfafullacascore)
        treducedsfatwentyacascore = boundaryevaluate(generate_data.treducedsfatwenty['aca'][sample - 1], treducedfatwentytruthranges)
        treducedsfatwentyacascores.append(treducedsfatwentyacascore)
        realacascore=boundaryevaluate(generate_data.realacaboundaries['aca'][sample-1],realacatruthranges)
        realacascores.append(realacascore)
        realhacascore = boundaryevaluate(generate_data.realacaboundaries['haca'][sample - 1], realacatruthranges)
        realhacascores.append(realhacascore)
    print('Normal ACA')
    print(acascores)
    print(np.mean([x[0] for x in acascores]))
    print(np.mean([x[1] for x in acascores]))
    print('five treduced ACA')
    print(treducedsfafiveacascores)
    print(np.mean([x[0] for x in treducedsfafiveacascores]))
    print(np.mean([x[1] for x in treducedsfafiveacascores]))
    print('twenty treduced ACA')
    print(treducedsfatwentyacascores)
    print(np.mean([x[0] for x in treducedsfatwentyacascores]))
    print(np.mean([x[1] for x in treducedsfatwentyacascores]))
    print('full treduced ACA')
    print(treducedsfafullacascores)
    print(np.mean([x[0] for x in treducedsfafullacascores]))
    print(np.mean([x[1] for x in treducedsfafullacascores]))
    print('Before treduction')
    print(featureacascores)
    print(np.mean([x[0] for x in featureacascores]))
    print(np.mean([x[1] for x in featureacascores]))
    print('Before treduction')
    print(realacascores)
    print(np.mean([x[0] for x in realacascores]))
    print(np.mean([x[1] for x in realacascores]))
    print('*'*50)
    print('normal haca')
    print(hacascores)
    print(np.mean([x[0] for x in hacascores]))
    print(np.mean([x[1] for x in hacascores]))
    print('treduced haca')
    print(treducedsfafivehacascores)
    print(np.mean([x[0] for x in treducedsfafivehacascores]))
    print(np.mean([x[1] for x in treducedsfafivehacascores]))
    print('treduced haca')
    print(treducedsfatwentyhacascores)
    print(np.mean([x[0] for x in treducedsfatwentyhacascores]))
    print(np.mean([x[1] for x in treducedsfatwentyhacascores]))
    print('treduced haca')
    print(treducedsfafullhacascores)
    print(np.mean([x[0] for x in treducedsfafullhacascores]))
    print(np.mean([x[1] for x in treducedsfafullhacascores]))
    print('feature haca')
    print(featurehacascores)
    print(np.mean([x[0] for x in featurehacascores]))
    print(np.mean([x[1] for x in featurehacascores]))
    print('real haca')
    print(realhacascores)
    print(np.mean([x[0] for x in realhacascores]))
    print(np.mean([x[1] for x in realhacascores]))

def truetoyacawithwithoutsfa():
    acascores=[]
    hacascores=[]
    featureacascores=[]
    featurehacascores=[]
    for i in range(9):
        sample=i+1
        truthranges = []
        for j, point in enumerate(generate_data.truetoydata['truth'][sample - 1][1:-1]):
            truthranges.append((point, (point - 25, point + 25)))
        acascore = boundaryevaluate(generate_data.truetoydata['aca'][sample - 1], truthranges)
        acascores.append(acascore)
        hacascore = boundaryevaluate(generate_data.truetoydata['haca'][sample - 1], truthranges)
        hacascores.append(hacascore)
        featureacascore = boundaryevaluate(generate_data.truetoydatafeatures['aca'][sample - 1], truthranges)
        featureacascores.append(featureacascore)
        featurehacascore = boundaryevaluate(generate_data.truetoydatafeatures['haca'][sample - 1], truthranges)
        featurehacascores.append(featurehacascore)
    print('normal aca')
    print(acascores)
    print(np.mean([x[0] for x in acascores]))
    print(np.mean([x[1] for x in acascores]))
    print('normal haca')
    print(hacascores)
    print(np.mean([x[0] for x in hacascores]))
    print(np.mean([x[1] for x in hacascores]))
    print('normal featureaca')
    print(featureacascores)
    print(np.mean([x[0] for x in featureacascores]))
    print(np.mean([x[1] for x in featureacascores]))
    print('normal featurehaca')
    print(featurehacascores)
    print(np.mean([x[0] for x in featurehacascores]))
    print(np.mean([x[1] for x in featurehacascores]))


def algcomparison2():
    for i in range(9):
        segmentstocompare=[]
        sample=i+1
        data=np.loadtxt('logs/truetoydata'+str(sample))
        boundaries=np.loadtxt('logs/truetoydataboundaries'+str(sample))
        truthranges=[(1,(0,2))]
        for point in boundaries[1:]:
            truthranges.append((point,(point-25,point+25)))
        acaboundaries=generate_data.truetoydata['aca'][sample-1]
        hacaboundaries=generate_data.truetoydata['haca'][sample-1]
        batchboundaries=[0]+FullBatch(data,10,750)+[boundaries[-1]]
        minibatchboundaries=[0]+minibatch(data,1000)+[boundaries[-1]]
        print(batchboundaries)
        print(truthranges)
        fullbatchscore = boundaryevaluate(batchboundaries, truthranges)
        fullbatchscore = [round(x, 1) for x in fullbatchscore]
        minibatchscore = boundaryevaluate(minibatchboundaries, truthranges)
        minibatchscore = [round(x, 1) for x in minibatchscore]
        acascore = boundaryevaluate(acaboundaries, truthranges)

        acascore = [round(x, 1) for x in acascore]
        hacascore = boundaryevaluate(hacaboundaries,truthranges)
        hacascore = [round(x, 1) for x in hacascore]
        segmentstocompare.append((batchboundaries, 'Batch', str(fullbatchscore)))
        segmentstocompare.append((minibatchboundaries, 'Minibatch', str(minibatchscore)))
        segmentstocompare.append((generate_data.acaboundaries['aca'][sample - 1], 'ACA', str(acascore)))
        segmentstocompare.append((generate_data.acaboundaries['haca'][sample - 1], 'HACA', str(hacascore)))
        segmentstocompare=[(acaboundaries,'ACA',str(acascore)),(hacaboundaries,'HACA',str(hacascore)),(batchboundaries,'Batch',str(fullbatchscore)),(minibatchboundaries,'Minibatch',str(minibatchscore))]
        comparetotruth((truthranges,'Truth',''),segmentstocompare,1500)

    plt.show()

def Statisticalanalysis():
    dic = pickle.load(open('Logs/erroranalysisanalysed', 'rb'))
    for i, key in enumerate(sorted(dic)):

        variancedic = dic[key]
        xaxisbatch = []
        yaxisbatch = []
        stdbatch = []
        yaxisbatchmissed = []
        stdbatchmissed = []
        yaxisminibatch = []
        stdminibatch = []
        yaxisminibatchmissed = []
        stdminibatchmissed = []
        acafeature=[]
        hacafeature=[]
        acafull=[]
        hacafull=[]
        batchtimes=[]
        minibatchtimes=[]
        for j,error in enumerate(sorted(variancedic.keys())):
            acafeaturetruth=generate_data.toydatafeature[i][j]['truth']
            acafulltruth=generate_data.toydatafull[i][j]['truth']
            acafeaturetruthranges=[(x,(x-25,x+25)) for x in acafeaturetruth[1:-1]]
            acafulltruthranges=[(x,(x-25,x+25)) for x in acafulltruth[1:-1]]
            current = variancedic[error]
            xaxisbatch.append(error)
            yaxisbatch.append(current['batchscores'][1])
            stdbatch.append(current['batchscores'][2])
            yaxisbatchmissed.append(current['batchmisses'][1])
            stdbatchmissed.append(current['batchmisses'][2])
            yaxisminibatch.append(current['minibatchscores'][1])
            stdminibatch.append(current['minibatchscores'][2])
            yaxisminibatchmissed.append(current['minibatchmisses'][1])
            stdminibatchmissed.append(current['minibatchmisses'][2])
            batchtimes.append(current['batchtimes'][1])
            minibatchtimes.append(current['minibatchtimes'][1])
            acafeature.append(boundaryevaluate(generate_data.toydatafeature[i][j]['aca'],acafeaturetruthranges))
            hacafeature.append(boundaryevaluate(generate_data.toydatafeature[i][j]['haca'],acafeaturetruthranges))
            acafull.append(boundaryevaluate(generate_data.toydatafull[i][j]['aca'],acafulltruthranges))
            hacafull.append(boundaryevaluate(generate_data.toydatafull[i][j]['haca'],acafulltruthranges))
        print(np.mean(batchtimes))
        print(np.mean(minibatchtimes))
        plt.subplot(2, len(dic.keys()), i + 1)
        plt.ylabel('Error')
        # plt.errorbar(xaxisbatch, yaxisbatch, yerr=stdbatch, label='batch')
        # plt.errorbar([x + 0.0005 for x in xaxisbatch], yaxisminibatch, yerr=stdminibatch, c='red', label='minibatch', linestyle='--')
        plt.plot(xaxisbatch,[x[0] for x in acafull],'--',c='red',label='ACA')
        plt.plot(xaxisbatch,[x[0] for x in hacafull],c='red',label='HACA')
        plt.plot(xaxisbatch,[x[0] for x in acafeature],'--',c='blue',label='ACA feature')
        plt.plot(xaxisbatch,[x[0] for x in hacafeature],c='blue',label='HACA feature')
        plt.xlabel('noise level')
        plt.title('Variance = ' + str(key))
        plt.legend()
        plt.subplot(2, len(dic.keys()), i + 1 + len(dic.keys()))

        # plt.errorbar(xaxisbatch, yaxisbatchmissed, yerr=stdbatchmissed, label='batch')
        # plt.errorbar([x + 0.0005 for x in xaxisbatch], yaxisminibatchmissed, yerr=stdminibatchmissed, c='red', label='minibatch', linestyle='--')
        plt.ylabel('Missed')
        plt.plot(xaxisbatch,[x[1] for x in acafull],'--',c='red',label='ACA')
        plt.plot(xaxisbatch,[x[1] for x in hacafull],c='red',label='HACA')
        plt.plot(xaxisbatch,[x[1] for x in acafeature],'--',c='blue',label='ACA feature')
        plt.plot(xaxisbatch,[x[1] for x in hacafeature],c='blue',label='HACA feature')
        plt.legend()
        plt.xlabel('noise level')
        plt.title('Variance = ' + str(key))
    plt.show()

def handsegcompare():
    stufferino = np.loadtxt('handseg1.txt')
    segcompare = []
    truthranges = [(1, (1, 1)), (24, (20, 30)), (81, (75, 85)), (165, (160, 170)), (233, (228, 238)), (282, (282, 282))]
    print(stufferino.shape)
    asdf = [1] + FullBatch(stufferino, 5, 75) + [282]
    segcompare.append((asdf, 'Batch', str(boundaryevaluate(asdf, truthranges[1:-1]))))
    asdf2 = [1] + minibatch(stufferino, 140, reducenumber=9) + [282]
    segcompare.append((asdf2, 'Minibatch', str(boundaryevaluate(asdf2[1:], truthranges[1:-1]))))
    segcompare.append(([1, 21, 33, 53, 74, 169, 210, 282], 'handKKV', str(boundaryevaluate([1, 21, 33, 53, 74, 169, 210, 282], truthranges[1:-1]))))
    print(asdf2)
    comparetotruth((truthranges, 'Truth', ''), segcompare, 100)
    segcompare = []
    stufferino = np.loadtxt('handseg2.txt')
    truthranges = [(1, (1, 1)), (15, (10, 20)), (83, (78, 88)), (162, (157, 167)), (187, (182, 192)), (215, (215, 215))]
    asdf = [1] + FullBatch(stufferino, 6, 90) + [215]
    segcompare.append((asdf, 'Batch', str(boundaryevaluate(asdf, truthranges[1:-1]))))
    asdf2 = [1] + minibatch(stufferino, 100, reducenumber=9) + [215]
    segcompare.append((asdf2, 'Minibatch', str(boundaryevaluate(asdf2[1:], truthranges[1:-1]))))
    segcompare.append(([1, 18, 61, 163, 182, 215], 'handKKV', str(boundaryevaluate([1, 18, 61, 163, 182, 215], truthranges[1:-1]))))
    comparetotruth((truthranges, 'Truth', ''), segcompare, 100)
    plt.show()

def windowsizefinal():
    numiterations=5
    plt.figure()

    for i in range(numiterations):
        lengthshort=750
        lengthright=1000
        lengthlong=1250
        lengthterrible=1500
        data,boundaries=generate_data.toydata2(numblocks=5)
        ax=plt.subplot(numiterations,3,1+i*3)
        startpoint=(boundaries[0]+boundaries[1])/2
        ax.add_patch(patches.Rectangle((startpoint,0),lengthshort,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthshort],lengthshort)[0]
        plt.scatter(boundary+startpoint,1,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,2.5),lengthright,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthright],lengthright)[0]
        plt.scatter(boundary+startpoint,3.5,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,5),lengthlong,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthlong],lengthlong)[0]
        plt.scatter(boundary+startpoint,6,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,7.5),lengthterrible,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthterrible],lengthterrible)[0]
        plt.scatter(boundary+startpoint,8.5,marker='x',s=250)
        for point in boundaries:
            plt.plot([point,point],[0,10],'black')
        ax=plt.subplot(numiterations,3,2+i*3)
        startpoint=(boundaries[1]+boundaries[1])/2
        ax.add_patch(patches.Rectangle((startpoint,0),lengthshort,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthshort],lengthshort)[0]
        plt.scatter(boundary+startpoint,1,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,2.5),lengthright,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthright],lengthright)[0]
        plt.scatter(boundary+startpoint,3.5,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,5),lengthlong,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthlong],lengthlong)[0]
        plt.scatter(boundary+startpoint,6,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,7.5),lengthterrible,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthterrible],lengthterrible)[0]
        plt.scatter(boundary+startpoint,8.5,marker='x',s=250)
        for point in boundaries:
            plt.plot([point,point],[0,10],'black')
        ax=plt.subplot(numiterations,3,3+i*3)
        startpoint=(boundaries[2]+boundaries[1])/2
        ax.add_patch(patches.Rectangle((startpoint,0),lengthshort,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthshort],lengthshort)[0]
        plt.scatter(boundary+startpoint,1,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,2.5),lengthright,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthright],lengthright)[0]
        plt.scatter(boundary+startpoint,3.5,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,5),lengthlong,2,alpha=0.2,facecolor='red'))
        boundary=minibatch(data[startpoint:startpoint+lengthlong],lengthlong)[0]
        plt.scatter(boundary+startpoint,6,marker='x',s=250)

        ax.add_patch(patches.Rectangle((startpoint,7.5),lengthterrible,2,alpha=0.2,facecolor='blue'))
        boundary=minibatch(data[startpoint:startpoint+lengthterrible],lengthterrible)[0]
        plt.scatter(boundary+startpoint,8.5,marker='x',s=250)
        for point in boundaries:
            plt.plot([point,point],[0,10],'black')
    plt.show()


#first_attempt()
#second_attempt()
#minibatchtest()
#minibatchprettypicture()
#windowsizetest()
#manywindows()
#numfeaturesminibatch()
#windowsize2()
#exactboundaries()
#exactboundariespicture()
#windowsizeminibatch()
#windowsizeminibatch2()
#highvariancedata()
#highvariancedatavariablesscalefactor()
#highvariancedata3graph()
#doubletripletest()
#doubletriplediagram()
#realdatacomparison()
#realdatacomparisondiagram()
#smoldatatest()
#smoltest2()
#smoldtwtest()
#smoltest3()
#generate_features()
#smoltest5()
#windowsizetest4()
#toydatapaper()
#varianceanalysis()
#erroranalysis()
#toydataexample()
#realdataclusterlists()
#toydataexample2()
#boundarycomparisons()
#smoltest6()
#boxtest()
#clustertest()
#findbestminibatch(9)
# algcomparison()
#erroranalysisdata()
#acasfatest()
#erroranalysisextra()
# acawithwithoutsfa()
# truetoyacawithwithoutsfa()
# algcomparison2()
#windowsizefinal()
#highvariancedata()
#highvariancedatavariablesscalefactor()
# erroranalysisextra()

# Statisticalanalysis()
handsegcompare()

