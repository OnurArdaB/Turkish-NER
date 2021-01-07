from bs4 import BeautifulSoup as bs
import requests

URL = "https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27nin_il%C3%A7eleri"
response = requests.get(URL)
districts_=[]
if(response.status_code == 200):
    soup = bs(response.text,"html.parser")
    table = soup.findAll("table",{"class":"wikitable sortable"})
    tableBody = table[0].findAll("tbody")
    trS = tableBody[0].findAll("tr")
    for tr in trS[1:]: #first line is header
        tdS = tr.findAll("td")
        districts_.append(tdS[0].text)

with open("LOCATION.txt","a",encoding="utf-8") as file:
    file.write("\n######################\n")
    for district in districts_:
        file.write(district)
    