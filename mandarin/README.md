After running gen_cards.py, move contents of temp_media_storage to C:\Users\senoj\AppData\Roaming\Anki2\User 1\collection.media


## Stroke order images
Currently using two sources for images on cards:
https://github.com/nmarley/chinese-char-animations
and
https://github.com/skishore/makemeahanzi

The first has GIFs of characters being written. The second has animated SVGs of the characters being written and an SVG with ordered strokes. Anki will play animated SVGs, but they do not loop, so you only see the image once using the animated SVG, hence why the GIFs are also being used.

Other resources include:
* https://github.com/chanind/hanzi-writer
* https://commons.wikimedia.org/wiki/Commons:Stroke_Order_Project might also be useful
    * #url_template = f"https://commons.wikimedia.org/wiki/File:{char}-bw.png"