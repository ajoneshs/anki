# source for data: https://github.com/ruddfawcett/hanziDB.csv/blob/master/data/hanziDB.csv
import requests
import csv

# CSV header
# frequency_rank,charcter,pinyin,definition,radical,radical_code,stroke_count,hsk_level,general_standard_num

# check http://www.strokeorder.info/mandarin.php?q={char} next
# maybe http://www.chinesehideout.com/tools/strokeorder.php?c={char}

# makemeahanzi seems like the best option
# Anki won't loop animated SVGs though so I would have to use the still SVGs
# supposedly has simplified and traditional
# https://github.com/skishore/makemeahanzi

# https://github.com/nmarley/chinese-char-animations might work
# has gifs of simplified and traditional characters

num_200 = 0
num_other = 0
num_404 = 0
row_num = 0
with open('hanziDB.csv', encoding='utf-8') as hanzifile:
    hanzireader = csv.reader(hanzifile, delimiter=',')
    for row in hanzireader:
        row_num += 1
        if row_num > 1000:
            break
        print(row)
        char = row[1]
        url_template = f"https://commons.wikimedia.org/wiki/File:{char}-bw.png"
        print(char)
        print(url_template)
        r = requests.get(url_template)

        status = r.status_code
        if status == 200:
            num_200 += 1
        else:
            num_other += 1
            if status != 404:
                print(f"Code found other than 404/200: {status}")
                print(f"Triggered by: {url_template}")
            else:
                num_404 +=1
        print(r.status_code)

print(f"Status codes")
print(f"200: {num_200}")
print(f"404: {num_404}")

percent = num_200 / (num_other + num_200) * 100

print(f"Percent returning 200: {percent}%")

'''
With URL template: https://commons.wikimedia.org/wiki/File:{char}-bw.png
For simplified characters
Status codes
200: 738
404: 262
Percent returning 200: 73.8%
'''