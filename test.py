# -*- coding: utf-8 -*- 
import os
import datetime
import re
import sys
import urllib2
import csv
import codecs

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
		
		row.append('Gaepo')
		row.append(price_list[i])
		row.append(area_list[i])
		writer.writerow(row)

def test():
	url='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=127.0723995&mapY=37.4915256&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm='
	soup = soupify(url)
	row = []
	#titles = soup.find_all('td', class_='sale_type2')
	titles = soup.find_all('tr', class_='evennum')
	t= titles[2]

	if t.find('td', class_='sale_type2').text==unicode('아파트', 'utf-8'):
		property_type='apt'	
	else:
		property_type='house'
	#print property_type
	row.append(property_type)
	dong_name = t.find('td', class_='align_l name')
	#print dong_name.find('a').text
	row.append(dong_name.find('a').text.encode('utf-8'))
	area = re.findall(r"\d+.\d+", t.find('p', class_='calc_area').text)
	supply_area = area[0]
	dedicated_area =  area[1]
	#print supply_area
	#print dedicated_area
	row.append(supply_area)
	row.append(dedicated_area)
	#print titles[0].find('p', class_='calc_area').text
	#print titles[0].find('td', class_='num align_r').text
	price = re.findall(r"\d+,\d+", t.find('td', class_='num align_r').text)
	#print price[0]
	row.append(price[0])
	#for t in titles:
	#	print t.text
	return row

f=open('gangnam_gu.csv', 'ab')
writer = csv.writer(f)

header = []
header.append('Gu')
header.append('Dong')
header.append('Property Type')
header.append('Supply Area')
header.append('Dedicated Area')
header.append('Price')

writer.writerow(header)

writer.writerow(test())

'''
siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300'
add_page(siteUrl, writer)
for i in range(1,50):
	siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2932&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	add_page(siteUrl, writer)
'''
f.close()
