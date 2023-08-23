import opencc
converter = opencc.OpenCC('s2t.json')
men_si = "们"
print(converter.convert('们'))  # 漢字
print(converter.convert('們'))

# example without traditional equivalent
ni = "你"
print(converter.convert(ni))