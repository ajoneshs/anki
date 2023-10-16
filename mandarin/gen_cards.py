'''
To-Do
* figure out source for stroke order
* consider adding audio
    * find source for audio
* improve formatting
    * i.e. add '--------' or similar between sections
    * add notes about what is being auto generated to make it more readily apparent if there is an error that needs to be manually corrected
        * i.e. print(f"Traditional character(s) found: {tr}") at initial get character step after user provides simplified character(s)
* add checking system to make sure user gives simplified character
* maybe add additional meaning field for short definition (i.e. what is memorized rather than the longer auto-generated cedict translation)
    * if I add this, add it after auto generating definition
    * maybe auto generate the short definition somehow using cedict
    * in anki, show quick definition by default and then show longer definition at bottom of card
    * https://www.reddit.com/r/Anki/comments/lk4kfr/how_do_i_display_a_field_in_anki_only_if_another/
* for audio, use MSU tone library for single syllables (i.e. single characters), find some other source for words when multiple syllables are needed
    * probably some text-to-speech model?
    * keep log of audio files already collected and sent to collections.media
    * maybe a .txt file in this dir that this file will check to see if the audio file has already been downloaded for another card
        * do this for image files too
'''



####### Audio #######
# Look into adding audio
#########################
#########################


import csv
import opencc
import pinyin
import pinyin.cedict
import json
import shutil
import pyttsx3
import requests
import unicodedata

# UPDATE VERSION NUMBER AS YOU MAKE CHANGES
version = "1.0"
ver_num = f'Mandarin::Version::v{version}'

# clearing CSV file at start just in case
open('cards.csv', 'w').close()

# for getting from pinyin syllable to MSU tone ID number (for adding audio files)
f = open('pinyin_ids.json')
pinyin_ids = json.load(f)

# for converting simplified to traditional characters
converter = opencc.OpenCC('s2t.json')

cards = []

##### Tags #####
# for words, tag with component characters
# for characters, tag with character itself
# tag with pinyin syllables (for just characters?? or words too?)
#tags = [chars_si, chars_tr, syllables, tones, tr_exists]

'''
tag setup
Mandarin
    Characters
        Simplified
        Traditional
    Pinyin
        Syllables
            Standard
            Numerical
            Toneless
        Tones
            1
            2
            3
            4
            5
    Type
        Character
        Word/Phrase
    Version
'''
pre_ch_si = 'Mandarin::Characters::Simplified::'
pre_ch_tr = 'Mandarin::Characters::Traditional::'
pre_pin_syl_std = 'Mandarin::Pinyin::Syllables::Standard::'
pre_pin_syl_num = 'Mandarin::Pinyin::Syllables::Numerical::'
pre_pin_syl_raw = 'Mandarin::Pinyin::Syllables::Toneless::'
pre_pin_syl_tone = 'Mandarin::Pinyin::Tones::'
tag_type_char = 'Mandarin::Type::Character'
tag_type_word = 'Mandarin::Type::Word/Phrase'

'''
Image setup

Fields: svg_an_si, svg_an_tr, svg_still_si, svg_still_tr, gif_si, gif_tr

The two sources are:
gifs: https://github.com/nmarley/chinese-char-animations
and
svgs: https://github.com/skishore/makemeahanzi

Filenames
For the gif link, images are in /images-large and filenames are [utf-8 hexadecimal]-large.gif
ex: 们 (utf-8: 20204 (decimal), 4eec (hex)) is 4eec-large.gif
For the svg link, images are in /svgs-still and /svgs and filenames are [utf-8 decimal]-still.svg and [utf-8 decimal].svg respectively
ex: 20204-still.svg and 20204.svg
'''
ch_hex = ''
ch_dec = ''
name_gif = f'imgs/chinese-char-animations-master/images-large/{ch_hex}-large.gif'
name_svg_an = f'imgs/makemeahanzi-master/svgs/{ch_dec}.svg'
name_svg_still = f'imgs/makemeahanzi-master/svgs-still/{ch_dec}-still.svg'


