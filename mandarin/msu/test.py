from playsound import playsound
import requests
import os
import json

print(os.getcwd())

f = open('pinyin_ids.json')
pinyin_ids = json.load(f)

syllable1 = "nǐ"
syllable2 = "xióng"
id = (pinyin_ids[syllable2])[4]

#id = 1662
url1 = f"https://tone.lib.msu.edu/tone/{id}/PROXY_MP3/download"
url2 = f"https://tone.lib.msu.edu/tone/{id}/PROXY_MP3/view"

downloaded_audio = requests.get(url1)
with open(f'audio/{id}.mp3', 'wb') as f:
    f.write(downloaded_audio.content)

os.chdir('audio')
print(os.getcwd())

playsound(f'{id}.mp3')