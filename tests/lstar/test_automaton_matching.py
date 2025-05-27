#!/usr/bin/env pytest-3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from pybgl import (
    graph_to_html,
    make_automaton,
    make_func_property_map,
)
from regexp_learner import automaton_match
from ..common import html


G1 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 2, 'a'), (1, 1, 'b'),
        (2, 1, 'a'), (2, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G2 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G3 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
    ], 0,
    make_func_property_map(lambda q: False)
)

G4 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 1, 'b'), (1, 0, 'a')
    ], 0,
    make_func_property_map(lambda q: q == 1)
)

G5 = make_automaton(
    [
        (0, 0, 'a'), (0, 1, 'b'),
        (1, 1, 'b'), (1, 0, 'a')
    ], 0,
    make_func_property_map(lambda q: False)
)


def test_automaton_match12():
    html(graph_to_html(G1))
    html(graph_to_html(G2))
    obtained = automaton_match(G1, G2)
    assert obtained == "ba"
    html(f"These automata don't match for w = {obtained}")


def test_automaton_match11():
    html(graph_to_html(G1))
    html(graph_to_html(G1))
    assert automaton_match(G1, G1) is None
    html("These automata match")


def test_automaton_match13():
    html(graph_to_html(G1))
    html(graph_to_html(G3))
    expected = "b"

    obtained = automaton_match(G3, G1)
    assert expected == obtained, f"{expected=} {obtained=}"
    obtained = automaton_match(G1, G3)
    assert expected == obtained, f"{expected=} {obtained=}"
    html(f"These automata don't match for w = {obtained}")


def test_automaton_match45():
    html(graph_to_html(G4))
    html(graph_to_html(G5))
    expected = "b"

    obtained = automaton_match(G4, G5)
    assert expected == obtained, f"{expected=} {obtained=}"
    obtained = automaton_match(G5, G4)
    assert expected == obtained, f"{expected=} {obtained=}"
    html("These automata don't match for w = {obtained}")
