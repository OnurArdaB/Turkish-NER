import requests
from bs4 import BeautifulSoup as bs
URL = 'https://www.turkcebilgi.com/meslekler_listesi'

res = requests.get(URL)
if(res.status_code==200):
    soup = bs(res.text,'html.parser')
    div = soup.findAll('div',{"class":"content-body"})[0]
    textList = div.findAll("a")
    f = open("JOBS.txt",'a+',encoding="utf-8")
    for text in textList:
        if(len(text.text.split(" "))==1):
            final = text.text.lower()
        f.write(final+'\n')