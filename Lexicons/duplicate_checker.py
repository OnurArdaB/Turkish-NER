import sys

DupResolver = set()
with open("temp.txt","a+",encoding="utf-8") as file,open(sys.argv[1],"r",encoding="utf-8") as readfile:
    lines = readfile.readlines()
    print(lines)
    file.write("#####PROCESSED#####\n")
    for line in lines:
        if(line not in DupResolver):
            file.write(line)
            DupResolver.add(line)
