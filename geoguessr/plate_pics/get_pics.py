import requests
import urllib.request

url1 = 'https://theus50.com/images/state-licenses/'
url2 = '-license.jpg'

test_state = 'california'
state = test_state

unexpected_status_codes = []

try:
    url = url1 + state + url2
    r = requests.get(url)
    # status code should be either 404 or 200; something else would be unexpected
    if r.status_code == 404:
        #num404 += 1
        pass
    elif r.status_code == 200:
        #num200 += 1
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
        #req = urllib.request.Request(url, headers=headers)
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            # filename ex: data/pics/tz/tz215.png
            filename = 'data/pics/' + state + '.jpg'
            with open(filename, 'wb') as f:
                f.write(response.read())
        except Exception as e:
            print("error when trying to save image")
            print(f"exception is: {e}")
    else:
        print("Unexpected status code: " + str(r.status_code))
        unexpected_status_codes.append(f"{state} raised error {str(r.status_code)} with url {url}")
except Exception as e:
    # 24timezones.com gives 403 with urllib's default user agent--had to change
    print("Exception raised: " + str(e))