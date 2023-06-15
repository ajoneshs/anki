import requests
from bs4 import BeautifulSoup
import csv
import re

driving_side_url = 'https://en.wikipedia.org/wiki/Left-_and_right-hand_traffic'
html_text = requests.get(driving_side_url).text
soup = BeautifulSoup(html_text, 'html.parser')

tables = soup.find_all('table')
#print(len(tables))
#print(tables[1].prettify()[0:2000])
# Table with countries and LHT or RHT is tables[1]
table = tables[1]

countries = []
sides = []


################
# doesn't work for Canada, China, UK, US because of the sub-categories
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')

    country = cells[0].text.strip()
    side = cells[1].text.strip()
    abc = ['RHT', 'LHT']
    if side[0:3] not in abc:
        print('------------------------------')
        print("Error found")
        print(f"country: {country}")
        print(f"lht or rht: {side}")
        print('------------------------------')
        continue

    countries.append(country)
    sides.append(side)

print(sides)
print(len(sides))
print(countries)

'''

with open('driving_side_cards.csv', 'w', newline='') as f:
    writer = csv.writer(f)

# add tags

'''