# function to get image files ready for Anki use
# returns values img fields will be populated with
def get_images(zh_input):
    img_fields = {'gif': [], 'svg_an': [], 'svg_still': []}
    
    for char in zh_input:
        ch_dec = ord(char)
        ch_hex = hex(ch_dec)[2:]

        # where the files can be found
        name_gif = f'imgs/chinese-char-animations-master/images-large/{ch_hex}-large.gif'
        name_svg_an = f'imgs/makemeahanzi-master/svgs/{ch_dec}.svg'
        name_svg_still = f'imgs/makemeahanzi-master/svgs-still/{ch_dec}-still.svg'
        og_filenames = {
            'gif': name_gif,
            'svg_an': name_svg_an,
            'svg_still': name_svg_still
        }

        # cca stands for chinese char animations, mmah stands for make me a hanzi
        # both are the names of the repos they come from
        new_filenames = {
            'gif': f'{char}_cca.gif',
            'svg_an': f'{char}_mmah_an.svg',
            'svg_still': f'{char}_mmah_still.svg'
        }

        for img_type, og_filename in og_filenames.items():
            try:
                new_filename = f'{new_filenames[img_type]}'
                # if image has not already been added to Anki,
                # copy image file from current location to media dir with new name 
                # they will be moved to Anki from the media dir
                if new_filename not in open('existing_media.txt', encoding='UTF-8').read():
                    # copy image to media dir where it will be held temporarily
                    shutil.copy(og_filename, f'media/{new_filename}')
                    # add it to the list of media already on Anki
                    with open("existing_media.txt", "a", encoding="UTF-8") as f:
                        f.write(new_filename + '\n')
                # add the image's filename to the Anki field
                img_fields[img_type].append(f'<img src="{new_filename}">')
            except Exception as e:
                print(f"File not found for {char}: {og_filename}")
                print(f"Error: {e}")
    
    # formatting filenames for Anki fields
    for img_type, char_list in img_fields.items():
        # in case there were missing fields (i.e. for words or phrases)
        if len(char_list) != len(zh_input):
            # wipe the whole field since a phrase with a missing character would be confusing
            img_fields[img_type] = ''
        else:
            img_fields[img_type] = ''.join(img_fields[img_type])

    return img_fields['gif'], img_fields['svg_an'], img_fields['svg_still']


# setting up text-to-speech
engine = pyttsx3.init()

# the default voice rate is 200 `engine.getProperty('rate')`
# this was a bit too fast, so I adjusted it to 135 which seems good so far
# might want to adjust again in the future
adjusted_voice_rate = 135
engine.setProperty('rate', adjusted_voice_rate)

# changing voice to Mandarin-speaking one
# see full list of voices with `for voice in engine.getProperty('voices'): print(voice)`
zh_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0'
engine.setProperty('voice', zh_voice_id)


# maybe add a tag to card if audio is from MSU or generated with TTS??
def get_audio(zh_input, pinyin_zh_input):
    filename = f"{pinyin_zh_input.replace(' ', '_')}.mp3"
    # look to see if the file has previously been added to Anki
    if filename in open('existing_media.txt', encoding='UTF-8').read():
        return f"[sound:{filename}]"
    # if this is a new file, find/generate it, add it to media folder, and add to existing_media.txt
    # first try to get audio file from MSU files
    f = open('pinyin_ids.json')
    pids = json.load(f)
    f.close()
    if pinyin_zh_input in pids:
            filename = 'msu_' + filename
            # pinyin_ids.json is imperfect and doesn't have all 6 IDs for every syllable
            # when all 6 are present, the 4th one is the one I want since I prefer that speaker
            num_ids = len(pids[pinyin_zh_input])
            i = min(num_ids, 4)
            audio_id = pids[pinyin_zh_input][i]
            url_template = f"https://tone.lib.msu.edu/tone/{audio_id}/PROXY_MP3/download"
            downloaded_audio = requests.get(url_template)
            with open('media/' + filename, 'wb') as f:
                f.write(downloaded_audio.content)
    # generate audio using pyttsx3
    else:
        filename = 'tts_' + filename
        engine.save_to_file(zh_input, 'media/' + filename)
        engine.runAndWait()
    # add filename to existing_media.txt
    with open("existing_media.txt", "a", encoding="UTF-8") as f:
        f.write(filename + '\n')
    return f"[sound:{filename}]"


