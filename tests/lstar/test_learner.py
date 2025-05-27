#!/usr/bin/env pytest-3
# -*- coding: utf-8 -*-
#
# This file is part of the regexp-learner project
# https://github.com/nokia/regexp-learner

from pybgl import (
    Automaton,
    graph_to_html,
    in_ipynb,
    make_automaton,
    make_func_property_map,
)
from regexp_learner import (
    Learner,
    LstarObservationTable,
    Teacher,
    automaton_match,
    make_automaton_from_observation_table,
)
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


def test_make_automaton_from_observation_table():
    # Build observation table
    o = LstarObservationTable("ab")
    o.s = {"", "b", "ba"}
    o.set("", "", False)
    o.set("", "a", False)
    o.set("b", "", True)
    o.set("b", "a", False)
    o.set("a", "", False)
    o.set("a", "a", False)
    o.set("ba", "", False)
    o.set("ba", "a", True)
    o.set("bb", "", True)
    o.set("bb", "a", False)
    o.set("baa", "", True)
    o.set("baa", "a", False)
    o.set("bab", "", True)
    o.set("bab", "a", False)
    is_consistent = o.is_consistent()
    is_closed = o.is_closed()

    # Check
    html(o.to_html())
    html(
        "This observation table is %sconsistent" % (
            "" if is_consistent else "<b>not</b> "
        )
    )
    html(
        "This observation table is %sclosed" % (
            "" if is_closed else "<b>not</b> "
        )
    )
    assert is_consistent
    assert is_closed

    # Build and display the corresponding automaton
    h = make_automaton_from_observation_table(o)

    html("<b>obtained</b>")
    html(graph_to_html(h))
    html("<b>expected</b>")
    html(graph_to_html(G1))
    assert automaton_match(G1, h) is None


def test_make_automaton_from_observation_table2():
    # Build observation table
    o = LstarObservationTable("ab")
    o.s = {"", "a"}
    o.set("", "", False)
    o.set("a", "", True)
    o.set("b", "", False)
    o.set("aa", "", True)
    o.set("ab", "", False)
    is_consistent = o.is_consistent()
    is_closed = o.is_closed()

    # Check
    html(o.to_html())
    html(
        "This observation table is %sconsistent" % (
            "" if is_consistent else "<b>not</b> "
        )
    )
    html(
        "This observation table is %sclosed" % (
            "" if is_closed else "<b>not</b> "
        )
    )
    assert is_consistent
    assert is_closed

    # Build and display corresponding automatonbb
    h = make_automaton_from_observation_table(o)
    expected = make_automaton(
        [
            (0, 0, 'b'), (0, 1, 'a'),
            (1, 1, 'a'), (1, 0, 'b')
        ], 0,
        make_func_property_map(lambda q: q == 1)
    )
    html("<b>obtained</b>")
    html(graph_to_html(h))
    html("<b>expected</b>")
    html(graph_to_html(expected))
    assert automaton_match(expected, h) is None


def test_learners(gs: list[Automaton] = [G1, G2, G3, G4, G5]):
    verbose = in_ipynb()

    def test_learner(g):
        if not g.is_complete():
            html(graph_to_html(g))
            html(
                "Ignored, this automaton must be finite, "
                "deterministic and complete"
            )
            return

        teacher = Teacher(g)
        html("<b>Teacher</b>")
        html(graph_to_html(teacher.g))

        learner = Learner(teacher)
        h = learner.learn(verbose=verbose)
        html("<b>Learner</b>")
        html(graph_to_html(h))

        assert automaton_match(g, h) is None
        html(":-)")

    for (i, g) in enumerate(gs):
        html(f"<h3>Test G{i + 1}</h3>")
        test_learner(g)
