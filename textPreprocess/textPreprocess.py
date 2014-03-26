# -*- coding: UTF-8 -*-
from numpy import *
import numpy as np
import operator
import string
from os import listdir

'''
@jyc
test.txt
get userid_item_score file
weight of action:  shot:0-1; buy:1-10; favor:2-5;  cart:3-10
将原始数据raw_data.txt进行处理，得到 userID、itemID、score文件
userid_item_score.txt
'''
def getScore():
    itemTemp="0"; userTemp="0"
    score=0
    rpath="raw_data_utf8.txt"
    #rpath="test.txt"
    wpath="userid_item_score.txt"
    #只取出第一行作为 itemTemp 
    fr=open(rpath,"r")    
    for line in fr:
        linestr=line.split(",")
        itemTemp = linestr[1]
        break    
    fr.close()
    fw=open(wpath,"w")
    fr=open(rpath,"r")
    for line in fr:
        linestr=line.split(",")
        if linestr[1] != itemTemp :
            fw.write(userTemp+"\t"+itemTemp+"\t"+str(score)+"\n")  #将前一个结果写入文件，所以最后要新加一行
            score=0
        #进行 打分
        if   linestr[2]=="0":   score +=1
        elif linestr[2]=="1":   score +=10
        elif linestr[2]=="2":   score +=5
        elif linestr[2]=="3":   score +=10
        itemTemp = linestr[1]
        userTemp = linestr[0]
    #写入最后一行
    fw.write(userTemp+"\t"+itemTemp+"\t"+str(score)+"\n")
    fr.close()
    fw.close()
    print("-----------------------------getScore() have run： have got userid_item_score")

'''
@jyc
将文件userid_item_score.txt中的item的重复项进行处理、累加。
得到文件userid_item_score_del-reitem.txt
'''
def delReItem():
    userID="0"
    itemScore={}
    rpath="userid_item_score.txt"
    wpath="userid_item_score_del-reitem.txt"
    #只取出第一行,初始化userID 
    fr=open(rpath,"r")    
    for line in fr:
        linestr=line.split("\t")
        userID = linestr[0]
        break    
    fr.close()

    fw=open(wpath,"w")
    fr=open(rpath,"r")
    for line in fr:
        linestr=line.split("\t")
        #判断是否为同一个userID
        if linestr[0] != userID :
            #写入文件
            for (item,num) in itemScore.iteritems() :
                fw.write(userID+"\t"+str(item)+"\t"+str(num)+"\n")
            itemScore.clear()
        #字典里面没有数据，加0后，加入；有该数据，加上该数据的值，然后加入
        itemScore[linestr[1]] = itemScore.get(linestr[1],0) + int(linestr[2])
        userID = linestr[0]
    #打印、写入最后一组数据
    for (item,num) in itemScore.iteritems() :
        fw.write(userID+"\t"+str(item)+"\t"+str(num)+"\n")
    fr.close()
    fw.close()
    print "-----------------------------delReItem() have run：" 

'''
@jyc
test.txt
get the number of item and user
获取品牌brand和用户user的数目。
并返回升序排序的所有品牌组成的数组itemAll
'''    
def getNumOfItemUser():
    i=0; userID="0"
    rpath="raw_data_utf8.txt"
    #rpath="test.txt"
    wpath="userid_item_score_test.txt"  #未使用
    itemAll=[]
    userAll=[]
    fw=open(wpath,"w")
    fr=open(rpath,"r")
    for line in fr:
        linestr=line.split(",")
        itemAll.append(int(linestr[1]))
        userAll.append(int(linestr[0]))
        if linestr[0] != userID :
            i += 1 
        userID = linestr[0]
    fr.close()
    fw.close() 
    #print the number
    print("The number of line is: %d. The number of line is %d" %(len(itemAll),len(userAll)) )   
    itemAll=set(itemAll)
    userAll=set(userAll)
    print("The number of item is: %d. The number of user is: %d" %(len(itemAll),len(userAll)) )
    itemAll=list(itemAll)
    userAll=list(userAll)
    #判断用户userID在后面是否间隔重复出现（同一用户的itemID是重复出现的）
    if i == len(userAll) :
        print("i is %d，equal with 'userAll' ,which explain that the user is in order" %i) 

    itemAll.sort() #小-->大
    #print itemAll
    userAll.sort() #小-->大
    #print userAll
    #print len(userAll)
    print "-----------------------------getNumOfItemUser() have run：" 
    return itemAll

