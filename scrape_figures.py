# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from json_operations import *

PREFIX = 'https://ru.wikisource.org'
URL_OLD = 'https://ru.wikisource.org/wiki/Ветхий_завет'
FIGURES_OLD_CANON = 'figures_old_canon.json'
BOOK_NAMES_OLD_CANON = 'book_names_old_canon.json'


def scrape_old_canon(prefix, url):
    figures = dict()
    book_names = dict()

    soup = BeautifulSoup(requests.get(url).content)

    table = soup.find('table', {'class': 'standard'})

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')

        en_book_name = cells[5].text.strip()
        ru_book_name = cells[0].find_all('a')[0].text.strip()
        book_url = prefix + cells[0].find_all('a')[0].get('href')

        book_names[en_book_name] = ru_book_name
        figures[en_book_name] = scrape_book(en_book_name, book_url)

    return book_names, figures


def scrape_book(en_book_name, url):
    print 'Scraping', en_book_name
    verses_per_chapter = list()

    soup = BeautifulSoup(requests.get(url).content)

    verses = [map(int, item.get('id').split(':')) for item in soup.find_all('span', {'style': 'color:#00F;'})]

    previous_chapter_num = 1
    last_verse_num = None
    for curr_chapter_num, curr_verse_num in verses:
        if curr_chapter_num != previous_chapter_num:
            verses_per_chapter.append(last_verse_num)
            previous_chapter_num, last_verse_num = curr_chapter_num, curr_verse_num
        else:
            last_verse_num = curr_verse_num

    verses_per_chapter.append(verses[-1][1])
    return verses_per_chapter


if __name__ == '__main__':
    # names, figs = scrape_old_canon(PREFIX, URL_OLD)
    # dump_json(names, BOOK_NAMES_OLD_CANON)
    # dump_json(figs, FIGURES_OLD_CANON)
    pass
