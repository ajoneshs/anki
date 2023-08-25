from playsound import playsound
import requests
import os

print(os.getcwd())

id = 1662
url1 = f"https://tone.lib.msu.edu/tone/{id}/PROXY_MP3/download"
url2 = f"https://tone.lib.msu.edu/tone/{id}/PROXY_MP3/view"

downloaded_audio = requests.get(url1)
with open(f'audio/{id}.mp3', 'wb') as f:
    f.write(downloaded_audio.content)

os.chdir('audio')
print(os.getcwd())

playsound(f'{id}.mp3')