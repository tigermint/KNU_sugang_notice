#!/usr/bin/python3
#-*- coding: utf-8 -*-



import re
import requests
import urllib.request
import time
import random
import os


from selenium.webdriver.support.select import Select
from elasticsearch import Elasticsearch
from urllib.request import urlopen
# 사용 전에 파이썬 패키지 설치 (pip install html_table_parser)
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask import render_template
from flask import request

from selenium import webdriver as web #웹 자동클릭 구현 위한 WEBDRIVER use 

op = web.ChromeOptions()
op.add_argument('headless')
op.add_argument('window-size=1920x1080')
op.add_argument("disable-gpu")
# op.add_argument("no-sandbox")
# op.add_argument("--disable-dev-shm-usage")
# op.add_argument("headless") # 창 띄우지 않고 실행하기.
op.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Chrome/102.0.5005.61 Firefox/100.0}")


#driver = web.Chrome(executable_path='/home/shin/chromedriver', options = op) # in ubuntu
driver = web.Chrome()
driver.set_window_position(0,0) #browser 위치 조정
driver.maximize_window() #화면 최대화

randtime = random.uniform(1,2)
time.sleep(randtime)
driver.get("https://everytime.kr/login")
randtime = random.uniform(1,2)
time.sleep(randtime)

driver.find_element_by_name('userid').send_keys('2000sdh')
driver.find_element_by_name('password').send_keys('gm778899')

randtime = random.uniform(1,2)
time.sleep(randtime)

driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

driver.find_element_by_xpath('//*[@id="menu"]/li[3]').click()

driver.find_element_by_xpath('//*[@id="container"]/form/input[1]').send_keys('자바프로그래밍')

driver.find_element_by_xpath('//*[@id="container"]/form/input[2]').click()

html = driver.page_source #해당 사이트 정보 가져오기
soup = BeautifulSoup(html, 'html.parser')


data =  soup.find('div' , {'class' : 'lectures'})
randtime = random.uniform(1,2)
time.sleep(randtime)
print(data)

os.system("pause")