# -*- coding: UTF-8 -*-
import numpy as np
from numpy import *
import ali323
'''
选出没有购买行为的用户存储为notOnePurchaseUser.npy
'''
def selcOnOnePurchaseUser():
	allMt = load("data.npy")
	allUser = set(allMt[:,0])
	print len(set(allMt[:,0]))

	purchaseMt = ali323.getWithParameter(allMt,0 ,0 ,(1,),0 ,0)
	purcheseUser = set(purchaseMt[:,0])
	print len(set(purchaseMt[:,0]))
	notPurchaseUser = allUser.difference(purcheseUser)  #取出allUser不在purcheseUser中的部分
	print len(notPurchaseUser)
	print notPurchaseUser
	np.save("notOnePurchaseUser.npy", list(notPurchaseUser))
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

#删除所有BrandID中仅仅被点击了，但是没有被收藏、购物车和购买的BrandID
def delNotPurchasedBrandInDemo() :
	numOfNotPurchased = 0
	flagDispComma = 0  #控制是否显示第一个brand前面的逗号
	notPurchasedBrand = np.load("notPurchasedBrand.npy")
	#print("The number of notPurchasedBrand:%d " %(len(notPurchasedBrand)))
	rpath = "demo_322.txt"
	# rpath = "demo-jyc322.txt"
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
	fr.close()
	fw.close()
	#print("There are %d in notPurchasedBrand. \n" %numOfNotPurchased) 	
	print("demo-jyc322.txt : ")
	getNumOfBrandOfSubmitTXT(rpath)
	print("demo_322_del_brand.txt : ")
	#getNumOfBrandOfSubmitTXT(wpath)
