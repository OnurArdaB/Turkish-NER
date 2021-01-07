import requests
from bs4 import BeautifulSoup as bs
import string
#This page iterates until page 35,page number can be given as query parameter
URL = "https://nameberry.com/baby-names/164/English-Names"
result=set()
for i in range(1,35):
    r = requests.get(URL,params={
        'page':i
    })

    if(r.status_code==200):
        soup = bs(r.text,'html.parser')
        a = soup.findAll("a",{'class':"name_link"})
        for a_ in a:
            if(a_.text not in result):
                result.add(a_.text)
for letter in string.ascii_uppercase:
    URL = "https://nameberry.com/search/girls_names/"+letter
    for i in range(1,30):
        print(letter , i)
        r = requests.get(URL,{
            'page':i
        })
        if(r.status_code==200):
            soup = bs(r.text,'html.parser')
            a = soup.findAll("a",{'class':"name_link"})
            if(len(a)==0):
                break
            for a_ in a:
                if(a_.text not in result):
                    result.add(a_.text)
for letter in string.ascii_uppercase:
    URL = "https://nameberry.com/search/boys_names/"+letter
    for i in range(1,30):
        print(letter , i)
        r = requests.get(URL,{
            'page':1
        })
        if(r.status_code==200):
            soup = bs(r.text,'html.parser')
            a = soup.findAll("a",{'class':"name_link"})
            if(len(a)==0):
                break
            for a_ in a:
                if(a_.text not in result):
                    result.add(a_.text)
for letter in string.ascii_uppercase:
    URL = "https://nameberry.com/search/unisex_names/"+letter
    for i in range(1,30):
        print(letter , i)
        r = requests.get(URL,{
            'page':1
        })
        if(r.status_code==200):
            soup = bs(r.text,'html.parser')
            a = soup.findAll("a",{'class':"name_link"})
            if(len(a)==0):
                break
            for a_ in a:
                if(a_.text not in result):
                    result.add(a_.text)
for letter in string.ascii_uppercase:
    URL = "https://nameberry.com/search/unique_names_starting_with/"+letter
    for i in range(1,30):
        print(letter , i)
        r = requests.get(URL,{
            'page':1
        })
        if(r.status_code==200):
            soup = bs(r.text,'html.parser')
            a = soup.findAll("a",{'class':"name_link"})
            if(len(a)==0):
                break
            for a_ in a:
                if(a_.text not in result):
                    result.add(a_.text)
               
with open("PERSON.txt","a+",encoding="utf-8") as output:
    sortedNames = sorted(result)
    for name in sortedNames:
        output.write(name+"\n")