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
imgs_saved = 0
usa_imgs = []
tz_imgs = []


# count available images and save them
def save_imgs(start, end):
    print("beginning to test url: " + start + "..." + end)

    global imgs_saved
    num404 = 0
    num200 = 0

    # used for naming images stored locally to reflect their source
    # types reflect the website names (USA.com and 24TimeZones.com)
    if "usa" in start:
        type = "usa"
    else:
        type = "tz"

    for area_code in area_codes:
        try:
            url = start + area_code + end
            r = requests.get(url)
            # status code should be either 404 or 200; something else would be unexpected
            if r.status_code == 404:
                num404 += 1
            elif r.status_code == 200:
                num200 += 1
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
                req = urllib.request.Request(url, headers=headers)
                try:
                    response = urllib.request.urlopen(req)
                    # filename ex: data/pics/tz/tz215.png
                    filename = 'data/pics/' + type + '/' + type + area_code + '.png'
                    with open(filename, 'wb') as f:
                        f.write(response.read())
                    if type == "usa":
                        usa_imgs.append(area_code)
                    else:
                        tz_imgs.append(area_code)
                    imgs_saved += 1
                except Exception as e:
                    print("error when trying to save image")
                    print(f"exception is: {e}")
            else:
                print("Unexpected status code: " + str(r.status_code))
                unexpected_status_codes.append(f"{area_code} raised error {str(r.status_code)} with url {url}")
        except Exception as e:
            # 24timezones.com gives 403 with urllib's default user agent--had to change
            print("Exception raised: " + str(e))

    return num404, num200


usa404, usa200 = save_imgs(url1, url_ending)
tz404, tz200 = save_imgs(url2, url_ending)


# write to data/pics/ a list of the images that were successfully saved
def write_img_lists(type, img_list):
    filename = 'data/pics/' + type + '.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in img_list:
            writer.writerow([i])


# save file with lists of images successfully saved
write_img_lists('usa', usa_imgs)
write_img_lists('tz', tz_imgs)


# stats and error checking
print(f"total area codes: {len(area_codes)}")
print(f"usa404: {usa404}; usa200: {usa200}")
print(f"tz404: {tz404}; tz200: {tz200}")
print("images saved == total non-404s?: " + str(imgs_saved == (usa200 + tz200)))
print(f"No unexpected status codes?: " + str(unexpected_status_codes == []))