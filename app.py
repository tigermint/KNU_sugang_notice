# !/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests
import schedule
import time

import crawling.suganginfoVer2 as sugang

from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask import render_template
from flask import request

# from crawling import everytime

def startsugang(lecturename):
    sugang


schedule.every(10).seconds.do(startsugang)

while True:
    schedule.run_pending()
    time.sleep(1)




