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

def get_properties(gu_name, eng_dong_name, hangul_dong_name, property_type, titles, writer):
	for i in range(0, len(titles), 2):

		t= titles[i]
		row = []

		#commercial_name = t.find('td', class_='align_l name')
		area = re.findall(r"\d+.\d+", t.find('p', class_='calc_area').text)
		try:
			supply_area = area[0]
		except:
			area = re.findall(r" \d+", t.find('p', class_='calc_area').text)
			supply_area=area[0]
		try:
			dedicated_area =  area[1]
		except:
			area = re.findall(r" \d+", t.find('p', class_='calc_area').text)
			if len(area)>1:
				dedicated_area = area[1]
			else:
				dedicated_area='NA'

		price = re.findall(r"\d+,\d+", t.find('td', class_='num align_r').text)

		row.append(gu_name)
		row.append(eng_dong_name)
		row.append(hangul_dong_name)
		#row.append(commercial_name.find('a').text.encode('utf-8')+',')
		row.append(property_type)
		row.append(supply_area)
		row.append(dedicated_area)
		row.append(price[0])

		writer.writerow(row)

def add_page(gu_name, eng_dong_name, property_type, url, writer):
	
	soup = soupify(url)

	titles = soup.find_all('tr', class_=re.compile("_trow_\d+"))
	hangul_dong_name=soup.find('h2', id='depth4Content_Title').text.encode('utf-8')
	hangul_dong_name=re.findall(r"\[(.*?)\]", hangul_dong_name)[0]
	#print hangul_dong_name[0].decode('utf-8')
	#print hangul_dong_name.decode('cp949')
	get_properties(gu_name, eng_dong_name, hangul_dong_name, property_type, titles, writer)


gu='Gangnam'
dong='Cheongdam'
filename='{0}_{1}_v2.csv'.format(gu, dong)

f=open(filename, 'ab')
writer = csv.writer(f)

header = []
header.append('Gu')
header.append('Dong')
header.append('Dong')
#header.append('Building Name')
header.append('Property Type')
header.append('Supply Area')
header.append('Dedicated Area')
header.append('Price')

writer.writerow(header)

for i in range(1,2):

	#siteUrl = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2932&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#gaepo
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010300&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2523&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)

	#Nonhyun
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010800&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0313752&mapY=37.5135831&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Daechi-dong
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010600&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0654631&mapY=37.4991105&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Dogok
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011800&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0450504&mapY=37.4881434&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Samseong
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010500&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0553873&mapY=37.5147918&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010500&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Segok
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011100&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.1046001&mapY=37.4643598&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011100&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Suseo
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011500&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.1048862&mapY=37.4888562&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011500&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Sinsa
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010700&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0228994&mapY=37.5241419&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010700&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Apgujeong
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011000&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0236001&mapY=37.5291003&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011000&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Yeoksam
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010100&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0389498&mapY=37.4997761&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010100&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2332&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Irwon
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011400&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0816381&mapY=37.4874854&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011400&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2491&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#Jagok
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011200&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.1010002&mapY=37.4765999&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	#apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168011200&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm='
	#Cheongdam
	#siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010400&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=127.0523496&mapY=37.525492&mapLevel=10&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1168010400&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'.format(i)
	add_page(gu, dong, 'apt', apt_siteUrl, writer)

for j in range(1,3):
	#gangnam house
	house_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=C03&tradeTypeCd=A1&rletNo=&cortarNo=1168010400&hscpTypeCd=C02%3AC03%3AC04%3AD05&mapX=&mapY=&mapLevel=&page={0}&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=-3&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2521&bbs_tp_cd=&sort=&siteOrderCode=#_content_list_target'.format(j)
	add_page(gu, dong, 'house', house_siteUrl, writer)
f.close()
