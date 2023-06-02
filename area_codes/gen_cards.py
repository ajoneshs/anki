import requests
from bs4 import BeautifulSoup
import csv

area_codes_url = 'https://www.bennetyee.org/ucsd-pages/area.html'
html_text = requests.get(area_codes_url).text
soup = BeautifulSoup(html_text, 'html.parser')

table = soup.find('table')

area_codes = []
regions = []
descriptions = []

# extract data from html
for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    
    area_code = cells[0].text.strip()
    region = cells[1].text.strip()
    description = cells[3].text.strip()

    area_codes.append(area_code)
    regions.append(region)
    descriptions.append(description)

# load lists of available images
with open('data/pics/tz.csv', 'r') as f:
    tz_csv = f.read()
with open('data/pics/usa.csv', 'r') as f:
    usa_csv = f.read()

# generate csv file to import into Anki
with open('data/area_code_cards.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    field = ["front", "back", "tag"]
    #writer.writerow(field)
    
    for i in range(len(area_codes)):
        # generating maps field
        tz_img_exists = area_codes[i] in tz_csv
        usa_img_exists = area_codes[i] in usa_csv
        # maybe need to str(area_codes[i])
        maps_field = (
            ('<img src="tz' + area_codes[i] + '.png">') * tz_img_exists + '<br>' + 
            ('<img src="usa' + area_codes[i] + '.png">') * usa_img_exists
        )
        writer.writerow([area_codes[i], f"Region: {regions[i]}<br>{descriptions[i]}", maps_field, "AC::" + regions[i]])