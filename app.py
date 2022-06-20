from flask import Flask, render_template, request
from Crawler import suganginfoVer2 as cr
from Crawler import everytime as et
import asyncio

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def result():
    flag = False
    eflag = False
    subject = request.form.get('subject')
    code = request.form.get('code')
    prof = request.form.get('professor')
    evn = subject+'-'+prof
    dict = cr.searching(subject)
    print(dict)
    etdi = et.searching(subject)
    print(etdi)
    if not code in dict:
        flag = True
    if not evn in etdi:
        eflag = True
        
    return render_template("result.html",flag = flag, eflag = eflag, code = code, 
    prof = dict[code][11], subject = subject, credit = dict[code][8], croom = dict[code][14], 
    crnum = dict[code][15], personnel = dict[code][16], student = dict[code][17], time = dict[code][13],
    report = etdi[evn][0], team = etdi[evn][1], score = etdi[evn][5], ev1 = etdi[evn][7], ev2 = etdi[evn][9], ev3 = etdi[evn][11])

if __name__ == '__main__' : 
    app.run(debug=True)

