import requests
from bs4 import BeautifulSoup
import csv
import urllib.request

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

    # for naming images stored locally to reflect their source
    if "usa" in start:
        type = "usa"
    else:
        type = "tz"

    for area_code in area_codes:
        # remove later--just for testing
        if area_code == 204 or area_code == "204":
            break

        try:
            url = start + area_code + end
            # doesn't solve the problem
            # r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
            # version that I think should work
            r = requests.get(url)
            # status code should be either 404 or 200; something else would be unexpected
            if r.status_code == 404:
                num404 += 1
            elif r.status_code == 200:
                num200 += 1
                # original which doesn't work
                # urllib.request.urlretrieve(url, "pics/" + type + area_code + ".png")
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"}
                req = urllib.request.Request(url, headers=headers)
                try:
                    response = urllib.request.urlopen(req)
                    with open("pics/" + type + area_code + ".png", 'wb') as f:
                        f.write(response.read())
                except Exception as e:
                    print("error when trying to save image")
                    print(f"exception is: {e}")
            else:
                print("Unexpected status code: " + str(r.status_code))
                unexpected_status_codes.append(f"{area_code} raised error {str(r.status_code)} with url {url}")
        except Exception as e:
            # tz doesn't seem to let me save images--gives 403
            print("Exception raised: " + str(e))

    return num404, num200


usa404, usa200 = count_404(url1, url_ending)
tz404, tz200 = count_404(url2, url_ending)

print(f"usa404: {usa404}; usa200: {usa200}")
print(f"tz404: {tz404}; tz200: {tz200}")
print("below should be empty list")
print(unexpected_status_codes)
