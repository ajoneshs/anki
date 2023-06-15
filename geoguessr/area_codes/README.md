This directory contains the files used to create my Anki area code deck.

update_checker.py can be used to see if the website where the data was sourced from has been changed. Presumably this website would be updated if new area codes are added, or existing ones are changed so this would let me know I need to update my deck.

gen_cards.py is the code used to generate a csv file with area codes and relevant info and maps.

get_maps.py was used to download images and create a list of which images were successfully downloaded (lists and images themselves available in data/pics/). The images had to be manually copied into Anki's collection.media directory (C:\Users\senoj\AppData\Roaming\Anki2\User 1\collection.media)

anki_import_settings.PNG provides the settings used when importing the csv into Anki. The settings should work perfectly.

Images came from:
http://www.usa.com/area-code-map/215.png
and
https://m.24timezones.com/static_images/area_codes/215.png