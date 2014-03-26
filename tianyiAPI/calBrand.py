# -*- coding: UTF-8 -*-
'''
获取用户上传的Demo.txt 文件中的推荐的Brand总数。
与此同时，计算下个月成交的总记录.
rpath 为Demo.txt的路径

'''
def getNumOfBrandOfDemo(rpath,precision, recall):
	fr=open(rpath,"r")
	lenOfBrand = 0
	for line in fr :
		line = line.strip().split("\t")
		listFromLine = set(line[1].split(","))
		lenOfBrand += len(listFromLine)
	totalNumOfRealBuy = lenOfBrand * precision / recall
	print("The number of Recommend Brand is : %d \
		The total numbetr of real bought: %d" %(lenOfBrand , totalNumOfRealBuy))
	fr.close()


if __name__ == '__main__':
	getNumOfBrandOfDemo(rpath = "demo315.txt",precision=0.0437,recall=0.0136)
	getNumOfBrandOfDemo(rpath = "demo_322.txt",precision=0.0487,recall=0.0819)