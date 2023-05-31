# checks to see if the source data has been changed at all

import requests

og = open("data/area_codes.html", "r")
og_file = og.read()

area_codes_url = "https://www.bennetyee.org/ucsd-pages/area.html"
cur_file = requests.get(area_codes_url).text

same_file = og_file == cur_file

if same_file:
    print("No changes detected")
else:
    print("Changes detected!")
    new = open("data/updated_area_codes.html", "w")
    new.write(cur_file)
    new.close()

og.close()