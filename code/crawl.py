#! /usr/bin/env python
# crawl.py
# David Prager Branner
# 20141020

"""Crawl the Chinese subdomain of Wikipedia; collect links, synonym metadata."""

# To-do: Links containing "redlink=1" link to pages that do not yet exist. 
# Are we sure they are not being scraped?

# Do logging of errors.

# Add all data to .gitignore — transfer by sftp.

# Implement interlanguage links.

# Should main loop's call of scrape_links be in try-block?

import utils as U
import scrape as S
import os
import time
import urllib.parse as P
import traceback
import sys
import json

def main(time_before_new_changed=300):
    """Maintain a timed but endless loop that runs the main scraping program."""
    unscraped_links_filename = os.path.join(
            '..', 'data', 'links', 'links_unscraped.txt')
    done_links_filename = os.path.join(
            '..', 'data', 'links', 'done_links.txt')
    while True:
        # Use back-up timer here. Function scrape_links() has its own, but we 
        # need one here lest too few new links are available when we scrape and
        # we end up scraping Special:RecentChanges too often. The same 
        # timing is used here as in scrape_links().
        start_time = time.time()
        if input('Proceed? (require "yes"): ') != 'yes':
            print('Exiting.')
            break
        links, done_links = scrape_links(time_before_new_changed)
        # We always save the current scraped and unscraped links now.
        with open(unscraped_links_filename, 'w') as f:
            f.write('\n'.join(links))
        with open(done_links_filename, 'w') as f:
            f.write('\n'.join(done_links))
        print('Links saved in main loop.')
        while time.time() < start_time + time_before_new_changed:
            time.sleep(1)
        link = get_recent_changes(links, done_links)
        links = get_random_link(links)
        print('Continuing main loop.')

def get_unscraped_links(unscraped_links_filename, done_links):
    """Try three different means to get links to work with."""
    # Get the collection of links. 
    with open(unscraped_links_filename, 'r') as f:
        links = f.read()
    links = set(links.split('\n'))
    print('Retrieved {} unscraped links from {}'.
            format(len(links), unscraped_links_filename))
    # If empty, collect newest links (ignore other matter). 
    #     http://en.wikipedia.org/wiki/Special:RecentChanges
    if links == set():
        print('No links found in file\n    {}'.
                format(unscraped_links_filename))
        links = get_recent_changes(links, done_links)
        print('Retrieved {} links from "Special:RecentChanges".'.
                format(len(links)))
    # If these have all been done already, get random link.
    links = get_random_link(links)
    if '' in links:
        links.remove('')
    return links

def get_recent_changes(links, done_links):
    """Scrape links on the Special:RecentChanges page."""
    _, _, _, recent_links = S.main('Special:RecentChanges')
    starting_recent_links_num = len(recent_links)
#    recent_links = recent_links.difference(done_links) # Bad! What if updated?
    recent_links = recent_links.difference(links)
    links.update(recent_links)
    len(recent_links)
    print('Retrieved {} links from "Special:RecentChanges"; {} of which new.'.
            format(starting_recent_links_num, len(recent_links)))
    return links

def get_random_link(links):
    # Source: https://zh.wikipedia.org/wiki/Special:Random
    if links == set():
        links = {'Special:Random'}
        print('Turning to "Special:Random".')
    return links

def get_done_links(done_links_filename):
    """Retrieve the list of links already scraped."""
    with open(done_links_filename, 'r') as f:
        done_links = f.read()
    done_links = set(done_links.split('\n'))
    if done_links == {''}:
        done_links = set()
    print('Retrieved {} done links from {}'.
            format(len(done_links), done_links_filename))
    return done_links

def update_links(links, new_links, done_links, title):
    """Update the various sets of links."""
    links.discard(title)
    new_links.discard(title)
    new_links = new_links.difference(links)
    new_links = new_links.difference(done_links)
    links.update(new_links)
    # Update done_links.
    if title:
        done_links.add(title)
    return links, new_links, done_links

def scrape_links(time_before_new_changed, title=None, links=None,
        unscraped_links_filename=os.path.join(
            '..', 'data', 'links', 'links_unscraped.txt'), 
        done_links_filename=os.path.join(
            '..', 'data', 'links', 'done_links.txt')):
    """Scrape links from pages on candidate URLs and retrieve any synonyms."""
    start_time = time.time()
    done_links = get_done_links(done_links_filename)
    if links == None:
        links = get_unscraped_links(unscraped_links_filename, done_links)
    syn_count = len(os.listdir(os.path.join('..', 'data', 'synonyms_new')))
    print('Found {} synonym-files at start of while-loop.\n'.format(syn_count))
    while links:
        if time.time() > start_time + time_before_new_changed:
            print('Time {} seconds exceeded; getting new changed links.'.
                    format(time_before_new_changed))
            links = get_recent_changes(links, done_links)
            start_time = time.time()
        title = links.pop()
        # Ignore if title already done.
        if title in done_links:
            print('title already in links:', title in done_links)
            continue
        with open(done_links_filename, 'a') as f:
            f.write('\n' + title)
        try:
            page, _, synonyms, new_links = S.main(title)
        except KeyboardInterrupt:
            print('''\nWe met with KeyboardInterrupt; title: {}. '''.
                    format(title))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return links, done_links
        except TypeError:
            # TypeError: 'NoneType' object is not iterable
            # Usually because "HTTP Error 404: Not Found", so restore title.
            # But temporarily we are leaving titles unrestored, as we think
            # some of these were previously unfiltered `redlink=1" cases.
#            links.add(title)
            try:
                done_links.remove(title)
            except KeyError:
                pass
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
            syn_count = len(
                    os.listdir(os.path.join('..', 'data', 'synonyms_new')))
        links, new_links, done_links = update_links(
                links, new_links, done_links, title)
        print('''T: {}; links: + {:>3} => {:>}; done: {} ({}%); '''
              '''syn: + {} => {} ({}%);\n    {}'''.
                format(int(time.time() - start_time), len(new_links), 
                    len(links), len(done_links), 
                    round(
                        100 * len(done_links) / 
                        (len(done_links) + len(links)), 1), 
                    len(synonyms), syn_count, 
                    round(100 * syn_count / len(done_links), 1), 
                    title))
        # Uncomment the following line to save whole pages (compressed).
        # _ = U.store_data(page, title, target_dir='html_new', tar=True)
#         # Write the whole of "links": "title" removed, "new_links" added.
#         try:
#             with open(unscraped_links_filename, 'w') as f:
#                 f.write('\n'.join(links))
#         except KeyboardInterrupt:
#             print('''\nWe met with KeyboardInterrupt; title: {}. '''.
#                     format(title))
#             exc_type, exc_value, exc_traceback = sys.exc_info()
#             traceback.print_exception(exc_type, exc_value, exc_traceback)
#             return links, done_links
#     return links, done_links

if __name__ == '__main__':
    main()
