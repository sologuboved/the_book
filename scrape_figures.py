import requests
from bs4 import BeautifulSoup
import json

FIGURES_OLD = 'figures_old.json'


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def dump_json(data, json_file):
    with open(json_file, 'w') as handler:
        json.dump(data, handler)


def scrape_book(url):
    soup = BeautifulSoup(requests.get(url).content)
    verses = [map(int, item.get('id').split(':')) for item in soup.find_all('span', {'style': 'color:#00F;'})]
    print verses[-1]
    verses_per_chapter = list()
    previous_chapter_num = 1
    last_verse_num = None
    for curr_chapter_num, curr_verse_num in verses:
        if curr_chapter_num != previous_chapter_num:
            print curr_verse_num, last_verse_num
            verses_per_chapter.append(last_verse_num)
            previous_chapter_num = curr_chapter_num
            last_verse_num = curr_verse_num
        else:
            last_verse_num = curr_verse_num
    verses_per_chapter.append(verses[-1][1])
    print verses_per_chapter, len(verses_per_chapter)


if __name__ == '__main__':
    scrape_book('https://ru.wikisource.org/wiki/%D0%9F%D1%81%D0%B0%D0%BB%D1%82%D0%B8%D1%80%D1%8C')
