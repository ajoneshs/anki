import requests
from bs4 import BeautifulSoup
import csv
import re

driving_side_url = 'https://en.wikipedia.org/wiki/Left-_and_right-hand_traffic'
html_text = requests.get(driving_side_url).text
soup = BeautifulSoup(html_text, 'html.parser')

tables = soup.find_all('table')
#print(tables)
print(len(tables))
print(tables[1].prettify()[0:2000])


'''
#print(soup.prettify())

start_string = "Worldwide distribution by country"

print(type(soup))

re.findall(start_string, soup)
'''