# for getting from pinyin with tone marks to pinyin with numbers
# adapted from https://stackoverflow.com/questions/42854588/get-tone-number-from-pinyin
def to_tone_number(s):
    table = {0x304: ord('1'), 0x301: ord('2'), 0x30c: ord('3'),
         0x300: ord('4')}
    pin_split = pin.split(' ')
    for i, pin_syl in enumerate(pin_split):
        og_return = unicodedata.normalize('NFD', pin_syl).translate(table)
        temp = [*og_return]
        for index, char in enumerate(temp):
            if str(char).isnumeric():
                num = temp.pop(int(index))
                break
        temp.append(num)
        temp = ''.join(temp)
        pin_split[i] = temp
    return ' '.join(pin_split)
    

while True:
    # clear tags (initialize on first run)
    tags = set()
    tags.add(ver_num)

    # get character
    print("Enter character(s): ")
    ch = input()
    print(f"input is: \n{ch}")
    ch = ch.strip()
    #
    # do some checking to make sure input is using simplified characters
    #
    si = ch
    tr = converter.convert(si)
    # add simplified characters to list to tags
    for char in si:
        tags.add(pre_ch_si + char)
    # does traditional version exist? if so add tags
    if tr == si:
        tr = ""
        tr_exists = "No"
    else:
        tr_exists = "Yes"
        for char in tr:
            tags.add(pre_ch_tr + char)
    # add tag for if it's a character or word
    if len(si) > 1:
        tags.add(tag_type_word)
    else:
        tags.add(tag_type_char)

    # get pinyin
    # standard pinyin form, i.e. 'nǐ hǎo'
    pin = pinyin.get(si, delimiter=" ")
    print(f"Is the following pinyin correct: \n{pin}")
    print("y if correct, otherwise paste correct pinyin: ")
    response = input()
    if response != 'y':
        pin = response
        # getting numerical pinyin using function borrowed from other project
        pin_num = to_tone_number(pin)
        print(f"Auto-generated numerical pinyin is: {pin_num}")
        # removing the numbers from pin_num
        pin_toneless = ''.join([i for i in pin_num if not i.isnumeric()])
        print(f"Auto-generated toneless pinyin is: {pin_toneless}")
    else:
        pin_num = pinyin.get(si, format="numerical", delimiter=" ")
        pin_toneless = pinyin.get(si, format="strip", delimiter=" ")
    # add tags for pinyin syllables
    for syl in pin.split():
        tags.add(pre_pin_syl_std + syl)
    for syl in pin_num.split():
        tags.add(pre_pin_syl_num + syl)
    for syl in pin_toneless.split():
        tags.add(pre_pin_syl_raw + syl)
    # add tags for tones
    for char in pin_num:
        if char.isnumeric():
            tags.add(pre_pin_syl_tone + char)
    
    # character/word meaning
    full_def = pinyin.cedict.translate_word(si)
    full_def = '; '.join(full_def)
    print(f"Auto-generated full definition is: {full_def}")
    (print("Keep? y/n"))
    if input() != 'y':
        print("Enter your own full definition: ")
        full_def = input()
    
    # getting images
    # using function defined outside of loop
    gif_si, svg_an_si, svg_still_si = get_images(si)
    gif_tr, svg_an_tr, svg_still_tr = get_images(tr)

    # getting audio
    audio = get_audio(si, pin)
    
    # optional fields
    quick_def = ''
    lit_meaning = ''
    hint = ''
    examples = ''

    print("Add quick definition? n/input quick def now")
    response = input()
    if response != 'n':
        quick_def = response

    print("Use other optional fields? y/n")
    if input() == 'y':
        print("Add literal meaning? y/n")
        if input() == 'y':
            print("Input literal meaning: ")
            lit_meaning = input()
        print("Add hint? y/n")
        if input() == 'y':
            print("Input hint: ")
            hint = input()
        print("Add examples? y/n")
        if input() == 'y':
            print("Input examples: ")
            examples = input()

    # consolidate tags into string
    tags = ' '.join(tags)

    # add current card to list of cards
    row = [si, tr, tr_exists, pin, pin_num, pin_toneless, full_def, quick_def, lit_meaning, hint, examples, gif_si, gif_tr, svg_an_si, svg_an_tr, svg_still_si, svg_still_tr, audio, tags]
    
    # write current row to CSV
    with open('cards.csv', 'a', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(row)

    # Clearing variable values
    for i in range(len(row)):
        row[i] = ""

    # end loop here if user is done adding cards
    print("Add more cards? y/n")
    if input() == "n":
        break
