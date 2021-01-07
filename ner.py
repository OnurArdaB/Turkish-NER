# -*- coding: utf-8 -*-
import re
import os 
import sys
from Lexicons import PERSON
from Lexicons import second_names

#These are names used before or after of a special name(Organization,Location,Person,Date) and due to this reason they are not appended too the lexicon files.
#PERSON is a dictionary for faster checking time and performance.
MONTH_LIST = second_names.MONTH_LIST
QUERY_LOCATION_ENDS = second_names.QUERY_LOCATION_ENDS
QUERY_ORGANIZATION_ENDS = second_names.QUERY_ORGANIZATION_ENDS
TITLES = second_names.TITLES
DIRECTIONS = second_names.DIRECTIONS
JOBS = second_names.JOBS
PERSON_NAME = PERSON.name
PERSON_SURNAME = PERSON.surname

listOfDateRegex = []
for i in ['/','-','\.','\|',':']:
    listOfDateRegex.append(fr'((?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0,1])){i}(?:(?:0[1-9])|(?:1[0,1,2])){i}(?:\d+\d+\d+\d+))')
    listOfDateRegex.append(fr'((?:(?:0[1-9])|(?:1[0,1,2])){i}(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0,1])){i}(?:\d+\d+\d+\d+))')
    listOfDateRegex.append(fr'((?:\d+\d+\d+\d+){i}(?:(?:0[1-9])|(?:1[0,1,2])){i}(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0,1])))')
    listOfDateRegex.append(fr'((?:\d+\d+\d+\d+){i}(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0,1])){i}(?:(?:0[1-9])|(?:1[0,1,2])))')
with open("./Lexicons/LOCATION.txt",encoding="utf-8") as LOCATION_FILE:
    LOCATIONS  =  LOCATION_FILE.readlines()
    for index in range(len(LOCATIONS)):
        if(LOCATIONS[index].find("\n")!=-1):
            LOCATIONS[index] = LOCATIONS[index].split("\n")[0]

with open("./Lexicons/ORGANIZATION.txt",encoding="utf-8") as ORGANIZATION_FILE:
    ORGANIZATION  =  ORGANIZATION_FILE.readlines()
    for index in range(len(ORGANIZATION)):
        if(ORGANIZATION[index].find("\n")!=-1):
            ORGANIZATION[index] = ORGANIZATION[index].split("\n")[0]

with open(f"./{sys.argv[1]}",encoding="utf-8") as SAMPLE_FILE:
    SAMPLE_LINES = SAMPLE_FILE.readlines()

