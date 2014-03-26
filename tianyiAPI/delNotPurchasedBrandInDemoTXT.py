# -*- coding: UTF-8 -*-
import numpy as np
from numpy import *
'''
获取用户上传的Demo.txt 文件中的推荐的Brand总数。
与此同时，计算下个月成交的总记录.
rpath 为Demo.txt的路径

'''
def getNumOfBrandOfSubmitTXT(rpath,precision = 0.0437, recall = 0.0819):
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

#删除所有BrandID中仅仅被点击了，但是没有被收藏、购物车和购买的BrandID
def delNotPurchasedBrandInDemo() :
	numOfNotPurchased = 0
	flagDispComma = 0  #控制是否显示第一个brand前面的逗号
	notPurchasedBrand = np.load("notPurchasedBrand.npy")
	print("The number of notPurchasedBrand:%d " %(len(notPurchasedBrand)))
	rpath = "demo_322.txt"
	wpath = "demo_322_del_brand.txt"
	fr = open(rpath,"r")
	fw = open(wpath,"w")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List
		listBrand = listUserBrand[1].split(",")  #购买的品牌List
		fw.write(listUserBrand[0] + "\t")
		for brandID in listBrand :
			if int(brandID) not in notPurchasedBrand :
				if flagDispComma ==0 : 	
					fw.write(brandID)					
					flagDispComma =1
				else :			
					fw.write(","+brandID)
				#print brandID
			else :
				#print brandID
				numOfNotPurchased += 1
		flagDispComma = 0
		fw.write("\n")
	print("There are %d in notPurchasedBrand. \n" %numOfNotPurchased) 	
	fr.close()
	fw.close()
	#getNumOfBrandOfSubmitTXT(wpath)

	X=289.;	Y=5940.-497. ;	Z=3532.
	P=X/Y ; 	R=X/Z
	F1=(2.*P*R)/(P+R)
	print F1
	print "\n"

	X=289.;	Y=5337;	Z=3532.
	P=X/Y ; 	R=X/Z
	F1=(2.*P*R)/(P+R)
	print F1
	print "\n"	

#计算其他人提交的Brand总数
def calcNumOfOthersBrand(rank,P,R):
	Y=(R*3532)/P
	print("The submit number of Top%d is %d: " %(rank,Y))
def dipNumOfOthersBrand():
	calcNumOfOthersBrand(1,0.0747,0.0689)
	calcNumOfOthersBrand(2,0.0809,0.0607)
	calcNumOfOthersBrand(3,0.0816,0.0601)
	calcNumOfOthersBrand(4,0.0751,0.0629)
	calcNumOfOthersBrand(5,0.0944,0.0536)
	calcNumOfOthersBrand(6,0.0683,0.0683)
	calcNumOfOthersBrand(7,0.0830,0.0570)
	calcNumOfOthersBrand(8,0.0701,0.0649)
	calcNumOfOthersBrand(9,0.0680,0.0661)
	calcNumOfOthersBrand(10,0.1068,0.0488)

#删除没有购买记录或者不会再购买的用户的所有数据
def delUserOfNotPurchase():
	numOfNotPurchasedUser = 0
	notPurchasedUser = np.load("noPurchaseGuy.npy")
	print("The number of notPurchasedBrand:%d " %(len(notPurchasedUser)))
	rpath = "demo_322_del_brand.txt"
	wpath = "demo_322_del_brand_user.txt"
	fr = open(rpath,"r")
	fw = open(wpath,"w")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List [userID,brandID]
		if int(listUserBrand[0]) in notPurchasedUser :
			numOfNotPurchasedUser += 1
		else :
			fw.write(line)

	print("There are %d in NotPurchasedUser. \n" %numOfNotPurchasedUser) 
	fr.close()
	fw.close()
	getNumOfBrandOfSubmitTXT(wpath)


'''
@jyc
删除给用户的过多的推荐数目：
1、删除这五月购买次数少于1的user；
2、根据用户这五个月的购买次数进行推荐，设五个月的购买次数为N则：
	N < 1 : 删除此用户；
	1 < N < 3: N*2(去尾)
	3 < N < 5: 取N=4/5 
	N > 5    : 取N=10
'''
def  delOverBrand():
	flagDispComma = 0  #控制是否显示第一个brand前面的逗号
	averagePurchasedTimes = np.load("userAveragePurchaseTime.npy")
	rpath = "demo_322_del_brand_user.txt"
	wpath = "demo_322_del_brand_user_overbrand.txt"
	fr = open(rpath, "r")
	fw = open(wpath, "w")

	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List[user, brand]
		listBrand = listUserBrand[1].split(",")  #购买的品牌List
		for user, times in averagePurchasedTimes :
			if user == int(listUserBrand[0]) :   # 选出改行用户user在矩阵中的对应的购买次数times
				#if times < 1:  do noting
				if times >= 0.2 :
					if 0.2<= times <=3 : times = 6#int(times * 2)
					#elif 3< times <=5 : times = 5
					elif times > 3:	times=10
					#将每一行的前times个brand写入文件，即写入listBrand[:int(times)]
					fw.write(listUserBrand[0] + "\t")
					for brandID in listBrand[:int(times)] :
						if flagDispComma == 0 : 	
							fw.write(brandID)	
							flagDispComma = 1
						else :			
							fw.write(","+brandID)
					fw.write("\n")
					flagDispComma = 0
	getNumOfBrandOfSubmitTXT(wpath)
	print("Done")
	fr.close()
	fw.close()
	

if __name__ == '__main__':
	#delNotPurchasedBrandInDemo()
	#dipNumOfOthersBrand()
	#delUserOfNotPurchase()
	delOverBrand()
