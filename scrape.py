#! /usr/bin/env python
# scrape.py
# David Prager Branner
# 20140918

"""Supply functions for studying Chinese Wikipedia pages."""

import urllib
import sys
import io
import traceback
import lxml.etree
parser = lxml.etree.HTMLParser(recover=False, encoding='utf-8')

def hexify(title):
    """Generate a hex string from kanji string, with percent prefixing."""
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
    api = 'https://zh.wikipedia.org/wiki/' + hexify(title)
    try:
        page = urllib.request.urlopen(api).read()
    except Exception as e:
        print(e)
    return page

def get_words(title):
    """Return list of dictionaries: words in tags marked data-noteta-code."""
    results = []
    page = fetch_page_html(title)
    try:
        # Earlier used:
        #     lxml.etree.parse(io.StringIO(page.decode()), parser)
        # got lxml.etree.XMLSyntaxError. Fixed with BytesIO.
        root = lxml.etree.parse(io.BytesIO(page), parser)
    except lxml.etree.XMLSyntaxError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        with open('problem_page_' + title + '.txt', 'wb') as f:
            f.write(page)
        sys.exit()
    if root:
        codes = root.xpath('//div[@data-noteta-code]')
    if codes:
        for code in [code.values()[-1].split(';') for code in codes]:
            d = {}
            for pair in code:
                if pair:
                    k, v = pair.strip(' ').split(':')
                    d[k] = v
            results.append(d)
    return results
