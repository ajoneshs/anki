# automatically add handwritten image for writing cards
# maybe use https://github.com/chanind/hanzi-writer
# https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project might also be useful

import csv

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
    # do some checking to make sure input is using simplified characters
    ch = ch.strip()
    trad_ch = #convert here

    # attempt to auto generate pinyin
    pinyin = #
    print(f"Is the following pinyin correct: {pinyin}")
    pinyin = input(pinyin)

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