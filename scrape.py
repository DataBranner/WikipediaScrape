#! /usr/bin/env python
# scrape.py
# David Prager Branner
# 20140918

import urllib
import io
import lxml.etree
parser = lxml.etree.HTMLParser()

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
    page = urllib.request.urlopen(api).read()
    return page

def get_words(title):
    page = fetch_page_html(title)
    root = lxml.etree.parse(io.StringIO(page.decode()), parser)
    # Note: Obama page returns empty but shouldn't - too long?
    codes = root.xpath('//div[@data-noteta-code]')
    ds = []
    if codes:
        for code in [code.values()[-1].split(';') for code in codes]:
            d = {}
            for pair in code:
                if pair:
                    k, v = pair.strip(' ').split(':')
                    d[k] = v
            ds.append(d)
    return ds
