import requests
from bs4 import BeautifulSoup

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