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
    start_time = time.time()
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
    while True:
        try:
            links, done_links = scrape_links(
                    links, done_links, unscraped_links_filename,
                    done_links_filename, start_time)
        except KeyboardInterrupt:
            print('''\nWe had KeyboardInterrupt; links: |{}|. '''.
                    format(len(links)))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            break

def scrape_links(
    links, done_links, unscraped_links_filename, done_links_filename, 
    start_time):
    syn_count = len(os.listdir(os.path.join('..', 'data', 'synonyms_new')))
    print('Found {} synonym-files at start of while-loop.\n'.format(syn_count))
    with open(unscraped_links_filename, 'a') as f, open(done_links_filename, 'a') as g:
        while links:
            old_link_length = len(links)
            title = links.pop()
            if len(links) == old_link_length:
                print('len(links) == old_link_length: {}'.format(len(links)))
                sys.exit()
            # Ignore if title already done.
            if title in done_links:
                continue
            try:
                page, title, synonyms, new_links = S.main(title)
            except KeyboardInterrupt:
                print('''\nWe met with KeyboardInterrupt; links: |{}|. '''.
                        format(len(links)))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                break
            except Exception:
                print('\nWe met with Exception; links: |{}|.'.
                        format(len(links)))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                print('\n')
            syn_count += len(synonyms)
            new_links = new_links - links - set(title)
            links.update(new_links)
            print('T: {}; links: + {:>4} => {:>}; syn.: + {} => {}; {}'.
                    format(int(time.time() - start_time), len(new_links), 
                           len(links), len(synonyms), syn_count, title))
            # Uncomment the following line to save whole pages (compressed).
            # _ = U.store_data(page, title, target_dir='html_new', tar=True)
            if synonyms:
                _ = U.store_data(
                        json.dumps(synonyms).encode(), title, 
                        target_dir='synonyms_new', tar=False)
            # Update done_links.
            done_links.add(title)
            f.write('\n'.join(new_links))
            f.flush()
            g.write('\n' + title)
            g.flush()
            time.sleep(2)
    return links, done_links

if __name__ == '__main__':
    main()