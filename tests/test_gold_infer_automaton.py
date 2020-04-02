#!/usr/bin/env pytest
# -*- coding: utf-8 -*-

__author__ = "Maxime Raynal"
__maintainer__ = "Maxime Raynal"
__email__ = "maxime.raynal@nokia.com"
__copyright__ = "Copyright (C) 2020, Nokia"
__license__ = "BSD-3"

from gold_inference.gold_infer_automaton import gold_infer_automaton
from pybgl.automaton import num_vertices, num_edges


def test_gold_infer_automaton():
    s_plus = {'abb', 'bb', 'bba', 'bbb', 'babb'}
    s_minus = {'', 'a', 'ba'}
    sigma = 'ab'
    b, g = gold_infer_automaton(s_plus, s_minus, sigma=sigma)
    assert b
    assert num_vertices(g) == 3
    assert num_edges(g) == 6
    b, g = gold_infer_automaton(s_plus, s_minus, sigma=sigma, fill_holes=True)
    assert b
    assert num_vertices(g) == 3
    assert num_edges(g) == 6
