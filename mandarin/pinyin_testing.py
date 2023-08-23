import pinyin, pinyin.cedict

print(pinyin.get('你好'))

print(pinyin.get('你好', format="numerical"))

print(pinyin.get('你好', format="numerical", delimiter=" "))

print(pinyin.get('你好', format="strip", delimiter=" "))

print(pinyin.cedict.translate_word('你'))