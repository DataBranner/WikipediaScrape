#! /usr/bin/env python
# scrape.py
# David Prager Branner
# 20140918

"""Supply functions for studying Chinese Wikipedia pages."""

import urllib
import sys
import re
import io
import traceback
import lxml.etree

def hexify(title):
    """Generate a hex string from kanji string, with percent-prefixing."""
    # Timeit shows encode() to have same running time as bytes(str, 'utf-8')
    return ('%' +
            '%'.join([hex(item)[2:].upper() for item in list(title.encode())]
           ))

def compose_api_req(title):
    return ('''http://zh.wikipedia.org/w/api.php?''' +
          '''action=query&''' +
          '''generator=allpages&''' +
          '''prop=info&''' +
          '''format=xml&''' +
          '''titles=''' + hexify(title))

def fetch_page_api(title):
    api = compose_api_req(title)
    page = urllib.request.urlopen(api).read()
    return page

def fetch_page_html(title):
    """Construct URL for page using title."""
    url = 'https://zh.wikipedia.org/wiki/' + hexify(title)
    try:
        page = urllib.request.urlopen(url).read()
    except Exception as e:
        print(e)
        page = b''
    return page

def get_words(page):
    """Return list of dictionaries: words in tags marked data-noteta-code."""
    # We want to see any errors, so parser recover = False.
    parser = lxml.etree.HTMLParser(recover=False)
    results = []
    root = None
    try:
        # Earlier used:
        #     lxml.etree.parse(io.StringIO(page.decode()), parser)
        # got lxml.etree.XMLSyntaxError. Fixed with BytesIO.
        root = lxml.etree.parse(io.BytesIO(page), parser)
    except lxml.etree.XMLSyntaxError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    if root:
        divs = root.xpath('//div[@data-noteta-code]')
    else:
        # Retrying with recover=True
        print('Retrying with recover=True')
        parser = lxml.etree.HTMLParser(recover=True)
        root = lxml.etree.parse(io.BytesIO(page), parser)
        if root:
            divs = root.xpath('//div[@data-noteta-code]')
    if divs:
        # Typical div.values() item is a string:
        #     'zh-cn:艾波克; zh-tw:艾巴; zh-hk:天啟;'
        for code in [div.values()[-1].split(';') for div in divs]:
            d = {}
            for pair in code:
                if pair:
                    try:
                        k, v = pair.lstrip(' ').split(':')
                    except ValueError as e:
                        # One error found here was "zh-cn:地址栏zh-tw:網址列".
                        # Can we divide on the known keys if error?
                        # Another error: "裁准". Not divisible.
                        # Other errors: "月台", "恒生", "琼", "平台", "入伙",
                        # "卡里", "格里", "特里", "范冰", "荃灣行人天橋網絡",
                        # "網絡", "啓"
                        # "中国大陆：昂山素季；台灣：翁山蘇姬；香港：昂山素姬",
                        # "中国大陆：密集阵；台灣：方陣；香港：方陣",
                        # "中国大陆：圣迭戈；台灣：聖地牙哥；香港：聖地牙哥",
                        # "zh:-hk:資料", "平方公里",
                        # "大陆、台湾：特斯拉；香港：忒斯拉；"
                        # "zh-sg:简讯:", "zh-sg:面子书:"
                        print('Error:\n    {}\n    {}'.format(e, pair))
                        continue
                    d[k] = v
            results.append(d)
    return results

def get_links(page):
    """Return list of all links on page."""
    parser = lxml.etree.HTMLParser(recover=True)
    root = lxml.etree.parse(io.BytesIO(page), parser)
    if root:
        urls = root.xpath('//a/@href')
    if urls:
        urls = [re.sub('[&#].+$', r'', item) for item in urls if
                item.find('action=') == -1 and
               re.search('^/wiki/', item) and
               not re.search('\....$', item)]
    return urls

def main(title):
    page = fetch_page_html(title)
    if page:
        words = get_words(page)
        links = get_links(page)
        return words, links
