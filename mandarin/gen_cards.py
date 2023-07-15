# automatically add handwritten image for writing cards
# maybe use https://github.com/chanind/hanzi-writer

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
    else:
        print("Add more cards? y/n")
    
    if input() == "n":
        break
    else: 
        row = create_new_row()
        cards.append(row)

print(cards)