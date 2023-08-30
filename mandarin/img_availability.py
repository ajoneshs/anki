# source for data: https://github.com/ruddfawcett/hanziDB.csv/blob/master/data/hanziDB.csv

row_num = 0
with open('hanziDB.csv', encoding='utf-8') as hanzi:
    for row in hanzi:
        row_num += 1
        if row_num > 300:
            break
        print(row)