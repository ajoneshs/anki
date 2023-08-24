import pinyin, pinyin.cedict

print(pinyin.get('你好'))

print(pinyin.get('你好', format="numerical"))

print(pinyin.get('你好', format="numerical", delimiter=" "))

print(pinyin.get('你好', format="strip", delimiter=" "))

print(pinyin.cedict.translate_word('你'))

print(pinyin.cedict.translate_word('随机胡言乱语'))

(print("-------"))
non_existent_def = pinyin.cedict.translate_word('随机胡言乱语')
print(non_existent_def)
print(type(non_existent_def))

print("---------------")
shui = '水'
print(pinyin.cedict.translate_word(shui))