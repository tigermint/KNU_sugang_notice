#!/usr/bin/python3
#-*- coding: utf-8 -*-



# import re
# import requests
# import urllib.request
import time
import random
# import os

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
# from urllib.request import urlopen
# 사용 전에 파이썬 패키지 설치 (pip install html_table_parser)
from bs4 import BeautifulSoup
# from flask import Flask, jsonify
# from flask import render_template
# from flask import request

from selenium import webdriver as web #웹 자동클릭 구현 위한 WEBDRIVER use 

sugangdic = {}


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
        for i in range (len(A)):
            A[i] = mockcha[i] + "/" + A[i]

        allinfolist.append(A)

    # print(allinfolist)
    # print(len(allinfolist))

    for i in range (len(allinfolist)):
        AA = allinfolist[i]
        sugangdic[AA[6]] = AA


# op = Options()
# op.add_argument('window-size=1920x1080')
# op.add_argument("disable-gpu")
# # op.add_argument("no-sandbox")
# # op.add_argument("--disable-dev-shm-usage")
# op.add_argument("headless") # 창 띄우지 않고 실행하기.
# op.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Chrome/102.0.5005.61 Firefox/100.0}")
# op.add_argument('--start-maximized')

# # driver = web.Chrome(executable_path='/home/shin/chromedriver', options = op) # in ubuntu
# driver = web.Chrome(options=op)


# randtime = random.uniform(0,1)
# time.sleep(randtime)
# driver.get("https://knuin.knu.ac.kr/public/stddm/lectPlnInqr.knu")
# randtime = random.uniform(0,1)
# time.sleep(randtime)


def searching(lecturename):

    op = Options()
    op.add_argument('window-size=1920x1080')
    op.add_argument("disable-gpu")
    # op.add_argument("no-sandbox")
    # op.add_argument("--disable-dev-shm-usage")
    op.add_argument("headless") # 창 띄우지 않고 실행하기.
    op.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Chrome/102.0.5005.61 Firefox/100.0}")
    op.add_argument('--start-maximized')

    # driver = web.Chrome(executable_path='/home/shin/chromedriver', options = op) # in ubuntu
    driver = web.Chrome(options=op)


    randtime = random.uniform(0,1)
    time.sleep(randtime)
    driver.get("https://knuin.knu.ac.kr/public/stddm/lectPlnInqr.knu")
    randtime = random.uniform(0,1)
    time.sleep(randtime)

    selecting = Select(driver.find_element_by_xpath('//*[@id="schCode"]'))
    selecting.select_by_visible_text("교과목명")

    driver.find_element_by_id("schCodeContents").send_keys("{0}".format(lecturename))
    #html에서 입력받은 값을 send_keys할 것임


    driver.find_element_by_css_selector('#btnSearch').click()
    driver.implicitly_wait(10)

    html = driver.page_source #해당 사이트 정보 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    data =  soup.find('table', {'class' : 'gridHeaderTableDefault'})
    randtime = random.uniform(1.5,2.5) #창이 빠르게 닫기면 크롤링을 못 해오는 경우가 있어 방지하기 위해 sleep 걸음
    time.sleep(randtime)
    #가져올 값들이 몇 개 존재하는지 알아보기
    what = driver.find_element_by_xpath("//*[@id='wq_uuid_93_lblCount']").text
    numwhat = int(what)
    print(numwhat)

    #스크롤 내리기 - 이유 : 스크롤 안 내리면 크롤링을 덜 해옴..
    driver.execute_script("window.scrollTo(0,900)")

    scrollYto = driver.find_element_by_class_name("w2grid_scrollY")

    scrolling(driver) #한번 크롤링 실행

    scrollnum = 0
    while(len(sugangdic) <= numwhat): #딕셔너리가 가져와야 할 값보다 작거나같으면(같은 경우를 넣어준 이유는 처음에 가끔 데이터를 이상하게 받아와서임)
        driver.execute_script("arguments[0].scrollBy(0,{0})".format(scrollnum + 420), scrollYto)
        #페이지가 스크롤 내릴 때 마다 동적으로 데이터를 가져오므로, 수동으로 일정 부분 늘려서 데이터 가져온다.
        scrolling(driver)
        if(len(sugangdic) > numwhat):
            break

    #페이지가 동적으로 움직이기 때문에 일어나는 오류 
    #맨 마지막임을 알리기 위해 html에서 tag는 같지만 안의 값을 모두 ""로
    #설정해놓아 항상 마지막에 'null'이 출력되게 된다.
    #따라서 key값이 "강좌번호/null" 과 일치하면, 딕셔너리에서 삭제할 것이다.

    if "강좌번호/null" in sugangdic:
        del sugangdic["강좌번호/null"]


    print(sugangdic)

    driver.quit()


searching("자료구조")
# os.system("pause")