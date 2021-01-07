from bs4 import BeautifulSoup as bs
import requests

#we will use requests to get necessary html pages and Beautiful Soup in order to parse the information inside the page

URL = "https://www.bbc.co.uk/academy/tr/articles/art20150916134647005"
#This page contains country names and their capital names.

r = requests.get(URL)

if(r.status_code == 200):

    #Obtained html page is inserted inside the bs4 html parser in order to parse the necessary fields easier
    soup = bs(r.text,"html.parser")

    #The page contains a table and rest of the information is not necessary for us
    rows = soup.findAll("tr")
    
    headings = []

    strongs = rows[:1][0].findAll("strong")

    for strong in strongs:
        headings.append(strong.text)
    
    column_3 = []
    column_4 = []

    for data in rows[1:]:
        p_ = data.findAll("p")
        column_3.append(p_[2].text)
        column_4.append(p_[3].text)

    print(headings[2],column_3[0],column_3[-1],len(column_3))  
    print(headings[3],column_4[0],column_4[-1],len(column_4))  

    if(len(column_3)==len(column_4)):
        print("Everything seems to be fine...")
        file = open("LOCATION.txt","a") #opening file in append mode
        for row in column_3:
            file.write(row+'\n')
        

else:   
    print("PAGE CAN NOT BE RETRIEVED...")