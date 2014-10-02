#! /usr/bin/env python
# crawl.py
# David Prager Branner
# 20141002, works

""""""
import utils as U
import scrape as S
import os

def main():
    # Get the collection of links. 
    filename = os.path.join('..', 'data', 'links', 'links_unscraped.txt')
    with open(filename, 'r') as f:
        links = f.read()
    links = links.split('\n')
    print('Retrieved {} unscraped links from file\n    {}'.
            format(len(links), filename))
    # If empty, collect newest links (ignore other matter). 
    #     http://en.wikipedia.org/wiki/Special:RecentChanges
    if links == ['']:
        print('No links found in file\n    {}'.format(filename))
        _, _, _, links = S.main('Special:RecentChanges')
        print('Retrieved {} links from "Special:RecentChanges".'.
                format(len(links)))
    print('links:', links)
    # If these have been done already, get random link.
    #     https://zh.wikipedia.org/wiki/Special:Random
    if not links:
        links = ['Special:Random']
        print('Turning to "Special:Random".')
    links = set(links)
    if '' in links:
        links.remove('')
    # Also get the list of done links.
    done_links_filename = os.path.join('..', 'data', 'links', 'done_links.txt')
    with open(done_links_filename, 'r') as f:
        done_links = f.read()
    done_links = set(done_links.split('\n'))
    if done_links == {''}:
        done_links = set()
    print('Retrieved {} done links from file\n    {}'.
            format(len(done_links), done_links_filename))
    try:
        links, done_links = scrape_links(links, done_links)
    except KeyboardInterrupt:
        print('We had KeyboardInterrupt; links: |{}|. Now cleaning up.'.
                format(len(links)))
    links = '\n'.join(links)
    with open(filename, 'w') as f:
        f.write(links)
    done_links = '\n'.join(done_links)
    with open(done_links_filename, 'w') as f:
        f.write(done_links)

def scrape_links(links, done_links=set()):
    while links:
        title = links.pop()
        print('Trying title {}'.format(title))
        # Ignore if title already done.
        if title in done_links:
            continue
        page, title, synonyms, links = S.main(title)
        print('''Data retrieved from title {}:'''
                '''\n    page-size: {}, synonyms:  {}, links:     {}'''.
                format(title, len(page), len(synonyms), len(links)))
        U.store_data(page, title, target_dir='html_new', tar=True)
        U.store_data(synonyms, title, target_dir='synonyms_new', tar=False)
        U.store_links(links)
        # Update done_links.
        done_links.add(title)
    return links, done_links

if __name__ == '__main__':
    main()
        