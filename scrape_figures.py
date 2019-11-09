# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from json_operations import *

PREFIX = 'https://ru.wikisource.org'
URL_OLD = 'https://ru.wikisource.org/wiki/Ветхий_завет'
URL_NEW_BOOKS = 'https://ru.wikisource.org/wiki/Новый_завет'
URL_NEW_NAMES = 'https://ru.wikipedia.org/wiki/Новый_завет'
FIGURES_OLD_CANON = 'figures_old_canon.json'
BOOK_NAMES_OLD_CANON = 'book_names_old_canon.json'
FIGURES_NEW = 'figures_new.json'
BOOK_NAMES_NEW = 'book_names_new.json'
FIGURES_CANON = 'figures_canon.json'
BOOK_NAMES_CANON = 'book_names_canon.json'


def scrape_old_canon(prefix, url, url_names=None):
    """
    Scrape names of books and numbers of verses per chapter from the Old Testament canon
    :param prefix: str
    :param url: str
    :param url_names: None
    :return: tuple ({str: [int, int, ...]}, {srt: srt})
    """
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


def scrape_new(prefix, url_books, url_names):
    """
    Scrape names of books and numbers of verses per chapter from the New Testament
    :param prefix: str
    :param url_books: str
    :param url_names: str
    :return: tuple ({str: [int, int, ...]}, {srt: srt})
    """
    en_book_names = scrape_book_names_new(url_names)

    ru_book_names = list()
    figures_list = list()

    soup = BeautifulSoup(requests.get(url_books).content)

    lines = soup.find_all('li')  # up to -49
    for line in lines[: -48]:  # 27 in total
        if str(line)[: 6] == '<li><a':
            book_name = line.text
            ru_book_names.append(book_name)
            book_url = prefix + line.find('a').get('href')
            figures_list.append(scrape_book(book_name, book_url))

    assert len(en_book_names) == len(ru_book_names) == len(figures_list), "Inequal lengths"

    book_names = dict(zip(en_book_names, ru_book_names))
    figures = dict(zip(en_book_names, figures_list))
    return book_names, figures


def scrape_book_names_new(url):
    """
    Scrape English abbreviations of the New Testament book titles
    :param url: str
    :return: list
    """
    soup = BeautifulSoup(requests.get(url).content)
    table = soup.find('table', {'class': 'standard'})
    return [row.find_all('td')[5].text.split(',')[0].replace(' ', '') for row in table.find_all('tr')[2:]]


def scrape_book(book_name, url):
    """
    Scrape number of verses per chapter in the given book
    :param book_name: str
    :param url: str
    :return: list of ints
    """
    print('Scraping', book_name)
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


def launch_scrape_and_dump_separate(scrape, prefix, url_books, url_names, book_names_json, figures_json):
    """
    Scrape and dump into json files either the Old or the New Testament names of books and numbers of verses per chapter
    :param scrape: func
    :param prefix: str
    :param url_books: str
    :param url_names: str or None
    :param book_names_json: str
    :param figures_json: srt
    :return: None
    """
    names, figures = scrape(prefix, url_books, url_names)
    dump_json(names, book_names_json)
    dump_json(figures, figures_json)


def launch_scrape_and_dump_joined(prefix, url_books_old, url_books_new, url_names_new, books_names_json, figures_json):
    """
    Scrape and dump into json files both the Old and the New Testament names of books and numbers of verses per chapter
    :param prefix: str
    :param url_books_old: str
    :param url_books_new: str
    :param url_names_new: str
    :param books_names_json: str
    :param figures_json: str
    :return: None
    """
    names_old, figures_old = scrape_old_canon(prefix, url_books_old)
    length_n_old, length_f_old = len(names_old), len(figures_old)
    names_new, figures_new = scrape_new(prefix, url_books_new, url_names_new)
    names_old.update(names_new)
    figures_old.update(figures_new)
    assert len(names_old) == len(names_new) + length_n_old, "Something went wrong with Names"
    assert len(figures_old) == len(figures_new) + length_f_old, "Something went wrong with Figures"
    dump_json(names_old, books_names_json)
    dump_json(figures_old, figures_json)


if __name__ == '__main__':
    # launch_scrape_and_dump_joined(PREFIX, URL_OLD, URL_NEW_BOOKS, URL_NEW_NAMES, BOOK_NAMES_CANON, FIGURES_CANON)
    # joined = load_json(BOOK_NAMES_CANON)
    # launch_scrape_and_dump_separate(scrape_new, PREFIX, URL_NEW_BOOKS, URL_NEW_NAMES, BOOK_NAMES_NEW, FIGURES_NEW)
    # for en, ru in load_json(BOOK_NAMES_NEW).items():
    #     print en, ru
    pass
