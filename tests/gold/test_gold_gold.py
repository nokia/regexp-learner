#!/usr/bin/env pytest
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from pybgl import in_ipynb
from regexp_learner import gold


def test_gold_gold():
    verbose = in_ipynb()
    s_plus = {"abb", "bb", "bba", "bbb", "babb"}
    s_minus = {"", "a", "ba"}
    sigma = "ab"
    (g, success) = gold(
        s_plus, s_minus,
        sigma=sigma, verbose=verbose
    )
    assert success
    assert g.num_vertices() == 3
    assert g.num_edges() == 6
    (g, success) = gold(
        s_plus, s_minus,
        sigma=sigma, fill_holes=True, verbose=verbose
    )
    assert success
    assert g.num_vertices() == 3
    assert g.num_edges() == 6
