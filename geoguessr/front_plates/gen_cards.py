import csv
from data.state_abbrev import abbrev

data = open('data/data.txt', 'r').read().splitlines()

front = data[1].split(', ')
rear = data[3].split(', ')
most = data[5].split(', ')

# tag format: Geo::Country::US::State/territory Geo::Front_Plates

'''
with open('data/front_plates_cards.csv', 'w', newline='') as f:
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
'''