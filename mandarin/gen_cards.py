# automatically add handwritten image for writing cards
# maybe use https://github.com/chanind/hanzi-writer
# https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project might also be useful

import csv
import opencc
import pinyin
import pinyin.cedict

converter = opencc.OpenCC('s2t.json')

cards = []


# not sure what this was about
def create_new_row():
    row = []
    row = [1, 2, 3]
    return row


while True:
    # get character
    print("Enter character(s): ")
    ch = input()
    print(f"input is: \n{ch}")
    ch = ch.strip()
    #
    #
    # do some checking to make sure input is using simplified characters
    si = ch
    tr = converter.convert(si)
    tr_exists = "Yes"
    if tr == si:
        tr = ""
        tr_exists = "No"

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


    ##### Meaning #####
    # Try using cedict meaning and give user option to override this (like with pinyin)


    ##### Tags #####
    # for words, tag with component characters
    # for characters, tag with character itself
    # tag with pinyin syllables (for just characters?? or words too?)

    # add current card to list of cards
    row = [si, tr, tr_exists, pin, pin_num, pin_toneless, meaning, lit_meaning, hint, examples, stroke_order]
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