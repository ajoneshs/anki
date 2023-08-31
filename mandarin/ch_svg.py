import requests
from bs4 import BeautifulSoup

# http://www.chinesehideout.com/tools/strokeorder.php?c=們
url = "http://www.chinesehideout.com/tools/strokeorder.php?c=%E5%80%91"

response = requests.get(url)
print(response.content)

with open("test.html", "wb") as f:
    f.write(response.content)

#soup = BeautifulSoup()