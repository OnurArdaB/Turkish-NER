import pandas as pd

df = pd.read_csv('worldcompanies.csv',delimiter=",")

parent_company = df['ParentCompany']
company = df['Company']

unique_parent = set()
unique_company = set()
for inst in parent_company:
    if(inst not in unique_parent):
        unique_parent.add(inst)
for inst in company:
    if(inst not in unique_company):
        unique_company.add(inst)

with open('ORGANIZATION.txt','a',encoding="utf-8") as file:
    file.write("#######################\n")
    for parent in sorted(unique_parent):
        file.write(parent+'\n')
    file.write("#######################\n")
    for company in sorted(unique_company):
        file.write(company+'\n')