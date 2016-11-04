import requests
from lxml import etree
from PIL import Image, ImageEnhance, ImageFilter
import io
from pytesser import *

url = 'http://www.newegg.cn/Product/S5K-5C3-05D_320.htm'
html = etree.HTML(requests.get(url).text)

name = html.xpath('//*[@id="tab1"]/div[1]/div[2]/div[2]/ul[1]/li[2]/div[2]/text()')
price = html.xpath('//*[@id="priceValue"]/span/strong/img/@src')
print(price)
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2',
       'S': '8'
       }

nameimage = io.BytesIO(requests.get(price[0]).content)
im = Image.open(nameimage)

imgry = im.convert('L')

out = imgry.point(table, '1')

text = image_to_string(out)

text = text.strip()
text = text.upper();

for r in rep:
    price = text.replace(r, rep[r])

print(name[0] + '  =  ' + price)



