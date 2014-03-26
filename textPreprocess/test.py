# -*- coding: UTF-8 -*-
import numpy as np 
from numpy import *

sc=np.load("D:\Python27\jyc_test_ali\scoreMat.npy")
#U,Sigma,VT = linalg.svd([[1,1],[7,7]])
#U,Sigma,VT = linalg.svd(sc)

#svdRec.recommend(myMat,2)

'''
from numpy import *

def indexTest():
	aMat=zeros((4,5))
	bMat=zeros(4)
	print aMat
	print bMat

	bMat[2]=5
	bMat[3]=9
	print bMat
	print "---------"
	print list(enumerate(bMat))


	#获取item=9的下标index
	for index,item in (enumerate(bMat)):
		if item==9:
			print index
			print item

#dic test 
def dicTest():	
	dicTest={}
	aa='jycAge'
	dicTest[aa]=33
	bb=12
	dicTest[bb]=97
	print dicTest
	print dicTest.get('aa',12)

'''
#list dic test
def arrayDicTest():
	userAllID[] = {}

'''

if __name__ == '__main__':
	indexTest()
	dicTest()
'''


