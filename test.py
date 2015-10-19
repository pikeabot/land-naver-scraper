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

	return BeautifulSoup(page, 'html.parser')

def get_properties(gu_name, eng_dong_name, titles, writer):
	for i in range(0, len(titles), 2):

		t= titles[i]
		row = []
		if t.find('td', class_='sale_type2').text==unicode('아파트', 'utf-8'):
			property_type='apt'	
		else:
			property_type='house'

		dong_name = t.find('td', class_='align_l name')

		area = re.findall(r"\d+.\d+", t.find('p', class_='calc_area').text)
		supply_area = area[0]
		try:
			dedicated_area =  area[1]
		except:
			area = re.findall(r" \d+", t.find('p', class_='calc_area').text)
			dedicated_area = area[1]

		price = re.findall(r"\d+,\d+", t.find('td', class_='num align_r').text)

		row.append(gu_name)
		row.append(eng_dong_name)
		row.append(dong_name.find('a').text.encode('utf-8')+',')
		row.append(property_type)
		row.append(supply_area)
		row.append(dedicated_area)
		row.append(price[0])

		writer.writerow(row)

def add_page(gu_name, eng_dong_name, url, writer):
	
	soup = soupify(url)
	
	#titles = soup.find_all('td', class_='sale_type2')
	#titles = soup.find_all('tr', class_='evennum')
	#get_properties(gu_name, eng_dong_name, titles, writer)
	titles = soup.find_all('tr', class_=re.compile("_trow_\d+"))
	#titles=soup.find_all('tr')
	get_properties(gu_name, eng_dong_name, titles, writer)
	'''
	f=open('test.text', 'wb')
	for t in titles:
		#f.write(t.text.encode('utf-8'))
		print t
	f.close()
	'''


f=open('gangnam_gu.csv', 'ab')
writer = csv.writer(f)

header = []
header.append('Gu')
header.append('Dong')
header.append('Dong')
header.append('Property Type')
header.append('Supply Area')
header.append('Dedicated Area')
header.append('Price')

writer.writerow(header)


#siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300'
#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=127.0723995&mapY=37.4915256&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm='
#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2523&ptpNo=&bssYm=&page=35#_content_list_target'
#add_page('Gangnam-gu', 'Gaepo', siteUrl, writer)

for i in range(1,48):
	#siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2932&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2523&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)

	add_page('Gangnam-gu', 'Gaepo', siteUrl, writer)

f.close()
