# automatically add handwritten image for writing cards
# maybe use https://github.com/chanind/hanzi-writer
# https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project might also be useful


####### Audio #######
# Look into adding audio
#########################
#########################


import csv
import opencc
import pinyin
import pinyin.cedict

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
'''
pre_ch_si = 'Mandarin::Characters::Simplified::'
pre_ch_tr = 'Mandarin::Characters::Traditional::'
pre_pin_syl_std = 'Mandarin::Pinyin::Syllables::Standard::'
pre_pin_syl_num = 'Mandarin::Pinyin::Syllables::Numerical::'
pre_pin_syl_raw = 'Mandarin::Pinyin::Syllables::Toneless::'
pre_pin_syl_tone = 'Mandarin::Pinyin::Tones::'


# not sure what this was about
def create_new_row():
    row = []
    row = [1, 2, 3]
    return row


while True:
    # clear tags (initialize on first run)
    tags = set()

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

    # get pinyin
    # standard pinyin form, i.e. 'nǐ hǎo'
    pin = pinyin.get(si, delimiter=" ")
    print(f"Is the following pinyin correct: \n{pin}")
    print("y if correct, otherwise paste correct pinyin: ")
    response = input()
    if response != 'y':
        pin = response
        # have to manually enter numerical and toneless pinyin
        # eventually automate this
        print("Input numerical pinyin (i.e. ni3 hao3): ")
        pin_num = input()
        print("Input toneless pinyin (i.e. ni hao): ")
        pin_toneless = input()
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
    meaning = pinyin.cedict.translate_word(si)
    meaning = '; '.join(meaning)
    print(f"Auto-generated meaning is: {meaning}")
    (print("Keep? y/n"))
    if input() != 'y':
        print("Enter your own meaning: ")
        meaning = input()
    
    # optional fields
    lit_meaning = ''
    hint = ''
    examples = ''

    print("Use optional fields? y/n")
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
    

    ###### Placeholders ######
    stroke_order = ""



    # consolidate tags into string
    tags = ' '.join(tags)

    # add current card to list of cards
    row = [si, tr, tr_exists, pin, pin_num, pin_toneless, meaning, lit_meaning, hint, examples, stroke_order, tags]
    cards.append(row)

    # Clearing variable values
    # var names come from fields for Anki note:
    # field = ["Simplified", "Traditional", "Pinyin", "Pinyin (numerical)", "Pinyin (toneless)", "Meaning", "Literal meaning", "Is there traditional?", "Hint", "Examples", "Stroke order"]
    all_vars = [si, tr, tr_exists, pin, pin_num, pin_toneless, meaning, lit_meaning, hint, examples, stroke_order]
    for i in range(len(all_vars)):
        all_vars[i] = ""

    # end loop here if user is done adding cards
    print("Add more cards? y/n")
    if input() == "n":
        break

print(cards)


'''

# var names come from fields for Anki note:
# field = ["Simplified", "Traditional", "Is there traditional?", "Pinyin", "Pinyin (numerical)", "Pinyin (toneless)", "Meaning", "Literal meaning", "Hint", "Examples", "Stroke order"]
all_vars = [si, tr, pin, pin_num, pin_toneless, meaning, lit_meaning, tr_exists, hint, examples, stroke_order]

for i in range(len(all_vars)):
    all_vars[i] = ""

#
#
# from /geoguessr/area_codes/gen_cards.py
#
#

# generate csv file to import into Anki
with open('data/area_code_cards.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    field = ["Simplified", "Traditional", "Is there traditional?", "Pinyin", "Pinyin (numerical)", "Pinyin (toneless)", "Meaning", "Literal meaning", "Hint", "Examples", "Stroke order"]
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