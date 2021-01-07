import pandas as pd

df = pd.read_csv('worlduniversities.csv',delimiter=',')
print(df.head(-1))
university_names = df['institution']
uniqueness = set()
for name in university_names:
        if(name not in uniqueness):
            uniqueness.add(name)
with open('ORGANIZATION.txt','a',encoding="utf-8") as file:
    for name in sorted(uniqueness):
        file.write(name+'\n')
    

print(len(university_names))