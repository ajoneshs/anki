# code is for testing cedict to look for way to auto generate short definition

import pinyin, pinyin.cedict

shui = '水'
men = '们'
ni = '你'
hao = '好'

print(pinyin.cedict.translate_word(shui))
print(pinyin.cedict.translate_word(men))
print(pinyin.cedict.translate_word(ni))
print(pinyin.cedict.translate_word(hao))