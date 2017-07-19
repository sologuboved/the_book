# -*- coding: utf-8 -*-

from json_operations import *

BOOK_NAMES_OLD_CANON = 'book_names_old_canon.json'
FIGURES_OLD_CANON = 'figures_old_canon.json'


class Stats(object):
    def __init__(self, names_file, figures_file):
        self._names = load_json(names_file)
        self._figs = load_json(figures_file)

    def find_means(self, show=False):
        means = {b_n: sum(self._figs[b_n]) / float(len(self._figs[b_n])) for b_n in self._figs}
        ord_means = sorted(means.items(), key=lambda m: m[1], reverse=True)
        if show:
            print "Printing Means:"
            print
            self.prettyprint(ord_means)
            print
            print
        return ord_means

    def find_total_mean(self):
        all_chapters = list()
        for book in self._figs.values():
            all_chapters += book
        return sum(all_chapters) / float(len(all_chapters))

    def find_variance(self):
        pass

    def prettyprint(self, items):
        longest = len(max(self._names.values(), key=lambda t: len(t)))
        for en_name, val in items:
            ru_name = self._names[en_name]
            print ru_name + ' ' * (longest - len(ru_name)), '\t\t', val




if __name__ == '__main__':
    stats = Stats(BOOK_NAMES_OLD_CANON, FIGURES_OLD_CANON)
    stats.find_means(True)


