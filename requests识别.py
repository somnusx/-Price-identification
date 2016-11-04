import requests
from lxml import etree
from PIL import Image, ImageEnhance, ImageFilter
import io
import re
import os
from pytesser import *


url = 'http://www.newegg.cn/Product/A28-800-6TM-26.htm'
urls = set()
urls.add(url)


def res(url):
    r = requests.get(url).text
    aas = re.findall('http://www.newegg.cn/Product.+?\=1',r)
    for aa in aas:
        if aa in urls:
            continue
        else:
            urls.add(aa)
            res(aa)

res(url)
for i in urls:
    
    r = requests.get(i).text

    html = etree.HTML(r)

    name = html.xpath('//*[@id="tab1"]/div[1]/div[2]/div[2]/ul[1]/li[2]/div[2]/text()')
    price = html.xpath('//*[@id="priceValue"]/span/strong/img/@src')

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
    if price:        
        rs = requests.get(price[-1]).content
        with open('o.png','wb') as code:
            code.write(rs)
        #nameimage = io.BytesIO(rs)
        nameimage = 'o.png'
        im = Image.open(nameimage)

        imgry = im.convert('L')

        out = imgry.point(table, '1')

        text = image_to_string(out)

        text = text.strip()
        text = text.upper()

        for r in rep:
            price = text.replace(r, rep[r])

        print(name[0] + '  =  ' + price)




