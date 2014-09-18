#! /usr/bin/env python
# scrape.py
# David Prager Branner
# 20140918

def hexify(title)"
    """Generate a hex string from kanji string, with percent prefixing."""
    # Timeit shows encode() to have same running time as bytes(str, 'utf-8')
    return ('%' + 
            '%'.join([hex(item)[2:].upper() for item in list(title.encode())]
           )