'''
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
'''
#删除没有购买记录或者不会再购买的用户的所有数据
def delUserOfNotPurchase():
	numOfNotPurchasedUser = 0
	notPurchasedUser = np.load("noPurchaseGuy.npy")
	print("The number of notPurchasedBrand:%d " %(len(notPurchasedUser)))
	rpath = "demo_322_del_brand.txt"
	wpath = "demo_322_del_brand_user.txt"
	fr = open(rpath,"rb")
	fw = open(wpath,"wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List [userID,brandID]
		if int(listUserBrand[0]) in notPurchasedUser :
			numOfNotPurchasedUser += 1
		else :
			fw.write(line)
	fr.close()
	fw.close()
	print("There are %d in NotPurchasedUser. \n" %numOfNotPurchasedUser) 
	print("delUserOfNotPurchase() done. demo_322_del_brand_user.txt : ")	
	getNumOfBrandOfSubmitTXT(wpath)

'''
@jyc
删除给用户的过多的推荐数目：
1、删除这五月购买次数少于1的user；
2、根据用户这五个月的购买次数进行推荐，设五个月的购买次数为N则：
	N < 0.2     : 删除此用户；
	0.2 < N < 1 : modifyTimes*3(去尾) 
	1 < N < 3   : modifyTimes*2 
	3 < N < 5   : 取modifyTimes=5
	N > 5       : modifyTimes=10  
'''
def  delOverBrand():
	flagDispComma = 0  #控制是否显示第一个brand前面的逗号
	averagePurchasedTimes = np.load("userAveragePurchaseTime.npy")
	rpath = "demo_322_del_brand_user.txt"
	wpath = "demo_322_del_brand_user_overbrand.txt"
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")

	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List[user, brand]
		listBrand = listUserBrand[1].split(",")  #购买的品牌List
		for user, times in averagePurchasedTimes :
			if user == int(listUserBrand[0]) :   # 选出改行用户user在矩阵中的对应的购买次数times
				#if times < 1:  do noting
				if times > 0.2:
					if 0.2 < times <1 : modifyTimes = times*3#int(times * 2)
					elif 1 <= times < 3:	modifyTimes = times*2
					elif 3 <= times <=5 : modifyTimes = 5
					elif 5 < times:	modifyTimes=10

					#将每一行的前times个brand写入文件，即写入listBrand[:int(times)]
					fw.write(listUserBrand[0] + "\t")
					for brandID in listBrand[:int(modifyTimes)] :
						if flagDispComma == 0 : 	
							fw.write(brandID)	
							flagDispComma = 1
						else :			
							fw.write(","+brandID)
					fw.write("\n")
					flagDispComma = 0
	fr.close()
	fw.close()
	print("delOverBrand done. demo_322_del_brand_user_overbrand.txt :")
	getNumOfBrandOfSubmitTXT(wpath)
	
'''
@jyc
用户收藏购物车但是没有买过的,将其添加到结果里面。
注意：先判断结果里面有没有这个物品
'''	
def addSaveCartButNotPurchase() :
	flagDispComma = 0  #控制是否显示第一个brand前面的逗号
	flagDispEnter = 0  #控制是否显示第一个brand前面的逗号
	userIDAll= [] #存放rpath中所有用户的ID
	userIDTemp=0
	saveCartButNotPurchase = np.load("saveCartButNotPurchase.npy")
	notPurchasedUser = np.load("notOnePurchaseUser.npy")  #用于将没有购买行为，但是购物车有物品的user删除
	#print saveCartButNotPurchase
	saveCartButNotPurchase = sorted(saveCartButNotPurchase, key=lambda jj : jj[0], reverse=True) #降序排序
	#saveCartButNotPurchase = mat(saveCartButNotPurchase)
	#print saveCartButNotPurchase
	rpath = "demo_322_del_brand_user_overbrand.txt"
	wpath = "demo_322_del_brand_user_overbrand_addCartBrand.txt"
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List[user, brand]
		userIDAll.append(int(listUserBrand[0]))
		listBrand = listUserBrand[1].split(",")  #购买的品牌List
		for user, brand in saveCartButNotPurchase :
			if user == int(listUserBrand[0]) :   # 选出改行用户user在矩阵中的对应的购买次数times
				if str(brand) not in listBrand : #当矩阵中的brand没在该行时，添加进来
					listBrand.append(brand)
		#写入新文件：user brand newBrand
		fw.write(listUserBrand[0] + "\t")
		for brandID in listBrand :
			if flagDispComma == 0 : 	
				fw.write(brandID)	
				flagDispComma = 1
			else :			
				fw.write(","+str(brandID))
		fw.write("\n")
		flagDispComma = 0
	#添加 用户（源文件中没有的用户）加入购物车，但是没有购买的
	# print notPurchasedUser
	for user,brand in saveCartButNotPurchase :
		if user not in userIDAll :
			if int(user) not in notPurchasedUser :  #只添加有购买行为的用户
				if user != userIDTemp :
					if flagDispEnter == 0 :
						fw.write(str(user) + "\t" + str(brand))	
						flagDispEnter = 1
					else :
						fw.write("\n" + str(user) + "\t" + str(brand))
				else :
					fw.write("," + str(brand))
		userIDTemp = user 

	fr.close()
	fw.close()
	print("addSaveCartButNotPurchase done. demo_322_del_brand_user_overbrand_addCartBrand.txt :")	
	getNumOfBrandOfSubmitTXT(wpath)

'''
添加热门brand：将热门列表推荐给提交的最终用户，里面的每一个人。
'''	
def addHotBrand() :
	flagDispComma = 0
	rpath = "demo_322_del_brand_user_overbrand_addCartBrand.txt"
	wpath = "demo_322_del_brand_user_overbrand_addCartBrand-hotBrand.txt"
	mtHotBrand = np.load("hotPurchasedBrand.npy")
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2维List[user, brand]
		listBrand = listUserBrand[1].split(",")  #购买的品牌List
		for brandID in mtHotBrand :
			if str(brandID) not in listBrand : #如果热门brandID没有在改行的用户的brand中，则添加
				listBrand.append(str(brandID)) 
		#添加完成后，写入文件		

		#将每一行的前times个brand写入文件，即写入listBrand[:int(times)]
		fw.write(listUserBrand[0] + "\t")
		for brandID in listBrand :
			if flagDispComma == 0 : 	 #写逗号的标志位
				fw.write(brandID)	
				flagDispComma = 1
			else :			
				fw.write(","+brandID)
		fw.write("\n")
		flagDispComma = 0
	fr.close()
	fw.close()
	print("addHotBrand done. demo_322_del_brand_user_overbrand_addCartBrand-hotBrand.txt : ")
	getNumOfBrandOfSubmitTXT(wpath)




if __name__ == '__main__':

	#dipNumOfOthersBrand()

	delNotPurchasedBrandInDemo()
	delUserOfNotPurchase()
	delOverBrand()	
	addSaveCartButNotPurchase()

	# addHotBrand()
	#selcOnOnePurchaseUser()
	# calcNumOfOthersBrand(2,P=0.0437,R=0.0136)





'''
#计算F1值
	X=289.;	Y=5337;	Z=3532.
	P=X/Y ; 	R=X/Z
	F1=(2.*P*R)/(P+R)
	print F1
	print "\n"	
'''