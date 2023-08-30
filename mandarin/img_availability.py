# source for data: https://github.com/ruddfawcett/hanziDB.csv/blob/master/data/hanziDB.csv
import requests
import csv

row_num = 0
with open('hanziDB.csv', encoding='utf-8') as hanzifile:
    hanzireader = csv.reader(hanzifile, delimiter=',')
    for row in hanzireader:
        row_num += 1
        if row_num > 5:
            break
        print(row)
        char = row[1]
        url_template = f"https://commons.wikimedia.org/wiki/File:{char}-bw.png"
        print(char)
        print(url_template)
        r = requests.get(url_template)
        print(r.status_code)
