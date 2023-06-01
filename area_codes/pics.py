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

url1 = "http://www.usa.com/area-code-map/"
url2 = "https://m.24timezones.com/static_images/area_codes/"
url_ending = ".png"

unexpected_status_codes = []

def count_404(start, end):
    print("beginning to test url: " + start + "..." + end)

    num404 = 0
    num200 = 0

    for area_code in area_codes:
        try:
            url = start + area_code + end
            r = requests.get(url)
            # status code should be either 404 or 200; something else would be unexpected
            if r.status_code == 404:
                num404 += 1
            elif r.status_code == 200:
                num200 += 1
            else:
                print("Unexpected status code: " + str(r.status_code))
                unexpected_status_codes.append(f"{area_code} raised error {str(r.status_code)} with url {url}")
        except Exception as e:
            print("Exception raised: " + str(e))

    return num404, num200


usa404, usa200 = count_404(url1, url_ending)
tz404, tz200 = count_404(url2, url_ending)

print(f"usa404: {usa404}; usa200: {usa200}")
print(f"tz404: {tz404}; tz200: {tz200}")
print("below should be empty list")
print(unexpected_status_codes)
