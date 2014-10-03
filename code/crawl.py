#! /usr/bin/env python
# crawl.py
# David Prager Branner
# 20141002, works

""""""
import utils as U
import scrape as S
import os
import time
import urllib.parse as P
import traceback
import sys
import json

def main():
    break_loop = False
    while not break_loop:
        # Get the collection of links. 
        unscraped_links_filename = os.path.join(
                '..', 'data', 'links', 'links_unscraped.txt')
        with open(unscraped_links_filename, 'r') as f:
            links = f.read()
        links = links.split('\n')
        print('Retrieved {} unscraped links from {}'.
                format(len(links), unscraped_links_filename))
        # If empty, collect newest links (ignore other matter). 
        #     http://en.wikipedia.org/wiki/Special:RecentChanges
        if links == ['']:
            print('No links found in file\n    {}'.
                    format(unscraped_links_filename))
            _, _, _, links = S.main('Special:RecentChanges')
            print('Retrieved {} links from "Special:RecentChanges".'.
                    format(len(links)))
        # If these have been done already, get random link.
        #     https://zh.wikipedia.org/wiki/Special:Random
        if not links:
            links = ['Special:Random']
            print('Turning to "Special:Random".')
        links = set(links)
        if '' in links:
            links.remove('')
        # Also get the list of done links.
        done_links_filename = os.path.join(
                '..', 'data', 'links', 'done_links.txt')
        with open(done_links_filename, 'r') as f:
            done_links = f.read()
        done_links = set(done_links.split('\n'))
        if done_links == {''}:
            done_links = set()
        print('Retrieved {} done links from {}'.
                format(len(done_links), done_links_filename))
        while links:
            try:
                links, done_links = scrape_links(links, done_links)
            except KeyboardInterrupt:
                print('''\nWe had KeyboardInterrupt; links: |{}|. '''
                      '''Now cleaning up.'''.format(len(links)))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                break_loop = True
                break
            except TypeError:
                print('\nWe had TypeError; links: |{}|. Now cleaning up.'.
                        format(len(links)))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                break_loop = True
                break
            clean_up(
                    unscraped_links_filename, links, done_links_filename, 
                    done_links)
        clean_up(unscraped_links_filename, links, done_links_filename, 
                done_links)

def clean_up(unscraped_links_filename, links, done_links_filename, done_links):
    """Clean up after exception."""
    print('''Links now in "{}": {}\n'''
          '''Links now in "{}": {}'''.
          format(unscraped_links_filename, len(links), 
                 done_links_filename, len(done_links)))
    links = '\n'.join(links)
    with open(unscraped_links_filename, 'w') as f:
        f.write(links)
    done_links = '\n'.join(done_links)
    with open(done_links_filename, 'w') as f:
        f.write(done_links)

def scrape_links(links, done_links):
    start_time = time.time()
    while links and time.time() - start_time < 100:
        title = links.pop()
        # Ignore if title already done.
        if title in done_links:
            continue
        page, title, synonyms, new_links = S.main(title)
        links.update(set(new_links))
        if title in links:
            links.remove(title)
        print('Time: {}; Links left: {}; synonyms: {}; new links: {}; {}'.
                format(int(time.time() - start_time), len(links), 
                       len(synonyms), len(new_links), title))
        # Uncomment the following line to save whole pages (compressed).
        # _ = U.store_data(page, title, target_dir='html_new', tar=True)
        if synonyms:
            _ = U.store_data(
                    json.dumps(synonyms).encode(), title, 
                    target_dir='synonyms_new', tar=False)
        # Update done_links.
        done_links.add(title)
        time.sleep(2)
    print('Time: {} seconds.'.format(int(time.time() - start_time)))
    return new_links, done_links

if __name__ == '__main__':
    main()
        