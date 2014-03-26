# -*- coding: UTF-8 -*-
import numpy as np
from numpy import *
import ali323
'''
ѡ��û�й�����Ϊ���û��洢ΪnotOnePurchaseUser.npy
'''
def selcOnOnePurchaseUser():
	allMt = load("data.npy")
	allUser = set(allMt[:,0])
	print len(set(allMt[:,0]))

	purchaseMt = ali323.getWithParameter(allMt,0 ,0 ,(1,),0 ,0)
	purcheseUser = set(purchaseMt[:,0])
	print len(set(purchaseMt[:,0]))
	notPurchaseUser = allUser.difference(purcheseUser)  #ȡ��allUser����purcheseUser�еĲ���
	print len(notPurchaseUser)
	print notPurchaseUser
	np.save("notOnePurchaseUser.npy", list(notPurchaseUser))
'''

��ȡ�û��ϴ���Demo.txt �ļ��е��Ƽ���Brand������
���ͬʱ�������¸��³ɽ����ܼ�¼.
rpath ΪDemo.txt��·��
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
#�����������ύ��Brand����
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

#ɾ������BrandID�н���������ˣ�����û�б��ղء����ﳵ�͹����BrandID
def delNotPurchasedBrandInDemo() :
	numOfNotPurchased = 0
	flagDispComma = 0  #�����Ƿ���ʾ��һ��brandǰ��Ķ���
	notPurchasedBrand = np.load("notPurchasedBrand.npy")
	#print("The number of notPurchasedBrand:%d " %(len(notPurchasedBrand)))
	rpath = "demo_322.txt"
	# rpath = "demo-jyc322.txt"
	wpath = "demo_322_del_brand.txt"
	fr = open(rpath,"r")
	fw = open(wpath,"w")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2άList
		listBrand = listUserBrand[1].split(",")  #�����Ʒ��List
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
#ɾ��û�й����¼���߲����ٹ�����û�����������
def delUserOfNotPurchase():
	numOfNotPurchasedUser = 0
	notPurchasedUser = np.load("noPurchaseGuy.npy")
	print("The number of notPurchasedBrand:%d " %(len(notPurchasedUser)))
	rpath = "demo_322_del_brand.txt"
	wpath = "demo_322_del_brand_user.txt"
	fr = open(rpath,"rb")
	fw = open(wpath,"wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2άList [userID,brandID]
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
ɾ�����û��Ĺ�����Ƽ���Ŀ��
1��ɾ�������¹����������1��user��
2�������û�������µĹ�����������Ƽ���������µĹ������ΪN��
	N < 0.2     : ɾ�����û���
	0.2 < N < 1 : modifyTimes*3(ȥβ) 
	1 < N < 3   : modifyTimes*2 
	3 < N < 5   : ȡmodifyTimes=5
	N > 5       : modifyTimes=10  
'''
def  delOverBrand():
	flagDispComma = 0  #�����Ƿ���ʾ��һ��brandǰ��Ķ���
	averagePurchasedTimes = np.load("userAveragePurchaseTime.npy")
	rpath = "demo_322_del_brand_user.txt"
	wpath = "demo_322_del_brand_user_overbrand.txt"
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")

	for line in fr :
		listUserBrand = line.strip().split("\t")  #2άList[user, brand]
		listBrand = listUserBrand[1].split(",")  #�����Ʒ��List
		for user, times in averagePurchasedTimes :
			if user == int(listUserBrand[0]) :   # ѡ�������û�user�ھ����еĶ�Ӧ�Ĺ������times
				#if times < 1:  do noting
				if times > 0.2:
					if 0.2 < times <1 : modifyTimes = times*3#int(times * 2)
					elif 1 <= times < 3:	modifyTimes = times*2
					elif 3 <= times <=5 : modifyTimes = 5
					elif 5 < times:	modifyTimes=10

					#��ÿһ�е�ǰtimes��brandд���ļ�����д��listBrand[:int(times)]
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
�û��ղع��ﳵ����û�������,������ӵ�������档
ע�⣺���жϽ��������û�������Ʒ
'''	
def addSaveCartButNotPurchase() :
	flagDispComma = 0  #�����Ƿ���ʾ��һ��brandǰ��Ķ���
	flagDispEnter = 0  #�����Ƿ���ʾ��һ��brandǰ��Ķ���
	userIDAll= [] #���rpath�������û���ID
	userIDTemp=0
	saveCartButNotPurchase = np.load("saveCartButNotPurchase.npy")
	notPurchasedUser = np.load("notOnePurchaseUser.npy")  #���ڽ�û�й�����Ϊ�����ǹ��ﳵ����Ʒ��userɾ��
	#print saveCartButNotPurchase
	saveCartButNotPurchase = sorted(saveCartButNotPurchase, key=lambda jj : jj[0], reverse=True) #��������
	#saveCartButNotPurchase = mat(saveCartButNotPurchase)
	#print saveCartButNotPurchase
	rpath = "demo_322_del_brand_user_overbrand.txt"
	wpath = "demo_322_del_brand_user_overbrand_addCartBrand.txt"
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2άList[user, brand]
		userIDAll.append(int(listUserBrand[0]))
		listBrand = listUserBrand[1].split(",")  #�����Ʒ��List
		for user, brand in saveCartButNotPurchase :
			if user == int(listUserBrand[0]) :   # ѡ�������û�user�ھ����еĶ�Ӧ�Ĺ������times
				if str(brand) not in listBrand : #�������е�brandû�ڸ���ʱ����ӽ���
					listBrand.append(brand)
		#д�����ļ���user brand newBrand
		fw.write(listUserBrand[0] + "\t")
		for brandID in listBrand :
			if flagDispComma == 0 : 	
				fw.write(brandID)	
				flagDispComma = 1
			else :			
				fw.write(","+str(brandID))
		fw.write("\n")
		flagDispComma = 0
	#��� �û���Դ�ļ���û�е��û������빺�ﳵ������û�й����
	# print notPurchasedUser
	for user,brand in saveCartButNotPurchase :
		if user not in userIDAll :
			if int(user) not in notPurchasedUser :  #ֻ����й�����Ϊ���û�
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
�������brand���������б��Ƽ����ύ�������û��������ÿһ���ˡ�
'''	
def addHotBrand() :
	flagDispComma = 0
	rpath = "demo_322_del_brand_user_overbrand_addCartBrand.txt"
	wpath = "demo_322_del_brand_user_overbrand_addCartBrand-hotBrand.txt"
	mtHotBrand = np.load("hotPurchasedBrand.npy")
	fr = open(rpath, "rb")
	fw = open(wpath, "wb")
	for line in fr :
		listUserBrand = line.strip().split("\t")  #2άList[user, brand]
		listBrand = listUserBrand[1].split(",")  #�����Ʒ��List
		for brandID in mtHotBrand :
			if str(brandID) not in listBrand : #�������brandIDû���ڸ��е��û���brand�У������
				listBrand.append(str(brandID)) 
		#�����ɺ�д���ļ�		

		#��ÿһ�е�ǰtimes��brandд���ļ�����д��listBrand[:int(times)]
		fw.write(listUserBrand[0] + "\t")
		for brandID in listBrand :
			if flagDispComma == 0 : 	 #д���ŵı�־λ
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
#����F1ֵ
	X=289.;	Y=5337;	Z=3532.
	P=X/Y ; 	R=X/Z
	F1=(2.*P*R)/(P+R)
	print F1
	print "\n"	
'''