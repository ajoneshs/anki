# automatically add handwritten image for writing cards
# maybe use https://github.com/chanind/hanzi-writer
# https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project might also be useful

import csv
import opencc

converter = opencc.OpenCC('s2t.json')

count = 0
cards = []


def create_new_row():
    row = []
    row = [1, 2, 3]
    return row


while True:
    count += 1
    if count == 1:
        print("Welcome, would you like to add cards? y/n")
    
    print("Enter character(s): ")
    ch = input()
    print(f"input is: {ch}")
    #
    # do some checking to make sure input is using simplified characters
    #
    ch = ch.strip()
    trad_ch = converter.convert(ch)

    # attempt to auto generate pinyin
    # maybe this: https://pypi.org/project/pinyin/
    pinyin = #
    print(f"Is the following pinyin correct: {pinyin}")
    print("y if correct, otherwise paste correct pinyin: ")
    response = input(pinyin)
    if response != 'y':
        pinyin = response

    print("Add more cards? y/n")
    if input() == "n":
        break
    else: 
        row = create_new_row()
        cards.append(row)
    
    # end loop here if user is done adding cards
    print("Add more cards? y/n")
    if input() == "n":
        break

print(cards)