for LINE_NUMBER,SAMPLE_TEXT in enumerate(SAMPLE_LINES):
    LINE_NUMBER+=1
    LOCATIONS_FOUND = list()
    DATE_FOUND = list()
    ORGANIZATION_FOUND = list()
    PERSON_FOUND = list()

    #LOCATIONS
    #RULE-1 Country and Continent Detection via Lexicon
    for uppercaseWord in re.finditer(r'((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*[ -]?)+(?:[\.,]*))',SAMPLE_TEXT):
        uppercaseWord = SAMPLE_TEXT[uppercaseWord.start():uppercaseWord.end()]
        if uppercaseWord in LOCATIONS:
            if(uppercaseWord not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+uppercaseWord)
    
    #Slightly modified existing rule.
    if 'ilçesi' in SAMPLE_TEXT:
        temp=re.findall(r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?=\s+ilçesi\w+)',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
                if(element not in LOCATIONS_FOUND):
                    LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #Rule 2-Multiword containing Country ,Region ,Mountain ,Sea and etc in the end of the string.
    for END in QUERY_LOCATION_ENDS:
        if END in SAMPLE_TEXT:
            QUERY = '((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* ){1,})'+'{params}+)'.format(params=END)
            temp = re.findall(QUERY,SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in LOCATIONS_FOUND):
                    LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #Slightly modified existing rule.
    if 'istan' in SAMPLE_TEXT:
        temp = re.findall(r'((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]* ){0,})[A-ZÇĞİÖŞÜ][a-zçğıöşü]*istan+)',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #Rule 3-Latitude Longitude -+90 For Latitude and -+180 For Longitude
    QUERY_LAT_LON = r'((?:(?:[+,-]{1}[0-8][0-9]\.{1}[0-9]*)|(?:[+,-]{1}90\.{1}[0-9]{5}))\s?(?:(?:[+,-]{1}[1]?[0-7][0-9]\.{1}[0-9]*)|(?:[+,-]?[0-9][0-9]\.{1}[0-9]*)|(?:[+,-]?180\.[0-9]*)))'
    temp  = re.findall(QUERY_LAT_LON,SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
        if(element not in LOCATIONS_FOUND):
            LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #Rule 4-DakiTaki/DekiTeki
    QUERY_DA_DE_TA_TE_Kİ = r'((?:(?:[A-ZÇİÖŞÜ][a-zçıöşüA-ZÇİĞÖŞÜ]*\s?){1,})(?=\'\s?[d,t][a,e]ki))'
    temp  = re.findall(QUERY_DA_DE_TA_TE_Kİ,SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
        if(element not in LOCATIONS_FOUND):
            LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)
    
    #Slightly modified existing rule.
    for direction in DIRECTIONS:
        QUERY_DA_DE_TA_TE_Kİ = fr'({direction} (?:(?:[A-ZÇİÖŞÜ][a-zçıöşüA-ZÇİĞÖŞÜ]*\s?)'+'{1,}))'
        temp  = re.findall(QUERY_DA_DE_TA_TE_Kİ,SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #Rule 5-Güzergahı .... .... 'ya doğru
    QUERY_TOWARDS = r'[g,G]üzergahı ((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*){1,}))[ ,]?\'[ ,]?y?a?e? doğru'
    temp  = re.findall(QUERY_TOWARDS,SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)
    
    #Rule 6-.... .... semalarında
    QUERY_TOWARDS = r'((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* ){1,}))semalarında'
    temp  = re.findall(QUERY_TOWARDS,SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)
    
    #Rule 7-Starts with uppercase word followed by lower case word and after all upper cases  'ya gidicek is location.
    if 'gidecek.' in SAMPLE_TEXT:
        temp = re.findall(r'(?:\w+){1} (?:[a-zçğıöşü]){1,} ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*[\s]?){1,})(?:[\s]?\'y[a,e]{1}) gidecek\.',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)
    #Rule 8-Dün akşam saatlerinde ...'dan yola çıkan [herhangi bir araç tipi].
    if ' yola çıkan otobüs' or ' yola çıkan kamyon' or ' yola çıkan araba' or ' yola çıkan tren' or ' yola çıkan araç' in SAMPLE_TEXT:
        temp = re.findall(r'(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*) (?:[a-zçğıöşü]*) ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*[\s]?){1,})(?:\'[d,t]{1}[a,e]{1}n) yola çıkan (?:otobüs|kamyon|araba|araç)',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in LOCATIONS_FOUND):
                LOCATIONS_FOUND.append(f"Line {LINE_NUMBER}: LOCATION "+element)

    #ORGANIZATION
    #Rule 9-Procter & Gamble or Procter Procter Procter ... & Gamble Gamble ...
    QUERY_AMPERSAN= r'((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* )+\& (?:\w+[ ,]?)+)'
    temp  = re.findall(QUERY_AMPERSAN,SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
            if(element not in ORGANIZATION_FOUND):
                ORGANIZATION_FOUND.append(f"Line {LINE_NUMBER}: ORGANIZATION "+element)

    #Rule 10-...bank since 
    if 'bank' in SAMPLE_TEXT or 'BANK' in SAMPLE_TEXT:
        temp = re.findall(r'((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ )*)[A-ZÇĞİÖŞÜ][a-zçğıöşü]*(?:(?:bank)|(?:BANK)))',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in ORGANIZATION_FOUND):
                ORGANIZATION_FOUND.append(f"Line {LINE_NUMBER}: ORGANIZATION "+element)

    #Slightly modified existing rule.
    for END in QUERY_ORGANIZATION_ENDS:
        if END in SAMPLE_TEXT:
            QUERY = '((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* ){1,})'+'{params}+)'.format(params=END)
            temp = re.findall(QUERY,SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in ORGANIZATION_FOUND):
                    ORGANIZATION_FOUND.append(f"Line {LINE_NUMBER}: ORGANIZATION "+element)
    
    #Slightly modified existing rule.
    if 'spor' in SAMPLE_TEXT:
        temp = re.findall(r'((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* )*[A-ZÇĞİÖŞÜ][a-zçğıöşü]*spor+)',SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in ORGANIZATION_FOUND):
                ORGANIZATION_FOUND.append(f"Line {LINE_NUMBER}: ORGANIZATION "+element)

    #Slightly modified existing rule.
    for uppercaseWord in re.finditer(r'[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*',SAMPLE_TEXT):
        uppercaseWord = SAMPLE_TEXT[uppercaseWord.start():uppercaseWord.end()]
        if uppercaseWord in ORGANIZATION:
            if(uppercaseWord not in ORGANIZATION_FOUND):
                ORGANIZATION_FOUND.append(f"Line {LINE_NUMBER}: ORGANIZATION "+uppercaseWord)

    ##DATE
    #Rule 11-Date Detection seperated with /,-,.,|,: formatted as dd/mm/yyyy,mm/dd/yyyy,yyyy/dd/mm,yyyy/mm/dd
    for regex in listOfDateRegex:
        temp = re.findall(regex,SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in DATE_FOUND):
                DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)

    #Rule 12-Time Detection seperators .,:,- in one regex
    temp = re.findall(r'((?:\D[0,1][0-9][\.,:,-][0,1,2,3,4,5][0-9][ ,\',\w]{1})|(?:\D2[0,1,2,3][\.,:,-][0,1,2,3,4,5][0-9][ ,\',\w]{1})|(?:\D24[\.,:,-]00[ ,\',\w]{1}))',SAMPLE_TEXT)
    for element in temp if len(temp)>0 else []:
        if(element not in DATE_FOUND):
            DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)

    #Rule 13-Date Recognition with case aware conditioning seeking for 'yılı' or 'ayı' embedded inside the Text
    for month in MONTH_LIST:
        if month in SAMPLE_TEXT:
            temp = re.findall(fr'((?:(?:0[1-9])|(?:[0-9])|(?:[1-2][0-9])|(?:3[0,1])) {month} (?:\d+\d+\d+\d+))',SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
        
            temp = re.findall(fr'(?:\D+ )({month} (?:\d+\d+\d+\d+))',SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
            temp = re.findall(fr'([0-9]+ {month})(?:(?:\D{2})|(?:\.))',SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
            
            if 'yılı' in SAMPLE_TEXT and 'ayı' in SAMPLE_TEXT:
                temp = re.findall(fr'((?:\d+\d+\d+\d+) yılı(?:nın)? {month} ayı)',SAMPLE_TEXT)
                for element in temp if len(temp)>0 else []:
                    if(element not in DATE_FOUND):
                        DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
            
            if 'ayı' in SAMPLE_TEXT and 'yılı' not in SAMPLE_TEXT:
                temp = re.findall(fr'({month} ayı)',SAMPLE_TEXT)
                for element in temp if len(temp)>0 else []:
                    if(element not in DATE_FOUND):
                        DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
            if 'yılı' in SAMPLE_TEXT and 'ayı' not in SAMPLE_TEXT:
                temp = re.findall(fr'((?:\d+\d+\d+\d+) yılı)',SAMPLE_TEXT)
                for element in temp if len(temp)>0 else []:
                    if(element not in DATE_FOUND):
                        DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
    
    #Rule 14-Date Recognition checking for MmÖöSs digit,digit,... .yüzyıl
    if 'yüzyıl' in SAMPLE_TEXT:
            temp = re.findall(r'((?:(?:[M][ö,Ö,s,S])|(?:[m][ö,s]))[\., ,\-,\\](?:[1-9][0-9]*)\.yüzyıl)',SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
    #Rule 15-Date Recognition checking ayın 3'ü ,5'i etc.                
    if 'ayın' in SAMPLE_TEXT:
            temp = re.findall(r"(ayın \d+(?:\'s?[i,ü,u,ı]n?d?[e,a]))",SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
    #Rule 16-Date Recognition checking öğleden sonra (saat) 3'te or 11'de etc.
    if 'öğleden sonra' in SAMPLE_TEXT:
            temp = re.findall(r"(öğleden sonra(?:(?: saat )| )\d+'[d,t][e,a])",SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)
    if 'saat' in SAMPLE_TEXT and 'öğleden sonra' not in SAMPLE_TEXT:
            temp = re.findall(r"(saat \d+(?:\'[d,t][e,a]))",SAMPLE_TEXT)
            for element in temp if len(temp)>0 else []:
                if(element not in DATE_FOUND):                  
                    DATE_FOUND.append(f"Line {LINE_NUMBER}: DATE "+element)

    #Person
    #Rule 17-For Person Detection Titles used as Beginning of words
    for title in TITLES:
        temp = re.findall(fr"(?:{title} )((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*[ ,]?))+)",SAMPLE_TEXT)
        for element in temp if len(temp)>0 else []:
            if(element not in PERSON_FOUND):
                PERSON_FOUND.append(f"Line {LINE_NUMBER}: PERSON "+element)
    
    #Rule-18 Name Lexicon is divided to name and surname and any individual name can be counted as name since 
    #name lexicon is  pruned from words with multiple meaning(such as Eylül etc.) but surname is not.
    #This rule uses a heuristic stating that name can be matched without checking surname but surname  
    #can not be used as individually.Surname is not pruned since they are more specific and more likely to contain
    #a multi-meaning word.
    suspects = re.findall(r'((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]+[ ,]?)+)',SAMPLE_TEXT)
    for suspect in suspects:
        occurence = 0
        tokenized = suspect.rstrip().split(" ")
        if(len(tokenized)>1):
            for word in tokenized:
                if(word.title() in PERSON.name or word.title() in PERSON.surname or re.match("([A-Z][a-zA-Z]*(?:oğlu|ov|[c,ç]?[i,ü,ı]?ev|son))",word)):
                    occurence+=1
            if(occurence==len(tokenized)):
                PERSON_FOUND.append(f"Line {LINE_NUMBER}: PERSON "+suspect)
        else:
            for word in tokenized:
                if(word.title() in PERSON.name ):
                    occurence+=1
            if(occurence==len(tokenized)):
                PERSON_FOUND.append(f"Line {LINE_NUMBER}: PERSON "+suspect)
    
    if len(suspects)==0:
        for job in JOBS:
            res = re.match("([A-Z][a-z]*)\'in [a-zı]* {job}i?y?d?[i,ı,ü].",SAMPLE_TEXT)        
            if res:
                PERSON_FOUND.append(f"Line {LINE_NUMBER}: PERSON "+res[1])
    LOCATIONS_SORTED = sorted(LOCATIONS_FOUND)
    DATE_FOUND = sorted(DATE_FOUND)
    ORGANIZATION_FOUND = sorted(ORGANIZATION_FOUND)
    PERSON_FOUND = sorted(PERSON_FOUND)
    
    for location in LOCATIONS_SORTED:
        print(location)
    for organization in ORGANIZATION_FOUND:
        print(organization)
    for date in DATE_FOUND:
        print(date)
    for person in PERSON_FOUND:
        print(person)
