# -*- coding: UTF-8 -*-
import urllib2
import re

def testSpider():
	rank = 0
	url='http://www.baidu.com/s?wd=cloga'
	content=urllib2.urlopen(url).read()

	urls_pat=re.compile(r'<span class="g">(.*?)</span>')
	siteUrls=re.findall(urls_pat,content)


	strip_tag_pat=re.compile(r'<.*?>')
	file=open('results000.csv','w')

	for i in siteUrls:
	    i0=re.sub(strip_tag_pat,'',i)
	    i0=i0.strip()
	    i1=i0.split(' ')
	    date=i1[-1]
	    siteUrl=''.join(i1[:-1])
	    rank+=1
	    file.write(date+','+siteUrl+','+str(rank)+'\n')
	file.close()

def rankSpider():
	# url='http://102.alibaba.com/competition/addDiscovery/totalRank.htm'
	url = 'http://wszw.hzs.mofcom.gov.cn/fecp/fem/corp/fem_cert_stat_view_list.jsp'
	content=urllib2.urlopen(url).read()
	print content

	urls_pat=re.compile(r'<tbody class="intr-tbody">(.*?)</span>')
	siteUrls=re.findall(urls_pat,content)
	print siteUrls
	

if __name__ == '__main__':
	rankSpider()