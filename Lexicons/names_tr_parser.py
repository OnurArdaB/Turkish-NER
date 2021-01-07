#https://kerteriz.net/tum-turkce-erkek-ve-kadin-isimleri-cinsiyet-listesi-veritabani/
with open("names_tr.txt",encoding="utf-8") as names_file,open("PERSON.txt","a+",encoding='utf-8') as output:
    names = names_file.readlines()
    for name in names:
        temp = name.split(",")[0][1:]
        temp = temp[1:-1]
        output.write(temp+"\n")
        