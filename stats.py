# -*- coding: utf-8 -*-

from json_operations import *
import math

BOOK_NAMES_OLD_CANON = 'book_names_old_canon.json'
FIGURES_OLD_CANON = 'figures_old_canon.json'
FIGURES_NEW = 'figures_new.json'
BOOK_NAMES_NEW = 'book_names_new.json'
FIGURES_CANON = 'figures_canon.json'
BOOK_NAMES_CANON = 'book_names_canon.json'


class Stats(object):
    def __init__(self, names_file, figures_file):
        self._names = load_json(names_file)
        self._figs = load_json(figures_file)

    @staticmethod
    def get_ordered_items(dictionary):
        return sorted(dictionary.items(), key=lambda i: i[1], reverse=True)

    def find_means(self, show=False):
        means = {b_n: sum(self._figs[b_n]) / float(len(self._figs[b_n])) for b_n in self._figs}
        if show:
            self.prettyprint(means, 'Means')
        return means

    def find_total_mean(self):
        all_chapters = list()
        for book in self._figs.values():
            all_chapters += book
        return sum(all_chapters) / float(len(all_chapters))

    def find_variances(self, show=False):
        variances = dict()
        means = self.find_means()
        length = float(len(self._figs))
        for name in self._figs:
            mean = means[name]
            numerator = 0
            for chapter in self._figs[name]:
                numerator += (chapter - mean) ** 2
            variances[name] = numerator / length
        if show:
            self.prettyprint(variances, 'Variances')
        return variances

    def find_standard_deviations(self, show=False):
        variances = self.find_variances()
        standard_deviations = {name: math.sqrt(variances[name]) for name in variances}
        if show:
            self.prettyprint(standard_deviations, "Standard Deviations")
        return standard_deviations

    def prettyprint(self, dictionary, label):
        print "Printing", label
        print
        longest = len(max(self._names.values(), key=lambda t: len(t)))
        ordered_items = self.get_ordered_items(dictionary)
        for en_name, val in ordered_items:
            ru_name = self._names[en_name]
            print ru_name + ' ' * (longest - len(ru_name)), '\t\t', val
        print
        print


if __name__ == '__main__':
    # stats_old = Stats(BOOK_NAMES_OLD_CANON, FIGURES_OLD_CANON)
    # stats_old.find_means(True)
    # stats_old.find_variances(True)
    # stats_old.find_standard_deviations(True)

    stats_new = Stats(BOOK_NAMES_NEW, FIGURES_NEW)
    stats_new.find_means(True)
    # stats_new.find_variances(True)
    stats_new.find_standard_deviations(True)

    # stats_both = Stats(BOOK_NAMES_CANON, FIGURES_CANON)
    # stats_both.find_means(True)
    # stats_both.find_variances(True)
    # stats_both.find_standard_deviations(True)

    pass
