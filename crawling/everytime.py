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
from selenium.webdriver.common.by import By

op = Options()
op.add_argument('headless')
op.add_argument('window-size=1920x1080')
op.add_argument("disable-gpu")
# op.add_argument("no-sandbox")
# op.add_argument("--disable-dev-shm-usage")
# op.add_argument("headless") # 창 띄우지 않고 실행하기.
op.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Chrome/102.0.5005.61 Firefox/100.0}")
op.add_argument('--start-maximized')


#driver = web.Chrome(executable_path='/home/shin/chromedriver', options = op) # in ubuntu
driver = web.Chrome(executable_path='/home/shin/chromedriver', options=op)
# driver.set_window_position(0,0) #browser 위치 조정
# driver.maximize_window() #화면 최대화

randtime = random.uniform(0.5,1)
time.sleep(randtime)
driver.get("https://everytime.kr/login")
randtime = random.uniform(0.5,1)
time.sleep(randtime)

driver.find_element_by_name('userid').send_keys('2000sdh')
driver.find_element_by_name('password').send_keys('gm778899')

randtime = random.uniform(0.5,1)
time.sleep(randtime)

driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()

driver.find_element_by_xpath('//*[@id="menu"]/li[3]').click()

driver.find_element_by_xpath('//*[@id="container"]/form/input[1]').send_keys('자바프로그래밍')

randtime = random.uniform(0.5,1)
time.sleep(randtime)

driver.find_element_by_xpath('//*[@id="container"]/form/input[2]').click()


driver.implicitly_wait(10)
data = len(driver.find_element_by_xpath("//*[@id='container']/div").find_elements_by_tag_name('a'))


everytimeDic = {}


for num in range(data):
    realnum = driver.find_element_by_xpath("//*[@id='container']/div").find_elements_by_tag_name('a')[num]
    print("1")
    realnum.click()
    # time.sleep(1)
    html = driver.page_source #해당 사이트 정보 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    driver.implicitly_wait(10)
    data11 = driver.find_element_by_xpath("//*[@id='container']/div[2]")
    driver.implicitly_wait(10)

    lectureinfo_tag = data11.find_element_by_tag_name('h2')
    lectureinfo = lectureinfo_tag.text
    professorinfo_tag1 = data11.find_element_by_tag_name('p')
    professorinfo_tag2 = professorinfo_tag1.find_element_by_tag_name("span")
    professorinfo = professorinfo_tag2.text


    key = lectureinfo + "-" + professorinfo

    driver.implicitly_wait(10)

    ratedata = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]")

    gangpyeong = []
    # ratenum = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]/div[1]").text


    if(driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]/div[1]/span/span[1]").text != "0"):
        detailinfo = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]/div[2]")
        detailinfo1 = detailinfo.find_elements_by_tag_name("p")
        for all in detailinfo1:
            title = all.find_element_by_tag_name("label").text
            whatsin = all.find_element_by_tag_name("span").text
            gangpyeong.append(title + "-" +whatsin)

    else:
        gangpyeong.append("등록된 강의정보가 없습니다.")


    byeoljeom = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]/div[1]/span/span[1]").text
    gangpyeong.append("별점 : " + byeoljeom)

    article = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[2]")
    # article.findElement(By.TAG_NAME, "article").isDisplayed()
    if(driver.find_element_by_xpath("//*[@id='container']/div[4]/div[1]/div[1]").text != "0"):
        article1 = article.find_elements_by_tag_name("article")
        cnt = 1
        for all in article1:
            if(cnt < 6): #강의평 5개 이하로 크롤링해오기
                newall = all.find_elements_by_tag_name("p")
                for all2 in newall:
                    aaaaa = all2.text
                    if(aaaaa != ""):
                        gangpyeong.append(aaaaa)
                    else:
                        continue
                cnt = cnt + 1
            else:
                break

    else:
        article2 = driver.find_element_by_xpath("//*[@id='container']/div[4]/div[2]").text
        gangpyeong.append(article2)

    everytimeDic[key] = gangpyeong
    driver.back()
    # time.sleep(1)
    # driver.execute_script("alert('java 코드 적용');")
    # driver.execute_script("window.history.go(-1)")
    driver.implicitly_wait(10)


print(everytimeDic)

driver.quit()
os.system("pause")