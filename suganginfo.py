#!/usr/bin/python3
#-*- coding: utf-8 -*-



import re
import requests
import urllib.request
import time
import random
import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from elasticsearch import Elasticsearch
from urllib.request import urlopen
# 사용 전에 파이썬 패키지 설치 (pip install html_table_parser)
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask import render_template
from flask import request

from selenium import webdriver as web #웹 자동클릭 구현 위한 WEBDRIVER use 

def scrolling(driver):
    mockcha = ['개설연도', '개설학기', '학년', '교과구분', '개설대학', '개설학과', '강좌번호', '교과목명', '학점', '강의', '실습', '담당교수', '강의시간', '강의사간(실제시간)', '강의실', '호실번호', '수강정원', '수강신청', '수강꾸러미신청', '수강꾸러미신청가능여부', '강의방식', '비고']
    html = driver.page_source #해당 사이트 정보 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    data =  soup.find('table', {'class' : 'gridHeaderTableDefault'})

    randtime = random.uniform(0.5,1)
    time.sleep(randtime)

#나머지 것들 가져오기
    tbody = data.find("tbody")
    tbody1 = tbody.find_all("tr")
    allinfolist = []

    for all in tbody1:
        tbody2 = all.find_all("td")
        A = []
        for all2 in tbody2:
            if all2.get_text() != "":
                A.append(all2.get_text())

            else:
                A.append("null")

        A = A[1:] 
        print(len(A))
        for i in range (len(A)):
            A[i] = mockcha[i] + "/" + A[i]

        allinfolist.append(A)

    # print(allinfolist)
    # print(len(allinfolist))

    for i in range (len(allinfolist)):
        AA = allinfolist[i]
        sugangdic[AA[6]] = AA





sugangdic = {}

op = Options()

op.add_argument('--headless')
op.add_argument('window-size=1920x1080')
op.add_argument("disable-gpu")
# op.add_argument("no-sandbox")
# op.add_argument("--disable-dev-shm-usage")
# op.add_argument("headless") # 창 띄우지 않고 실행하기.
op.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Chrome/102.0.5005.61 Firefox/100.0}")
op.add_argument('--start-maximized')

# driver = web.Chrome(executable_path='/home/shin/chromedriver', options = op) # in ubuntu
driver = web.Chrome(options=op)


randtime = random.uniform(0.5,1)
time.sleep(randtime)
driver.get("https://knuin.knu.ac.kr/public/stddm/lectPlnInqr.knu")
randtime = random.uniform(0.5,1)
time.sleep(randtime)

#dropbox click

#driver.find_element_by_xpath('//*[@id="schSbjetCd1"]/option[6]').click() #elements가 아닌 element
# driver.find_element_by_xpath('//*[@id="schSbjetCd2"]/option[16]').click()

selecting = Select(driver.find_element_by_xpath('//*[@id="schSbjetCd1"]'))
selecting.select_by_visible_text("대학")

randtime = random.uniform(0,1)
time.sleep(randtime)

selecting2 = Select(driver.find_element_by_xpath('//*[@id="schSbjetCd2"]'))
selecting2.select_by_visible_text("IT대학")


driver.find_element_by_css_selector('#schSbjetCd3').click()
option = driver.find_element_by_xpath("//*[text()='전자공학부 B']")
#driver.execute_script("arguments[0].scrollintoView();",option)
option.click()

#selecting3 = Select(driver.find_element_by_xpath('//*[@id="schSbjetCd3"]'))
#selecting3.select_by_visible_text("글로벌소프트웨어융합전공");
driver.find_element_by_css_selector('#btnSearch').click()

randtime = random.uniform(1,2) #창이 빠르게 닫기면 크롤링을 못 해오는 경우가 있어 방지하기 위해 sleep 걸음
time.sleep(randtime)

html = driver.page_source #해당 사이트 정보 가져오기
soup = BeautifulSoup(html, 'html.parser')
data =  soup.find('table', {'class' : 'gridHeaderTableDefault'})

#table 목차 가져오기
thead = data.find(class_= 'gridHeaderTableDefault')
thead1 = thead.find_all(class_= 'w2grid_head_sort_div_main w2grid_head_sort_none')
print("목차")
print()
mokcha = []
for all in thead1:
    mokcha.append(all.get_text())
print(mokcha)
print(len(mokcha))

#스크롤 내리기 - 이유 : 스크롤 안 내리면 크롤링을 덜 해옴..
driver.execute_script("window.scrollTo(0,900)")

scrollYto = driver.find_element_by_class_name("w2grid_scrollY")

randtime = random.uniform(1,2)
time.sleep(randtime)

scrolling(driver)


driver.execute_script("arguments[0].scrollBy(0,420)", scrollYto)

scrolling(driver)

driver.execute_script("arguments[0].scrollBy(0,840)", scrollYto)

scrolling(driver)

driver.execute_script("arguments[0].scrollBy(0,1260)", scrollYto)

scrolling(driver)

print(sugangdic)

driver.quit()

# os.system("pause")