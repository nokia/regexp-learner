#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

import numpy as np
from operator import itemgetter
from collections import defaultdict

class LstarObservationTable:
    def __init__(self, a = "abcdefghijklmnopqrstuvwxyz"):
        self.a = a
        self.map_prefix = dict() # {str : int} maps prefixes with row indexes
        self.map_suffix = dict() # {str : int} maps suffixes with column indexes
        self.s = set()           # {str} keeps track of prefixes
         # {0,1}^(|map_prefixes|x|map_suffixes|) matrix (observation table)
        self.t = np.zeros((1, 1), dtype = np.bool_)
         # {0,1}^(|map_prefixes|x|map_suffixes|) indicated parts of T that have been probed
        self.probed = np.zeros((1, 1), dtype = np.bool_)

    @property
    def e(self) -> set:
        return set(self.map_suffix.keys())

    @staticmethod
    def get_or_create_index(m :dict, k :str) -> int:
        n = m.get(k)
        if n is None:
            n = len(m)
            m[k] = n
        return n

    def add_row(self):
        self.t      = np.insert(self.t,      self.t.shape[0],      values = 0, axis = 0)
        self.probed = np.insert(self.probed, self.probed.shape[0], values = 0, axis = 0)

    def add_col(self):
        self.t      = np.insert(self.t,      self.t.shape[1],      values = 0, axis = 1)
        self.probed = np.insert(self.probed, self.probed.shape[1], values = 0, axis = 1)

    def add_prefix(self, s :str) -> tuple:
        i = LstarObservationTable.get_or_create_index(self.map_prefix, s)
        (m, n) = self.t.shape
        added = (i >= m)
        if added:
            self.add_row()
        return (i, added)

    def add_suffix(self, e :str) -> tuple:
        j = LstarObservationTable.get_or_create_index(self.map_suffix, e)
        (m, n) = self.t.shape
        added = (j >= n)
        if added:
            self.add_col()
        return (j, added)

    def set(self, s :str, e: str, accepted :bool = True):
        (i, _) = self.add_prefix(s)
        (j, _) = self.add_suffix(e)
        self.t[i, j] = accepted
        self.probed[i, j] = True

    def get_row(self, s :str) -> int:
        return self.map_prefix.get(s)

    def get_col(self, e :str) -> int:
        return self.map_suffix.get(e)

    def get(self, s :str, e :str) -> bool:
        i = self.get_row(s)
        if i is None: return None

        j = self.get_col(e)
        if j is None: return None

        if self.probed[i, j] == False: return None
        ret = self.t[i, j]

        return bool(ret)

    def to_html(self) -> str:

        def bool_to_html(b) -> str:
            return "?" if b is None else str(b)

        def str_to_html(s) -> str:
            return repr(s) if s else "&#x3b5;"

        def prefix_to_html(t, s) -> str:
            return "<font color='red'>%s</font>" % str_to_html(s) if s in t.s \
                else str_to_html(s)

        sorted_prefixes = [
            tup[0] for tup in sorted(self.map_prefix.items(), key=itemgetter(1))
        ]
        sorted_suffixes = [
            tup[0] for tup in sorted(self.map_suffix.items(), key=itemgetter(1))
        ]
        return """
        <table>
            %(header)s
            %(rows)s
        </table>
        """ % {
            "header" : "<tr><th></th>%(ths)s</tr>" % {
                "ths" : "".join([
                    "<td>%s</td>" % str_to_html(suffix) for suffix in sorted_suffixes
                ]),
            },
            "rows" : "".join([
                "<tr><th>%(prefix)s</th>%(cells)s</tr>" % {
                    "cells" : "".join([
                        "<td>%s</td>" % bool_to_html(self.get(s, e)) for e in sorted_suffixes
                    ]),
                    "prefix" : prefix_to_html(self, s),
                } for s in sorted_prefixes
            ]),
        }

    def row(self, s :str) -> bytes:
        i = self.get_row(s)
        # tobytes() is used to get something hashable
        return self.t[i, :].tobytes() if i is not None else None

    #(s1, a) = self.o.find_mismatch_closeness()
    def find_mismatch_closeness(self)  -> tuple:
        assert self.probed.all()
        rows = {self.row(s) for s in self.s}
        for s in self.s:
            for a in self.a:
                row = self.row(s + a)
                if row not in rows:
                    return (s, a)
        return None

    def is_closed(self, verbose :bool = False) -> bool:
        ret = self.find_mismatch_closeness()
        if verbose and ret is not None:
            print("Not closed: s = %s a = %s" % (s, a))
        return ret is None

    def find_mismatch_consistency(self) -> tuple:
        assert self.probed.all()
        for (i1, s1) in enumerate(self.s):
            for (i2, s2) in enumerate(self.s):
                if i2 <= i1:
                    continue
                if self.row(s1) != self.row(s2):
                    continue
                for a in self.a:
                    if self.row(s1 + a) != self.row(s2 + a):
                        for e in self.e:
                            if self.get(s1 + a, e) != self.get(s2 + a, e):
                                return (s1, s2, a, e)
        return None

    def is_consistent(self, verbose :bool = False) -> bool:
        ret = self.find_mismatch_consistency()
        if verbose and ret is not None:
            (s1, s2, a, e) = ret
            print("Not consistent: s1 = %s s2 = %s a = %s e = %s" % (s1, s2, a, e))
        return ret is None

