# Turkish NER with Python Regexes
File and folder structure of the project.
```
│   NER Example Data.txt
│   ner.py
│   README.md
│   
├───Lexicons
│   │   cities_parser.py
│   │   company_parser.py
│   │   country_crawler.py
│   │   district_crawler.py
│   │   duplicate_checker.py
│   │   job_crawler.py
│   │   Kısaltmalar_Dizini.pdf
│   │   LOCATION.txt
│   │   names_eng_crawler.py
│   │   names_tr.txt
│   │   names_tr_parser.py
│   │   ORGANIZATION.txt
│   │   PERSON.py
│   │   TODO.md
│   │   zemberek_location_tr.txt
│   │   second_names.py
│   │   university_parser.py
│   │   worldcities.csv
│   │   worldcompanies.csv
│   │   worlduniversities.csv
```
## Lexicon Generation
Files with _parser.py extension:

cities_parser.py,company_parser.py and university_parser.py are used in order to parse information from csv files and re-write the extracted information to their respective lexicon files.(Lexicon file names are written with capital letter.)

cities_parser.py re-writes to LOCATION.txt while company_parser.py and university_parser.py re-writes to ORGANIZATION.txt.
worldcities.csv(https://www.kaggle.com/viswanathanc/world-cities-datasets)
worlduniversities.csv(https://www.kaggle.com/mylesoneill/world-university-rankings)

names_tr_parser.py is the final parser that parses names_tr.txt file(https://kerteriz.net/depo/isimler.zip) by basically splitting every line of instance with respect to ',' delimiter and re-writes the extracted information to the PERSON.txt.(PERSON.txt file has been modified by manually and reversed in to a .py file which contains a dictionary data structure in order to increase the speed of accesing PERSON names.)

Files with _crawler.py extension:

country_crawler.py extracted a page with country names(190 of them) from given URL("https://www.bbc.co.uk/academy/tr/articles/art20150916134647005").According to UN there exists 193 countries in world and the missing 3 countries were added manually to the list(LOCATION.txt) with also additional conutry and region names found in wikipedia.There are also some special location indetifying words such as Dağı or Adası which allows a query to match a word without statically typing the respecting name to the list.Those words are written manually and extracted from wikipedia.

district_crawler.py extracted a page with district names of turkey from given URL(https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27nin_il%C3%A7eleri) extracted the necessary information from the html page by parsing it with bs4(BeautifulSoup) module and re-writed the information to the LOCATION.txt.

names_eng_crawler.py extracted necessary information dynamically from the given URL(https://nameberry.com/baby-names/164/English-Names) since the datasize was extremely large in order to read in one time.It takes a lot of time in runtime but extracts the information perfectly.Extracted information is added to the PERSON.txt file.This specific website is choosen due to the fact that it was the best html formatted website for parsing , other alternatives used more complex table structures.

job_crawler.py extracted a page in html format from the given URL('https://www.turkcebilgi.com/meslekler_listesi') that contains a list of jobs in turkish(Not very comprehensive).Extracted jobs are added to second_names.py.

Kısaltmalar_Dizini.pdf was obtained from TDK and parsed with pyPdf2 and several other modules by command line.This file contained most of the possible titles that would allow a query to be written with regex and some other important organization names such as political parties and goverment institutions with their respective abbreviations.Since the current dataset contained tags(<b_enamex> etc.) these abbreviations could not perform well but can work properly on a well formatted file.

zemberek_location_tr.py
This file is taken from the Zemberek Turkish NLP tool(Also contains a module for NER using Neural Networks and etc.).It is very comprehensive and actually might be too comprehensive but still performs very well especially for very special cases like Aşağıaşılar köyü which is a small village of Akseki/Antalya with population of 50 even exists in the lexicon.

duplicate_checker.py
This script is used in order to eliminate the duplicate entries in files due to the fact that all of the mentioned files were obtained from web.These files are extremely large and it gets extremely hard to manually detect and eliminate duplicated entries.
Eliminating the duplicates is important since written queries can call these duplicates and match them multiple times which would not be correct.

Manually correction issue:

Turkish contains lots of words that can be interpreted as both for a person or a location or a date.Eylül is a great example of this name.It is possible to create rules that can check the before and after of the word in order to come to a decide on what to interpret but there are still some cases that the manually generated queries can not manage to handle these confusions.In order to eliminate this issue some of the Lexicons are eliminated from the Lexicons manually.

# Regular Expressions

## Location
    -Rule 1-Country and Continent Detection via Lexicon
    There are some very unique words that needs to be decided over a comparison with the words in the lexicon.In this rule any word sequence where       every word in it starts with an uppercase and followed by uppercase or lower case words finally followed by whitespace or '-' are captured by a     regex and compared with every word inside the locations lexicon.

    ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*[ -]?)+(?:[\.,]*))

    This regex tries to capture a sequence of words separated whether with a whitespace or with a minus sign (-).
    It is fault tolerant to cases like Paraguay,Mexica case where it captures Paraguay and Mexica seperately.
    
    -Rule 2-Multiword containing Country ,Region ,Mountain ,Sea and etc in the end of the string.
    This rule is actually a very repetitive rule but added inside the report since there is no better way to capture words appearing in this format.
    
    This rule tries to iterate over each noun in the given list and if the text contains that noun , than the program applies a regex with the given noun.This is very useful for capturing street names (Sok.) or island names etc. There exists an infinite amount of locations with the given format so it is not a option to create a lexicon that can catch these cases statically.In order to solve this problem this rule is applied which traverses these locations dynamically.
    
    These nouns are located in second_names.py file inside the Lexicons folder named as QUERY_LOCATION_ENDS.
    There is an another rule that uses the same idea with rule given above with a different regex.
    Country names ending with -istan is captured with the given regex.

    ((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]* ){0,})[A-ZÇĞİÖŞÜ][a-zçğıöşü]*istan+)

    -Rule 3-Latitude Longitude -+90 For Latitude and -+180 For Longitude
    Latitude and longtitude is again a identifies a location and it is unique which can be counted as an entity.
    We capture the stated information by applying the following regex.
    
    ((?:(?:[+,-]?[0-8][0-9]\.?[0-9]*)|(?:[+,-]?90\.?[0-9]*))\s?(?:(?:[+,-]?[1]?[0-7][0-9]\.?[0-9]*)|(?:[+,-]?[0-9][0-9]\.?[0-9]*)|(?:[+,-]?180\.[0-9]*)))

    Latitude ranges from -90 to +90 with posibility of having decimal values.from 0-89 is handled seperately in first inner non-capturing parenthesis.90 with decimal value is handled seperately aswell.Same conditions applied for longtitude with slight change.0-99 is handled in the second inner parenthesis.If it is not captured the 'or' operator advises that it can be 100-179 and if it does not holds,final assumption states that it can be 180.

    -Rule 4-'daki 'deki 'taki 'teki
    Any string followed by ('daki 'deki 'taki 'teki) locative suffix most probably specifies a location.
    ((?:(?:[A-ZÇİÖŞÜ][a-zçıöşüA-ZÇİĞÖŞÜ]*\s?){1,})(?=\'\s?[d,t][a,e]ki))
    This regex initially finds a word sequence and checks whether it is followed by a locative suffix.Locative suffix is defined dynamically.

    -Rule 5-Güzergahı .... 'ya doğru
    This rule states that any word that comes after Güzergahı or güzergahı followed by 'ye or 'ya or 'a or 'e is a location.
    [g,G]üzergahı ((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*){1,}))[ ,]?\'[ ,]?y?a?e? doğru 

    -Rule 6- .... semalarında
    This rule states that any word that starts with an uppercase that is followed by semalarında is a location
    ((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* ){1,}))semalarında
    
    -Rule 7 .... gidecek.
    This rule checks more details than the previous rules.A word sequence that started with a lowercased word or word followed by a subsequence of words starting with uppercase and/or contains uppercase words finally ending with 'gidecek.' must contain a location name.That location name can be extracted by current regex.
    (?:\w+){1} (?:[a-zçğıöşü]){1,} ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*[\s]?){1,})(?:[\s]?\'y[a,e]{1}) gidecek\.

    -Rule 8 Dün akşam saatlerinde .... .... ('dan or 'den) yola çıkan (herhangi bir araç tipi)
    This rule is created by examining the format on google.In a simple query on google it can be observed that every sentences in this format contained a location name.
    (?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*) (?:[a-zçğıöşü]*) ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]*[\s]?){1,})(?:\'[d,t]{1}[a,e]{1}n) yola çıkan (?:otobüs|kamyon|araba|araç)

## Organization
# ORGANIZATION
    -Rule 9-Procter & Gamble or Procter Procter Procter ... & Gamble Gamble ...
    Despite the fact that this rule might seem thin , it captures a lot names within the right format.
    ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]* )+\& (?:\w+[ ,]?)+)
    

    #Rule 10-...bank BANK 
    This query is capturing bank names.Most of the banks in turkey contain bank in their name.This allows regular expression to capture bank names.
    (r'((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ )*)[A-ZÇĞİÖŞÜ][a-zçğıöşü]*bank)',SAMPLE_TEXT)
    A very similiar rule is again applied for finding Spor Kulüpleri as '*spor'
    ((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]* )*[A-ZÇĞİÖŞÜ][a-zçğıöşü]*spor+)

    
    There are 2 duplicate rules applied where one is for direct matching the organization names from the Lexicon and the other is matchin organization names by adding an end word to a query.


