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
			try:
				area = re.findall(r" \d+", t.find('p', class_='calc_area').text)
				supply_area=area[0]
			except:
				supply_area='NA'
		try:
			dedicated_area =  area[1]
		except:
			area = re.findall(r" \d+", t.find('p', class_='calc_area').text)
			if len(area)>1:
				dedicated_area = area[1]
			else:
				dedicated_area='NA'
		try:
			price = re.findall(r"\d+,\d+", t.find('td', class_='num align_r').text)[0]
		except:
			price = re.findall(r"\d+", t.find('td', class_='num align_r').text)[0]

		row.append(gu_name)
		row.append(eng_dong_name)
		row.append(hangul_dong_name)
		#row.append(commercial_name.find('a').text.encode('utf-8')+',')
		row.append(property_type)
		row.append(supply_area)
		row.append(dedicated_area)
		row.append(price)

		writer.writerow(row)

def add_page(gu_name, eng_dong_name, property_type, url, writer):
	
	soup = soupify(url)

	titles = soup.find_all('tr', class_=re.compile("_trow_\d+"))
	hangul_dong_name=soup.find('h2', id='depth4Content_Title').text.encode('utf-8')
	hangul_dong_name=re.findall(r"\[(.*?)\]", hangul_dong_name)[0]
	#print hangul_dong_name[0].decode('utf-8')
	#print hangul_dong_name.decode('cp949')
	get_properties(gu_name, eng_dong_name, hangul_dong_name, property_type, titles, writer)

def create_file(gu, dong, apt_siteUrl, apt_page_num, house_siteUrl, house_page_num):
	#gu='Gangnam'
	#dong='Cheongdam'
	filename='{0}_{1}.csv'.format(gu, dong)

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

	for i in range(1,int(apt_page_num)):
		if apt_page_num==2:
			add_page(gu, dong, 'apt', apt_siteUrl, writer)
		else:
			add_page(gu, dong, 'apt', apt_siteUrl.format(i), writer)

	for j in range(1,int(house_page_num)):
		#gangnam house
		if house_page_num==2:
			add_page(gu, dong, 'house', house_siteUrl, writer)
		else:
			add_page(gu, dong, 'house', house_siteUrl.format(j), writer)
	f.close()

if __name__ == '__main__':
	
	f=open('pocheon_info.csv', 'rb')
	reader = csv.reader(f)
	i=0
	for r in reader:
		#if i >= 5:
		create_file(r[0], r[1], r[2], r[3], r[4], r[5])
		#i+=1
	'''
	apt_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=A1&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1150010300&articleOrderCode=-3&siteOrderCode=&cpId=&mapX=&mapY=&mapLevel=&minPrc=&maxPrc=&minWrrnt=&maxWrrnt=&minLease=&maxLease=&minSpc=&maxSpc=&subDist=&mviDate=&hsehCnt=&rltrId=&mnex=&mHscpNo=&mPtpRange=&mnexOrder=&location=2528&ptpNo=&bssYm=&page={0}#_content_list_target'
	house_siteUrl='http://land.naver.com/article/articleList.nhn?rletTypeCd=C03&tradeTypeCd=A1&rletNo=&cortarNo=1150010300&hscpTypeCd=C02%3AC03%3AC04%3AD05&mapX=&mapY=&mapLevel=&page={0}&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=-3&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2866&bbs_tp_cd=&sort=&siteOrderCode=#_content_list_target'
	create_file('Gangseo', 'Hwagok', apt_siteUrl, '28', house_siteUrl, '44')	
	'''