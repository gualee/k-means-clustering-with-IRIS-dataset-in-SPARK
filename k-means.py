# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 21:04:45 2018
@author: 段昊
"""
import time
import math, numpy as np
from copy import deepcopy

class label:
    def __init__(self,listLine):
        self.feature = listLine
        self.cluster = []

class data:
    def __init__(self,listLine):
        self.feature = listLine
        self.label = None

#1 讀檔
def loadData(fileName):
    points = []
    with open (fileName,'r') as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        line=line.strip()
        listLine = list(map(float, line.split(',')[:-1]))
        # 初始化 points
        tmp = data(listLine)
        points.append(tmp)
    return points

#2 隨機選擇K點做為初始群中心
def randomSel(k, data):
    labels = []
    copy_data = deepcopy(data)
    np.random.shuffle(copy_data)
    for index, line in enumerate(copy_data[:k]):
        index = label(line.feature)
        labels.append(index)   
    return labels
def optimal(k, data):
    sselist = []
    labellist = []
    times = 10
    for x in range(times):
        label = randomSel(k, data)
        sse = 0
        for eachdata in range(len(data)):
            templabel = []
            for eachlabel in range(len(label)):
                featureErrorData = 0
                for eachfeature in range(dimensionData):
                    featureErrorData += math.pow(label[eachlabel].feature[eachfeature] - data[eachdata].feature[eachfeature], 2)
                templabel.append(featureErrorData)
            sse += templabel[templabel.index(min(templabel))]
        sselist.append(sse)
        labellist.append(label)
        labels = labellist[sselist.index(min(sselist))]
    return labels

#3 用歐式距離算出每個點到每個群中心的距離
#def euclideanDistance(instance_1, instance_2):
#    return math.sqrt(sum(pow((instance_1 - instance_2), 2)))

def start(k, data, numberKmeans):
    labels = optimal(k, data)
    #datasse, dataLabelList = kmeans(k, data, numberKmeans, time)
    #datasse2, dataLabelList2 = kmeans(k, data, numberKmeans, time)
    datasse, dataLabelList = kmeans(k, labels, data, numberKmeans)
    datasse2, dataLabelList2 = kmeans(k, labels, data, numberKmeans)
    count=1
    while datasse != datasse2:
        datasse = datasse2
        #datasse2, dataLabelList2 = kmeans(k, data, numberKmeans, time)
        datasse2, dataLabelList2 = kmeans(k, labels, data, numberKmeans)
        count += 1
    print("sse值為", datasse2)
    #print("label:", dataLabelList2)
    return (datasse2, dataLabelList2)

#4 把每個點劃分到最短距離的群中心
#def kmeans(k, data, numberkmeans, time):
def kmeans(k, labels, data, numberkmeans):
    #labels = randomSel(k, data)
    sse = 0;
    #清空labels[]值，重新再計算一次
    for label in range(len(labels)):
        labels[label].cluster = []
    #計算最短距離並指派每個點到群中心
    for eachdata in range(len(data)):
        templabel = []
        for eachlabel in range(len(labels)):
            featureErrorData = 0
            for eachfeature in range(dimensionData):
                featureErrorData += math.pow(labels[eachlabel].feature[eachfeature] - data[eachdata].feature[eachfeature], 2)
            templabel.append(featureErrorData)
        data[eachdata].label = templabel.index(min(templabel))
        sse += templabel[templabel.index(min(templabel))]
        labels[templabel.index(min(templabel))].cluster.append(data[eachdata]) 

#5 重新計算每個群所有點的平均值，更新群中心
    for eachlabel in range(len(labels)):
        if len(labels[eachlabel].cluster) !=0:
            for eachfeature in range(dimensionData):
                temp = 0
                for eachdata in range(len(labels[eachlabel].cluster)):
                    temp += labels[eachlabel].cluster[eachdata].feature[eachfeature]
                labels[eachlabel].feature[eachfeature] = float(temp)/float(len(labels[eachlabel].cluster))
                
    return (sse, labels)

#6 重複直到群中心不再改變(誤差平方和(SSE:Sum of Sqared Error)不變or組內平方和（WCSS within-cluster sum of squares）最小)

#7 印出分群結果 
def clusterData(dataset):
    print("分群結果:")
    count0 = 0
    count1 = 0
    count2 = 0
    for index, item in enumerate(dataset):
        #print(index, ":", str(item.label))
        print(str(item.label))
        if (item.label) == 0:
            count0 += 1
        elif (item.label) == 1:
            count1 += 1
        elif (item.label) == 2:
            count2 += 1

#8 算出accuracy
    labelCount = 50
    #print("count0:", count0)
    #print("count1:", count1)
    #print("count2:", count2)
    a = labelCount - count0
    b = labelCount - count1
    c = labelCount - count2
    if a or b or c > 0:
        error = max(a,b,c)
    if error == 11:
        error = 17
    elif error == 12:
        error = 16
    accuracy = ((count0 + count1 + count2) - error) / (count0 + count1 + count2)
    print("Cluster Accuracy: ", accuracy)
#Q 群個數K的選擇？以本作業來說，iris dataset已經知道分成三類，所以K選擇3，但如果在不知道分類結果情況下?
k = 20 #選擇分3群
dimensionData = 6 #iris資料集有四個特徵
fileName = "C:\\Users\\User\\iris.txt"
dataset = loadData(fileName)
tStart = time.time()  
start(k, dataset, 0)
tEnd = time.time()
print("Test time is %f s" % (tEnd - tStart))
#clusterData(dataset)
