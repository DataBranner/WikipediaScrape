#! /usr/bin/env python
# utils.py
# David Prager Branner
# 20141002, works

import datetime
import sys
import time
import os
import tarfile
import traceback

"""Provide utilities for use with saving scraped data."""

def hexify(title):
    """Generate a hex string from kanji string, with percent-prefixing."""
    # Timeit shows encode() to have same running time as bytes(str, 'utf-8')
    return ('%' +
            '%'.join([hex(item)[2:].upper() for item in list(title.encode())]
           ))

def construct_date(date_and_time=None):
    """Construct a time-and-date string for appending to a filename."""
    if not date_and_time:
        date_and_time = datetime.datetime.today()
    date_and_time = date_and_time.strftime('%Y%m%d-%H%M')
    return date_and_time

def convert_from_unixtime(unixtime, whole=True):
    """Convert Unix time to human-readable string."""
    if not whole:
        # Date only, no time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d')
    else:
        # Both date and time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d-%H%M')
    return date

def open_directory(path):
    """Get list of files in a given directory."""
    file_list = glob.glob(path+'*')
    return file_list

def store_links(new_links):
    """Add `links` to contents of existing links file and re-save."""
    start_time = time.time()
    if not len(new_links):
        return 0
    filename = os.path.join('..', 'data', 'links', 'links_unscraped.txt')
    with open(filename, 'r') as f:
        links = f.read()
    links = set(links.split('\n'))
    links.update(new_links)
    links = '\n'.join(list(links))
    with open(filename, 'w') as f:
        f.write(links)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed in handling links: {} seconds.'
            .format(total_time))

def store_data(data, title, target_dir='html_new', tar=True):
    """Store `data` in `target_dir`, compressed if so requested."""
    if not len(data):
        return 0
    start_time = time.time()
    target_dir = os.path.join('..', 'data', target_dir)
    # Make sure target_dir exists in .. or create it.
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print('Created directory {}'.format('target_dir'), end='\n\n')
    # Save data to file "temp".
    temp_filename = os.path.join(target_dir, title)
    with open(temp_filename, 'wb') as f:
        f.write(data)
    if not tar:
        return 'uncompressed'
    # Create filename for compressed `data`.
    filename = os.path.join(
            target_dir, title + '_' + construct_date() + '.tar.bz2')
    print(filename)
    # Compress `data` and save into `target_dir`.
    try:
        with tarfile.open(filename, 'w:bz2') as f:
            f.add(temp_filename)
            print('\nData of cardinality {} saved, compressed to\n    "{}".'.
                    format(len(data), filename), end='\n\n')
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed in tarring: {} seconds.'.format(total_time))
    return 'compressed'

#def untar_directory(dir_name=None, check_db=True, db='qqq'):
#    """Extract all archives in compressed/ into temporary/."""
#    start_time = time.time()
#    connection = sqlite3.connect(os.path.join('../', db))
#    home_dir = os.getcwd()
#    # In order not to repeat decompressions unnecessarily, get list of all
#    # archives already inserted into database.
#    with connection:
#        cursor = connection.cursor()
#        cursor_output = cursor.execute(
#                '''SELECT directory_name FROM downloads_inserted''')
#        archives_done = [item[0].split('/')[-1]
#                 for item in cursor_output.fetchall()]
#    os.chdir('../data/compressed')
#    # Do the whole procedure below for any existing directories in downloads.
#    # First find the directories.
#    if not dir_name:
#        archives = open_directory('downloads_')
#    else:
#        archives = [dir_name]
#    number_archives = len(archives)
#    print('{} directories available to extract.'.
#            format(number_archives), end='\n\n')
#    # Make sure ../compressed exists or create it.
#    if not os.path.exists('../temporary'):
#        os.makedirs('../temporary')
#        print('Created directory temporary', end='\n\n')
#    # Now uncompress each directory.
#    archives.sort()
#    for archive in archives:
#        archive_short = archive.split('.')[0]
#    # If check_db, then first check whether this archive has already
#    # been processed.
#        if check_db and archive_short in archives_done:
#            number_archives -= 1
#            continue
#        # Copy and then uncompress each file, using context manager.
#        with tarfile.open('../compressed/' + archive , 'r:bz2') as f:
#            f.extractall('../temporary/')
#        print('Decompressed directory\n    "{}".'.
#            format(archive), end='\n\n')
#    print('In total, {} archives extracted out of {}.'.
#            format(number_archives, len(archives)))
#    # When finished, return to directory where we started.
#    os.chdir(home_dir)
#    end_time = time.time()
#    total_time = round(end_time - start_time)
#    print('Total time elapsed in tarring: {} seconds; '
#            '{} seconds per directory on avg.\n'.
#            format(total_time, round(total_time/len(archives), 1)))
