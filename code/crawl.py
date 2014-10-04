#! /usr/bin/env python
# crawl.py
# David Prager Branner
# 20141004, works

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
    while True:
        try:
            scrape_links(title=None)
        except KeyboardInterrupt:
            print('''\nWe had KeyboardInterrupt in main(). ''')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            break

def get_unscraped_links(unscraped_links_filename):
    # Get the collection of links. 
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
    return links

def get_done_links(done_links_filename):
    with open(done_links_filename, 'r') as f:
        done_links = f.read()
    done_links = set(done_links.split('\n'))
    if done_links == {''}:
        done_links = set()
    print('Retrieved {} done links from {}'.
            format(len(done_links), done_links_filename))
    return done_links

def update_links(links, new_links, done_links, title):
    new_links -= set(title)
    new_links = new_links.difference(links).difference(done_links)
    links.update(new_links)
    # Update done_links.
    done_links.add(title)
    return links, new_links, done_links

def scrape_links(title=None,
        unscraped_links_filename=os.path.join(
            '..', 'data', 'links', 'links_unscraped.txt'), 
        done_links_filename=os.path.join(
            '..', 'data', 'links', 'done_links.txt')):
    start_time = time.time()
    links = get_unscraped_links(unscraped_links_filename)
    done_links = get_done_links(done_links_filename)
    syn_count = len(os.listdir(os.path.join('..', 'data', 'synonyms_new')))
    print('Found {} synonym-files at start of while-loop.\n'.format(syn_count))
    with open(unscraped_links_filename, 'a') as f, open(done_links_filename, 'a') as g:
        while links:
            title = links.pop()
            # Ignore if title already done.
            if title in done_links:
                continue
            try:
                page, title, synonyms, new_links = S.main(title)
            except KeyboardInterrupt:
                print('''\nWe met with KeyboardInterrupt; title: {}. '''.
                        format(title))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                break
            except TypeError:
                # TypeError: 'NoneType' object is not iterable
                # Usually because "HTTP Error 404: Not Found", so restore title.
                # But many of these are corrupt; do not restore for now.
#                links.add(title)
                print('    {}'.format(title))
                continue
            except Exception:
                print('\nWe met with Exception; title: {}.'.
                        format(title))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                print('\n')
                continue
            if synonyms:
                _ = U.store_data(
                        json.dumps(synonyms).encode(), title, 
                        target_dir='synonyms_new', tar=False)
                syn_count += len(synonyms)
            links, new_links, done_links = update_links(
                    links, new_links, done_links, title)
            print('T: {}; links: + {:>4} => {:>}; syn.: + {} => {}; {}'.
                    format(int(time.time() - start_time), len(new_links), 
                           len(links), len(synonyms), syn_count, title))
            # Uncomment the following line to save whole pages (compressed).
            # _ = U.store_data(page, title, target_dir='html_new', tar=True)
            f.write('n' + '\n'.join(new_links))
            f.flush()
            g.write('\n' + title)
            g.flush()
            time.sleep(1.2)
    return links, done_links

if __name__ == '__main__':
    main()