## Date
    -Rule 11-Date Detection (seperated with /,-,.,|,: formatted as dd/mm/yyyy,mm/dd/yyyy,yyyy/dd/mm,yyyy/mm/dd)
        In Turkish , date sequences are formatted as dd/mm/yyyy but for a more detailed search other formats are implemented.
        A for loop iterates over each seperator since a date can not be formatted as dd/mm.yyyy.Each seperator is located inside the regex and the created queries are appended inside of a list.All of the regular expressions implemented for this part works in a similiar way.Day is ruled as it can not pass any number above 31 and month is ruled as it can not pass any number above 12.
    
    -Rule 12-Time Detection (seperated  with .,:,-)
    ((?:\D[0,1][0-9][\.,:,-][0,1,2,3,4,5][0-9][ ,\',\w]{1})|(?:\D2[0,1,2,3][\.,:,-][0,1,2,3,4,5][0-9][ ,\',\w]{1})|(?:\D24[\.,:,-]00[ ,\',\w]{1}))
    
    This regex can capture 3 possible scenarios where in the first one time can be between 00.00 to 19.59 and handled separately since if 2x.xx can only have [0-4] numbers for the second digit before seperator.Second possible scenario was for to catch any time between 20.00 and 23.59.Final possible scenario was to capture 24.00.

    -Rule 13-Date Recognition with case aware conditioning seeking for 'yılı' or 'ayı' embedded inside the text
        Dates can also be contain months stated as verbally.In order to captur these possbile conditions a month list is generated.Every month instance is appended to the regular expressions.In each iteration the month is first searched through the text and if the month name exists in the text than different queries are done.These queries have differentiative parts so they will not capture the same information twice.

        Condition-1:
        e.g 12 Ocak 1998
        ((?:(?:0[1-9])|(?:[0-9])|(?:[1-2][0-9])|(?:3[0,1])) {month} (?:\d+\d+\d+\d+))
        Days of a month can only range from 0-31.

        Condition-2:
        e.g Ocak 1998 guarenteed that it will not capture 12 Ocak 1998
        (?:\D+ )({month} (?:\d+\d+\d+\d+))

        Condition-3:
        08 Ocak continued by 2 non-digit letters or a single.
        e.g Gidiş tarihi 08 Ocak. , 08 Ocak günü yola çıkacaklar.
        ([0-9]+ {month})(?:(?:\D{2})|(?:\.))

        Condition-4:
        If both of the 'ayı' and 'yılı' word is inside of the text than it can contain a sequence like 1998 yılı Şubat ayı....
        e.g 1998 yılı Şubat ayı yolcuklarına başladılar. or 1998 yılının Şubat ayında yolcuklarına başladılar.
        ((?:\d+\d+\d+\d+) yılı {month} ayı) 

        Condition-5:
        If 'ayı' exists or 'yılı' exists but not both of them in the same time
        e.g 2020 yılı öğrenciler için zor bir yıldı. or Kasım ayı çok yoğun geçiyor.
        
        ({month} ayı)
        
        ((?:\d+\d+\d+\d+) yılı)

    -Rule 14-Date Recognition checking for MmÖöSs digit,digit,... .yüzyıl
        This rule tries to capture word sequences like MÖ. 19.yüzyıl etc.It checks if yüzyıl is inside the text and if it does applies the regex given below.

        ((?:(?:[M][ö,Ö,s,S])|(?:[m][ö,s]))[\., ,\-,\\](?:[1-9][0-9]*)\.yüzyıl)

        (?:(?:[M][ö,Ö,s,S])|(?:[m][ö,s])) is for conditioning to capture the MÖ,Mö,MS,Ms,mö,ms cases and followed by a range of seperators.(?:[1-9][0-9]*)\.yüzyıl is for xxx.yüzyıl
    
    -Rule 15-Date Recognition checking ayın 3'ü ,5'i etc.
        This rule first checks whether the text contains 'ayın' string or not.If the text contains than applies the regex given below.    

        (ayın \d+(?:\'s?[i,ü,u,ı]n?d?[e,a]))

        This regex captures any word sequence beginning with ayın with a whitespace followed by a digit sequence of digits.Non-capturing parantheses tries to capture a wide range of words starting with a apostrophe , followed by a range of letters[i,ü,u,ı] that can have n or d or both at the same time ending with vowel e and a.

        e.g (ayın 3'ünde) ,(ayın 5'inde) ,(ayın 7'si or ayın 7'sinde)
    
    -Rule 16-Date Recognition in format of 'öğleden sonra 5'te' or 'öğleden sonra saat 5'te' or 'saat 5'te'
        In this rule , if conditions check which regex best suits for a query on the text.
        If 'öğleden sonra' is inside the text than the program applies the regex given below.

        (öğleden sonra(?:(?: saat )| )\d+'[d,t][e,a])
        In this regex we try to capture öğleden sonra word followed by saat(optionally) with 'de 'da 'te 'ta

        If there is no öğleden sonra but there is 'saat' in the text than program applies the regex given below.
        (saat \d+(?:\'[d,t][e,a]))
        They are not independent rules, both of the given above regular expressions create one rule.

## Person
    -Rule 17-Person Detection using Titles as the beginning of the context
        This rule uses a list of  titles as a beginning of a string and tries to capture as many words as possible starting with an uppercase and continues with a lowercase or uppercase.It conditions the words to be followed by a whitespace.
        
        (?:{title} )((?:(?:[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*[ ,]?))+)

        Title changes dynamically allowing the code to traverse every title and uses a non-capturing regular parentheses the title is not the only things that is wanted to be caught.Inside the second parentheses a word is defined that starts with an uppercase
        ,continued by unknown number of lowercases or uppercases and finally after the word sequence ends , it is conditioned that the word sequence to be followed by a whitespace or not.A single word with the specified format is captured by the given regex
        [A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ]*[ ,]? and it is located inside of a non-capturing parentheses stating that it wil at least repeat one time.

        Finally all these conditions are located inside a capturing regular parentheses in order to act such word sequences as a whole.

    -Rule 18-Name Detection over traversing existing words in Lexicon
        This rule first tries to capture every sequence of words that can be suspected as a proper noun.Captured words are then compared with the words in the lexicon with a simple heuristic.If the word sequence contains a single word , the word is compared against only the firstname lexicon since in turkish most of the lastnames are also meaningful words and some other types of words(Location,Organization) can be caught as Person names even if they are not.If the word sequence is larger than 1 word than the firstname and lastname lexicons both are used for capturing person names.This rule is a duplicate of several rules but Person case does not contain a large amount of different cases due to language.
    
    -Rule 19-Name Detection via .... ..... öğretmeniydi.
    In this rule it can be observed that the predicate defines the subject and the object as humans and other than a few outliers it needs to be followed by a name.Those outliers are 0 Şu Bu Onlar Şunlar Bunlar.This is one sample of this rule.
    It is possible to extend the given rule with creating a small list of jobs.Appplying those jobs iteratively we can find the name.

    -Rule 20-Name Detection surnames with patterns like oğlu,son etc
    ([A-Z][a-zA-Z]*(?:oğlu|ov|[c,ç]?[i,ü,ı]?ev|son))

Useful Links:
-https://pythex.org/
-https://tscorpus.com/
-https://www.aclweb.org/anthology/P11-3019.pdf
