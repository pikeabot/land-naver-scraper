import os
import datetime
import re
import sys
import urllib2
import csv

from os import listdir
from os.path import isfile, join
from datetime import date
from bs4 import BeautifulSoup
#from scraperutil import soupify


def soupify(url):
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()

	return BeautifulSoup(page)

def get_price_list(prices):
	price_list=[]
	for p in prices:
		r = re.findall(r"\d+,\d+", p.text)
		if r:
			#f.write(r[0] + '\n')
			price_list.append(r[0])
	return price_list

def get_area_list(areas):
	area_list=[]
	for a in areas:
		r = re.findall(r"\d+.\d+", a.text)
		#f.write(r[0] + '\n')
		area_list.append(r[0])
	return area_list

def add_page(url, writer):
	soup = soupify(url)

	titles = soup.find_all('strong')
	area = soup.find_all("p", "calc_area")

	price_list = get_price_list(titles)
	area_list = get_area_list(area)

	for i in range(0, len(price_list)):
		row=[]
		row.append('강남구')
		row.append('Gaepo')
		row.append(price_list[i])
		row.append(area_list[i])
		writer.writerow(row)

f=open('gangnam_gu.csv', 'ab')
writer = csv.writer(f)

header = []
header.append('Gu')
header.append('Dong')
header.append('Price')
header.append('Area')
writer.writerow(header)


siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300'
add_page(siteUrl, writer)
for i in range(1,50):
	siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2932&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	add_page(siteUrl, writer)
f.close()
