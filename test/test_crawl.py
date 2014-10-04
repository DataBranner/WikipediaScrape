#! /usr/bin/env python
# test_crawl.py
# 20141004

import sys
sys.path.append('code')
import crawl as C
import random

def generate_random_set(n):
    return {random.random() for i in range(n)}

def test_update_links_01():
    links = {i for i in range(10)}
    new_links = {i for i in range(10, 13)}
    done_links = set()
    links, new_links, done_links = C.update_links(
            links, new_links, done_links, title='')
    assert links == {i for i in range(13)}
    assert new_links == {i for i in range(10, 13)}
    assert done_links == set()

def test_update_links_02():
    links = {i for i in range(10)}
    new_links = {i for i in range(10, 13)}
    done_links = {i for i in range(5, 11)}
    links, new_links, done_links = C.update_links(
            links, new_links, done_links, title='')
    temp = {i for i in range(13)}
    temp.remove(10)
    print('links:', links)
    print('new_links:', new_links)
    print('temp:', temp)
    print('done_links:', done_links)
    assert links == temp
    assert new_links == {i for i in range(11, 13)}
    assert done_links == {i for i in range(5, 11)}

def test_update_links_03():
    links = {i for i in range(10)}
    new_links = {i for i in range(10, 23)}
    done_links = {i for i in range(5, 15)}
    links, new_links, done_links = C.update_links(
            links, new_links, done_links, title='')
    temp = {i for i in range(10)}
    temp.update({i for i in range(15, 23)})
    print('links:', links)
    print('new_links:', new_links)
    print('temp:', temp)
    print('done_links:', done_links)
    assert links == temp
    assert new_links == {i for i in range(15, 23)}
    assert done_links == {i for i in range(5, 15)}

def test_update_links_04():
    links = {i for i in range(10)}
    new_links = {i for i in range(10, 23)}
    done_links = {i for i in range(5, 15)}
    links, new_links, done_links = C.update_links(
            links, new_links, done_links, title=18)
    temp = {i for i in range(10)}
    temp.update({i for i in range(15, 23)})
    temp.remove(18)
    print('links:', links)
    print('new_links:', new_links)
    print('temp:', temp)
    print('done_links:', done_links)
    assert links == temp
    temp2 = {i for i in range(15, 23)}
    temp2.remove(18)
    assert new_links == temp2
    temp3 = {i for i in range(5, 15)}
    temp3.add(18)
    assert done_links == temp3

