#!/usr/bin/env pytest-3
# -*- coding: utf-8 -*-

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

from pybgl.automaton        import make_automaton
from pybgl.graphviz         import dotstr_to_html
from pybgl.property_map     import make_func_property_map
from pybgl.html             import html
from lstar.automaton_match  import automaton_match

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
    svg = dotstr_to_html(G1.to_dot())
    html(svg)
    svg = dotstr_to_html(G2.to_dot())
    html(svg)

    obtained = automaton_match(G1, G2)
    assert obtained == "ba"

    html("These automata don't match for w = %r" % obtained)

def test_automaton_match11():
    html(dotstr_to_html(G1.to_dot()))
    html(dotstr_to_html(G1.to_dot()))
    assert automaton_match(G1, G1) == None

    html("These automata match")

def test_automaton_match13():
    html(dotstr_to_html(G1.to_dot()))
    html(dotstr_to_html(G3.to_dot()))
    expected = "b"

    obtained = automaton_match(G3, G1)
    assert expected == obtained, "expected = %r obtained = %r" % (expected, obtained)

    obtained = automaton_match(G1, G3)
    assert expected == obtained, "expected = %r obtained = %r" % (expected, obtained)

    html("These automata don't match for w = %r" % obtained)

def test_automaton_match45():
    html(dotstr_to_html(G4.to_dot()))
    html(dotstr_to_html(G5.to_dot()))
    expected = "b"

    obtained = automaton_match(G4, G5)
    assert expected == obtained, "expected = %r obtained = %r" % (expected, obtained)

    obtained = automaton_match(G5, G4)
    assert expected == obtained, "expected = %r obtained = %r" % (expected, obtained)

    html("These automata don't match for w = %r" % obtained)
