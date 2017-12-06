import csv
with open(r"C:\Users\chen\Desktop\欧盟微博关键字.csv","r+") as file:
    for line in csv.reader(file):
        print(line)