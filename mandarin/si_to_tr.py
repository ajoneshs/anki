import opencc
converter = opencc.OpenCC('s2t.json')
print(converter.convert('汉字'))  # 漢字