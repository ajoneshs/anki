import requests
from bs4 import BeautifulSoup
import csv

driving_side_url = 'https://en.wikipedia.org/wiki/Left-_and_right-hand_traffic'
html_text = requests.get(driving_side_url).text
soup = BeautifulSoup(html_text, 'html.parser')

tables = soup.find_all('table')
table = tables[1]
table_body = table.find('tbody')

data = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

print(data)

with open('wiki_table.csv', 'w', newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    row_num = 0
    for row in data:
        row_num += 1
        writer.writerow(row)

        # to make sure I haven't missed any countries with weird results
        # points me to CSV row numbers
        if len(row) > 1 and len(row[1]) >= 3:
            if row[1][1:3] != 'HT':
                print(row_num)