import pandas as pd

df = pd.read_csv("worldcities.csv",delimiter=",")

city_ = df["city_ascii"].to_list()

file = open("LOCATION.txt","a") #opening file in append mode
for city in city_:
    file.write(city+'\n')