'''
@jyc
将userid_item_score_del-reitem.txt文件中，
同一UserID的itemID和score放入字典userDict中，
再取出数据写入文件itemIDScore.txt（或者矩阵、数组）中
'''
def getFileOfItemScore():
    userDict={}
    userID="0"
    userAllID=[]    #对应存放itemIDScore.txt文件的每一行代表的ID
    itemAll = getNumOfItemUser()
    rpath="userid_item_score_del-reitem.txt"
    wpath="itemIDScoreTemp.txt"
    wpathP="itemIDScore.txt"
    #只取出第一行,初始化userID 
    fr=open(rpath,"r")    
    for line in fr:
        linestr=line.split("\t")
        userID = linestr[0]
        break    
    fr.close()
    fw=open(wpath,"w")
    fr=open(rpath,"r")    
    for line in fr:
        linestr=line.split("\t")
        #当userID变化时，把上一个缓存在字典中的数据写入文件，并清空字典
        if linestr[0] != userID :    
            #fw.write(userID+":")
            userAllID.append(userID)
            for item in itemAll :
                value = userDict.get(str(item),0)
                #fw.write(str(item)+"-"+str(value)+",")  
                fw.write(str(value)+",")   
            fw.write("\n")
            userDict.clear()
        userDict[linestr[1]] = int(linestr[2])
        userID=linestr[0]
    #写入最后一行
    #fw.write(userID+":")
    userAllID.append(userID)
    for item in itemAll :
        value = userDict.get(str(item),0)
        #fw.write(str(item)+"-"+str(value)+",")                
        fw.write(str(value)+",")                
    fw.write("\n")
    fr.close()
    fw.close() 
    #删除文件的最后一个逗号
    fr=open(wpath,"r")
    fw=open(wpathP,"w")
    for line in fr :
        line=line[:-2]
        fw.write(line+"\n")
    fr.close()
    fw.close() 
    return userAllID


'''
@jyc
将文件itemIDScore.txt转换成矩阵scoreMat。
返回：scoreMat,userLabelVector(即所有用户userAllID)
并保存为scoreMat.npy 矩阵文件
'''
def file2matrix():
    rpath="itemIDScore.txt"
    fr=open(rpath,"r")    
    arrayOLines=fr.readlines()
    #创建‘0’矩阵，维数：用户数--行、brand数--列
    linestr = arrayOLines[0].strip().split(",") #stripe去回车符
    userLabelVector=getFileOfItemScore()
    scoreMat = zeros((len(userLabelVector),len(linestr)))
    print len(linestr)
    print linestr
    index = 0
    for line in arrayOLines :
        line = line.strip()
        listFromLine = line.split(',')
        scoreMat[index,:] = map(int,listFromLine)
        index += 1     
    fr.close()
    print scoreMat
    print userLabelVector
    np.save("scoreMat.npy",scoreMat)
    print "scoreMat.npy save..."
    return scoreMat,userLabelVector

'''
获取评分最高的前N(10)项
'''
def getTopN(N=5):
    tempArray=[]
    userID = "0"
    rpath="userid_item_score_del-reitem.txt"
    wpathTemp="demo_322Temp.txt"
    wpath="demo_322.txt"
    fr=open(rpath,"r")    
    fw=open(wpathTemp,"w")     
    arrayOLines=fr.readlines()    
    userID = (arrayOLines[0].split("\t"))[0]
    print "userID:"+userID
    for line in arrayOLines :
        line =line.strip()
        listFromLine = line.split("\t")
        if listFromLine[0] == userID :
            tempArray.append([listFromLine[1],int( listFromLine[2])]) #save item,score in array
        else :
           # print tempArray
            tempArray = sorted(tempArray, key=lambda jj : jj[1], reverse=True)[:N]  #取前5个
            #print tempArray
            fw.write(userID + "\t")
            for x,y in tempArray :
                #fw.write(x+"-"+ str(y) + ",")
                fw.write(x + ",")
            fw.write("\n")
            tempArray=[]  #清空List，然后再加入append
            tempArray.append([listFromLine[1],int( listFromLine[2])]) #save item,score in array
        userID = listFromLine[0]
    ##写入最后一行
    tempArray = sorted(tempArray, key=lambda jj : jj[1], reverse=True)[:N]  #取前5个
    fw.write(userID + "\t")
    for x,y in tempArray :
        #fw.write(x+"-"+ str(y) + ",")
        fw.write(x + ",")
    fw.write("\n")
    fr.close()
    fw.close()
    ##删除最后一个逗号
    fr=open(wpathTemp,"r")
    fw=open(wpath,"w")
    for line in fr :
        line=line[:-2]
        fw.write(line+"\n")
    fr.close()
    fw.close() 


'''
@jyc
主函数
'''
if __name__ == '__main__':    
    getScore()
    delReItem()
    #getNumOfItemUser()
    userID = getFileOfItemScore()    
    print userID
    #file2matrix()
    getTopN(N=10)
