#! /usr/bin/env python
# scrape.py
# David Prager Branner
# 20141019

"""Given a Chinese Wikipedia page-title, return its links and synonyms."""

# More modularized than scrape_old.py and ready to have interlanguage routine added.

import urllib
import sys
import re
import io
import traceback
import lxml.etree
import utils as U
import string
import urllib.parse as P
import os

def compose_api_req(title):
    return ('''http://zh.wikipedia.org/w/api.php?''' +
          '''action=query&''' +
          '''generator=allpages&''' +
          '''prop=info&''' +
          '''format=xml&''' +
          '''titles=''' + P.quote(title))

def fetch_page_api(title):
    api = compose_api_req(title)
    page = urllib.request.urlopen(api).read()
    return page

def fetch_page_html(title):
    """Construct URL for page using title."""
    # Decide if title needs to be hexified or not.
    chars = string.ascii_letters + string.digits + string.whitespace + '%:'
    if any(i not in chars for i in set(title)):
        title = P.quote(title)
    url = 'https://zh.wikipedia.org/wiki/' + title
    try:
        page = urllib.request.urlopen(url).read()
    except Exception as e:
        print(e)
        page = b''
    return page

def get_synonyms(page, title):
    """Return list of dictionaries: words in tags marked data-noteta-code."""
    # We want to see any errors, so parser recover = False.
    parser = lxml.etree.HTMLParser(recover=True)
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
                        # "中国大陆：食物及卫生局；台灣：食物及衞生局；香港：食物及衞生局",
                        # "zh:-hk:資料", "平方公里",
                        # "大陆、台湾：特斯拉；香港：忒斯拉；"
                        # "zh-sg:简讯:", "zh-sg:面子书:"
                        print('Error:\n    {}\n    {}'.format(e, pair))
                        # Keep a record of these
                        with open(os.path.join('..', 'data', 'malformed.txt'), 
                                'r') as f:
                            content = f.read()
                        with open(os.path.join('..', 'data', 'malformed.txt'), 
                                'w') as f:
                            f.write(content + '\n' + title +'\t' + pair)
                        continue
                    d[k] = v
            results.append(d)
    return results

def get_interwiki(interwiki='interlanguage-link interwiki-en'):
    pass

def get_links(page):
    """Return list of all links on page."""
    parser = lxml.etree.HTMLParser(recover=True)
    root = lxml.etree.parse(io.BytesIO(page), parser)
    if root:
        urls = get_urls(root)
        title = get_title(root)
        interwiki = get_interwiki()
    if urls:
        urls = clean_urls(urls)
    return set(urls), title

def get_urls(root):
    """Get all URLs in <a href...> elements."""
    return root.xpath('//a/@href')

def get_title(root):
    """Get title of this page from page itself."""
    title = root.xpath('//title')[0].text
    return title.replace(' - 维基百科，自由的百科全书', '')

def clean_urls(urls):
    """Remove undesireable URLs and clean further."""
    # Features: 
    #     url.find('action=') == -1:    Only links to content.
    #     re.search('^/wiki/', url):    Only relative URLs on the Chinese site.
    #     not re.search('\....$', url): Not files with three-char extensions.
    #     'redlink=1' not in url:       Only links not now known not to exist.
    urls = [P.unquote(re.sub('[&#].+$', r'', url)) for url in urls if
            url.find('action=') == -1 and
            re.search('^/wiki/', url) and
            not re.search('\....$', url) and
            'redlink=1' not in url]
    # Since all links are relative, delete initial /wiki/.
    urls = [url.replace('/wiki/', '')
            for url in urls 
            if url and
            '/' not in url and 
            'Special:' not in url and
            'Project:' not in url and
            'Help:' not in url and
            'Portal:' not in url and
            'Wikipedia:' not in url and 
            'File:' not in url and
            'User:' not in url and
            'Template:' not in url and
            'Wikipedia talk:' not in url and
            'Wikipedia_talk:' not in url and
            'User talk:' not in url and
            'User_talk:' not in url and
            'Category talk:' not in url and
            'Category_talk:' not in url and
            'Template talk:' not in url and
            'Template_talk:' not in url and
            'Talk:' not in url]
    return urls

def main(title):
    page = fetch_page_html(title)
    if page:
        links, title = get_links(page)
        synonyms = get_synonyms(page, title)
        return page, title, synonyms, links
