#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from regexp_learner.gold.gold import gold
from pybgl.automaton import num_vertices, num_edges

def test_gold_gold():
    s_plus = {"abb", "bb", "bba", "bbb", "babb"}
    s_minus = {"", "a", "ba"}
    sigma = "ab"
    (g, success) = gold(s_plus, s_minus, sigma=sigma)
    assert success
    assert num_vertices(g) == 3
    assert num_edges(g) == 6
    (g, success) = gold(s_plus, s_minus, sigma=sigma, fill_holes=True)
    assert success
    assert num_vertices(g) == 3
    assert num_edges(g) == 6
